import asyncio

from fastapi import FastAPI, HTTPException
import json
import aio_pika
import asyncio

from ingestion_api.config.config_loader import ConfigLoader
from ingestion_api.middleware.ingest_middleware import IngestMiddleware
from ingestion_api.models.anomaly_event import AnomalyEvent, IngestResponse, Metadata, IngestResponseData
from ingestion_api.utils.logger import logger

app = FastAPI()

# Adding middleware
app.add_middleware(IngestMiddleware)


def get_rabbitmq_uri() -> str:
    logger.info(f"Connecting to RabbitMQ: {RABBITMQ_HOST}"
                f" with user: {RABBITMQ_USER}")

    return f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/"


config = ConfigLoader().load_config()
RABBITMQ_QUEUE = config['RABBITMQ_QUEUE']
RABBITMQ_USER = config.get('RABBITMQ_USER')
RABBITMQ_PASSWORD = config.get('RABBITMQ_PASSWORD')
RABBITMQ_HOST = config.get('RABBITMQ_HOST')


async def publish_event(event: AnomalyEvent):
    try:
        connection = await aio_pika.connect_robust(get_rabbitmq_uri())
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(RABBITMQ_QUEUE, durable=True)
            message = aio_pika.Message(body=json.dumps(event.dict(), default=str).encode())
            await channel.default_exchange.publish(message, routing_key=RABBITMQ_QUEUE)

            logger.info(f"Published event: {event.json()}")

    except Exception as e:
        logger.error(f"Error publishing event: {e}")
        raise HTTPException(status_code=500, detail="Error publishing event")

    finally:
        logger.info("Closing connection")
        await channel.close()


@app.post('/ingest', response_model=IngestResponse)
async def ingest_event(event: AnomalyEvent):
    logger.info("Received event")
    try:
        await publish_event(event)
    except Exception as e:
        logger.error(f"Error publishing event: {e}")
        raise HTTPException(status_code=500, detail="Error publishing event")
    return IngestResponse(
        data=IngestResponseData(status="success"),
        metadata=Metadata(request_id=event.id)
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=5001)
