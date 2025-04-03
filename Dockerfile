FROM python:3.10-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]