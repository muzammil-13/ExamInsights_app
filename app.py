import importlib
import logging
import sys
import os
from datetime import datetime
import click
import pathway as pw
import yaml
from dotenv import load_dotenv

from pathway.udfs import DiskCache, ExponentialBackoffRetryStrategy
from pathway.xpacks.llm import embedders, llms, parsers, splitters
from pathway.xpacks.llm.question_answering import BaseRAGQuestionAnswerer
from pathway.xpacks.llm.vector_store import VectorStoreServer

# To use advanced features with Pathway Scale, get your free license key from
# https://pathway.com/features and paste it below.
# To use Pathway Community, comment out the line below.
pw.set_license_key("demo-license-key-with-telemetry")

# Create logs directory if it doesn't exist (target /logs/ path)
LOG_DIR = os.getenv("LOG_DIR", "/logs")
try:
    os.makedirs(LOG_DIR, exist_ok=True)
except OSError:
    LOG_DIR = "logs"
    os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging with both console and file handlers
log_filename = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(console_formatter)

# File handler
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logging.info(f"Application started. Log file: {log_filename}")

load_dotenv()


def normalize_source_config(source_config: dict) -> dict:
    """Support both the old nested YAML shape and the current flat source shape."""
    try:
        if "kind" in source_config:
            return source_config

        for name, config in source_config.items():
            if isinstance(config, dict) and "kind" in config:
                return {"name": name, **config}

        raise ValueError(f"Invalid source configuration: {source_config}")
    except Exception as e:
        logging.error(f"Error normalizing source config: {e}")
        raise


def data_sources(source_configs) -> list[pw.Table]:
    logging.info(f"Loading {len(source_configs)} data source(s)")
    sources = []
    for raw_source_config in source_configs:
        source_config = normalize_source_config(raw_source_config)
        source_name = source_config.get("name", source_config["kind"])
        logging.info(f"Configuring data source: {source_name} (kind: {source_config['kind']})")

        if source_config["kind"] == "local":
            source = pw.io.fs.read(
                **source_config["config"],
                format="binary",
                with_metadata=True,
                name=source_name,
            )
            sources.append(source)
            logging.info(f"Local source '{source_name}' loaded successfully")
        elif source_config["kind"] == "gdrive":
            source = pw.io.gdrive.read(
                **source_config["config"],
                with_metadata=True,
                name=source_name,
            )
            sources.append(source)
            logging.info(f"Google Drive source '{source_name}' loaded successfully")
        elif source_config["kind"] == "sharepoint":
            io_sp = None
            for module_name in (
                "pathway.xpacks.connectors.sharepoint",
                "pathway.xpacks.sharepoint",
            ):
                try:
                    io_sp = importlib.import_module(module_name)
                    break
                except ImportError:
                    continue

            if io_sp is None:
                logging.error("The Pathway SharePoint connector is part of the commercial offering")
                print(
                    "The Pathway SharePoint connector is part of the commercial offering, "
                    "please contact us for a commercial license."
                )
                sys.exit(1)

            source = io_sp.read(
                **source_config["config"],
                with_metadata=True,
                name=source_name,
            )
            sources.append(source)
            logging.info(f"SharePoint source '{source_name}' loaded successfully")
        else:
            logging.error(f"Unsupported source kind: {source_config['kind']}")
            raise ValueError(f"Unsupported source kind: {source_config['kind']}")

    logging.info(f"Successfully loaded {len(sources)} data source(s)")
    return sources

@click.command()
@click.option("--config_file", default="config.yaml", help="Config file to be used.")
def run(config_file: str = "config.yaml"):
    try:
        logging.info(f"Loading configuration from: {config_file}")
        with open(config_file) as config_f:
            configuration = yaml.safe_load(config_f)
        logging.info("Configuration loaded successfully")

        LLM_MODEL = configuration["llm_config"]["model"]
        logging.info(f"LLM Model: {LLM_MODEL}")

        embedding_model = "avsolatorio/GIST-small-Embedding-v0"
        logging.info(f"Embedding Model: {embedding_model}")

        logging.info("Initializing embedder...")
        embedder = embedders.SentenceTransformerEmbedder(
            embedding_model,
            call_kwargs={"show_progress_bar": False}
        )
        logging.info("Embedder initialized")

        logging.info("Initializing LLM chat...")
        chat = llms.LiteLLMChat(
            model=LLM_MODEL,
            retry_strategy=ExponentialBackoffRetryStrategy(max_retries=6),
            cache_strategy=DiskCache(),
        )
        logging.info("LLM chat initialized")

        host_config = configuration["host_config"]
        host, port = host_config["host"], host_config["port"]
        logging.info(f"Server configuration: {host}:{port}")

        logging.info("Initializing document store...")
        doc_store = VectorStoreServer(
            *data_sources(configuration["sources"]),
            embedder=embedder,
            splitter=splitters.TokenCountSplitter(max_tokens=400),
            parser=parsers.ParseUnstructured(),
        )
        logging.info("Document store initialized")

        logging.info("Building RAG application...")
        rag_app = BaseRAGQuestionAnswerer(llm=chat, indexer=doc_store)
        rag_app.build_server(host=host, port=port)
        logging.info("RAG application built")

        cache_options = configuration.get("cache_options", {})
        logging.info(f"Cache options: {cache_options}")
        
        logging.info(f"Starting server on {host}:{port}")
        rag_app.run_server(
            with_cache=cache_options.get("with_cache", True),
            terminate_on_error=False,
        )
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_file}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run()
