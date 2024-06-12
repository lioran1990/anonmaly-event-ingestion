# autoscaler/Dockerfile_backup
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY autoscaler.py .
COPY . /app/autoscaler

# Workaround for the wait-for-it.sh script, since docker-compose v3.9 does not support depends_on condition for services
COPY wait-for-it.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Set PYTHONPATH to the root of the project to find modules
ENV PYTHONPATH=/app

CMD ["wait-for-it.sh", "rabbitmq:5672", "--", "python", "autoscaler/autoscaler.py"]