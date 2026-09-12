# Dockerfile — Microserviço Python (FastAPI) para Railway

FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./
RUN pip install uv --no-cache-dir && uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --http h11