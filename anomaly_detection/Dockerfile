FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire anomaly_detection directory to /app
COPY . /app/anomaly_detection

# Workaround for the wait-for-it.sh script, since docker-compose v3.9 does not support depends_on condition for services
COPY wait-for-it.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-it.sh


# Set PYTHONPATH to the root of the project to find modules
ENV PYTHONPATH=/app

#CMD ["python", "anomaly_detection/worker.py"]
CMD ["wait-for-it.sh", "db:5432", "--", "wait-for-it.sh", "rabbitmq:5672", "--", "python", "anomaly_detection/worker.py"]
