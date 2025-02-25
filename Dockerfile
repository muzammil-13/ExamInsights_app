FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-opencv && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-opencv && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/root/.local/bin:$PATH
COPY . .

EXPOSE 8000 8501
CMD ["sh", "-c", "python app.py & streamlit run streamlit_app.py"]
