# Ingestion and Anomaly Detection System
This project is a demonstration of a scalable architecture for ingesting, processing, and analyzing anomaly events using RabbitMQ, PostgreSQL, and Docker. The system is composed of several key components:

- Ingestion API
- Worker Service
- Autoscaler
- RabbitMQ
- PostgreSQL Database

## Components

### Ingestion API

The Ingestion API is responsible for receiving events and publishing them to the RabbitMQ queue.

- **Language:** Python
- **Framework:** FastAPI
- **Dependencies:** `aio-pika`, `pydantic`, `fastapi`, `uvicorn`
- **Role:** Accepts incoming events and publishes them to RabbitMQ for processing.

### Worker Service

The Worker Service is responsible for processing events from the RabbitMQ queue, detecting anomalies, and storing results in the PostgreSQL database.

- **Language:** Python
- **Dependencies:** `aio-pika`, `sqlalchemy`, `psycopg2-binary`
- **Role:** Consumes messages from RabbitMQ, processes events, detects anomalies, and stores results in PostgreSQL.
- **Scaling:** The service can be scaled up or down based on the queue length, as managed by the Autoscaler.

### Autoscaler

The Autoscaler monitors the length of the RabbitMQ queue and adjusts the number of Worker Service instances accordingly.

- **Language:** Python
- **Dependencies:** `docker`, `requests`
- **Role:** Monitors RabbitMQ queue length and scales Worker Service instances up or down based on predefined thresholds.
- **Behavior:**
  - Waits 60 seconds at boot time to 
  - Checks the queue length every 10 seconds.
  - Scales up if the queue length exceeds a threshold of 10 (configurable).

### RabbitMQ

RabbitMQ is used as the messaging broker for the system, allowing the Ingestion API and Worker Service to communicate asynchronously.

- **Image:** `rabbitmq:3-management`
- **Role:** Message broker facilitating communication between services.
- **Management UI:** Accessible at `http://localhost:15672` with default credentials (`guest` / `guest`).

### PostgreSQL Database

PostgreSQL is used as the database to store event and anomaly data processed by the Worker Service.

- **Image:** `postgres:13`
- **Role:** Persistent storage for event and anomaly data.
- **Default Credentials:** 
  - **User:** `user`
  - **Password:** `pass`
  - **Database:** `mydb`


## Setup and Running

### Prerequisites

- Docker
- Docker Compose
- Docker Swarm (if using swarm mode)

### Build and Deploy

1. **Run the Build Script:**

   Run the provided `build_images.sh` script to build the Docker images:

   ```bash
   chmod +x build_images.sh
   ./build_images.sh
   
## Usage

### Ingestion API

**Endpoint:** `/ingest`

**Method:** `POST`

**Payload:**

```json
{
  "id": "123452",
  "event_id": "55555334343",
  "role_id": "role123",
  "event_type": "CreateInstance",
  "event_timestamp": "2023-06-07T12:34:56Z",
  "affected_assets": ["asset1", "asset2"]
}
```

**CURL request:**
```curl --location 'http://localhost:5001/ingest' \
--header 'Content-Type: application/json' \
--data '{
  "id": "123452",
  "event_id": "52572",
  "role_id": "role123",
  "event_type": "CreateInstance",
  "event_timestamp": "1717970237",
  "affected_assets": ["asset1", "asset2"]
}'
```
Feel free to copy this and save it as `README.md` in your project.