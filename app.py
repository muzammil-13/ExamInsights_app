import logging
import sys
import os
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

load_dotenv()


def normalize_source_config(source_config: dict) -> dict:
    """Support both the old nested YAML shape and the current flat source shape."""
    if "kind" in source_config:
        return source_config

    for name, config in source_config.items():
        if isinstance(config, dict) and "kind" in config:
            return {"name": name, **config}

    raise ValueError(f"Invalid source configuration: {source_config}")


def data_sources(source_configs) -> list[pw.Table]:
    sources = []
    for raw_source_config in source_configs:
        source_config = normalize_source_config(raw_source_config)
        source_name = source_config.get("name", source_config["kind"])

        if source_config["kind"] == "local":
            source = pw.io.fs.read(
                **source_config["config"],
                format="binary",
                with_metadata=True,
                name=source_name,
            )
            sources.append(source)
        elif source_config["kind"] == "gdrive":
            source = pw.io.gdrive.read(
                **source_config["config"],
                with_metadata=True,
                name=source_name,
            )
            sources.append(source)
        elif source_config["kind"] == "sharepoint":
            try:
                import pathway.xpacks.connectors.sharepoint as io_sp

                source = io_sp.read(
                    **source_config["config"],
                    with_metadata=True,
                    name=source_name,
                )
                sources.append(source)
            except ImportError:
                print(
                    "The Pathway Sharepoint connector is part of the commercial offering, "
                    "please contact us for a commercial license."
                )
                sys.exit(1)
        else:
            raise ValueError(f"Unsupported source kind: {source_config['kind']}")

    return sources

@click.command()
@click.option("--config_file", default="config.yaml", help="Config file to be used.")
def run(config_file: str = "config.yaml"):
    with open(config_file) as config_f:
        configuration = yaml.safe_load(config_f)

    LLM_MODEL = configuration["llm_config"]["model"]

    embedding_model = "avsolatorio/GIST-small-Embedding-v0"

    embedder = embedders.SentenceTransformerEmbedder(
        embedding_model,
        call_kwargs={"show_progress_bar": False}
    )

    chat = llms.LiteLLMChat(
        model=LLM_MODEL,
        retry_strategy=ExponentialBackoffRetryStrategy(max_retries=6),
        cache_strategy=DiskCache(),
    )

    host_config = configuration["host_config"]
    host, port = host_config["host"], host_config["port"]

    doc_store = VectorStoreServer(
        *data_sources(configuration["sources"]),
        embedder=embedder,
        splitter=splitters.TokenCountSplitter(max_tokens=400),
        parser=parsers.ParseUnstructured(),
    )

    rag_app = BaseRAGQuestionAnswerer(llm=chat, indexer=doc_store)

    rag_app.build_server(host=host, port=port)

    cache_options = configuration.get("cache_options", {})
    rag_app.run_server(
        with_cache=cache_options.get("with_cache", True),
        terminate_on_error=False,
    )

if __name__ == "__main__":
    run()
