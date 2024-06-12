FROM python:3.9-slim AS base

# Set the working directory to /app
WORKDIR /app

# Install gcc and other dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app/ingestion_api

# Workaround for the wait-for-it.sh script, since docker-compose v3.9 does not support depends_on condition for services
COPY wait-for-it.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Set PYTHONPATH to the root of the project to find modules
ENV PYTHONPATH=/app

FROM base AS tester

# Copy the tests
COPY tests/ /app/tests/
RUN pip install pytest
RUN pytest /app/tests/

FROM base AS final

# CMD for starting the application
CMD ["wait-for-it.sh", "db:5432", "--", "wait-for-it.sh", "rabbitmq:5672", "--", "python", "ingestion_api/api.py"]
