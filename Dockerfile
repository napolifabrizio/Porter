FROM python:3.11.9-slim AS builder

RUN pip install poetry==2.1.2

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root

COPY source/ ./source/
RUN poetry install


FROM python:3.11.9-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/source /app/source

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "porter.app:app", "--host", "0.0.0.0", "--port", "8000"]
