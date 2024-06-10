#!/bin/bash

# Function to clean up the stack
cleanup() {
    echo "Removing the Docker stack..."
    docker stack rm my_stack
    echo "Docker stack removed."
}

# Trap to catch script exit and run the cleanup function
trap cleanup EXIT

# Build the ingestion API image with the latest tag
echo "Building ingestion API image..."
docker build -t ingestion_api:latest ./ingestion_api

# Build the worker image with the latest tag
echo "Building worker image..."
docker build -t anomaly_detection:latest ./anomaly_detection

# Build the autoscaler image with the latest tag
echo "Building autoscaler image..."
docker build -t autoscaler:latest ./autoscaler

echo "All images have been built and tagged with 'latest' successfully."

# Deploy the stack
docker stack deploy -c docker-compose.yml my_stack

# Keep the script running to keep the stack active
echo "Press Ctrl+C to stop the script and remove the stack..."
while true; do
    sleep 1
done
