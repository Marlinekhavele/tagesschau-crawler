FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./


RUN poetry install --only main --no-interaction --no-ansi

COPY . .

EXPOSE 8050

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=8050"]