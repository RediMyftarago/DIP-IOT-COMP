import json, os
from datetime import datetime, timezone
from fastapi import FastAPI
from kafka import KafkaProducer
from pydantic import BaseModel

KAFKA = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = "parking.iot.occupancy"
producer = KafkaProducer(bootstrap_servers=KAFKA, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
app = FastAPI(title="IoT Bridge")
last = {}

class SensorEvent(BaseModel):
    spotId: int
    occupied: bool

@app.post("/sensor")
def sensor(event: SensorEvent):
    if last.get(event.spotId) == event.occupied:
        return {"status": "unchanged"}
    last[event.spotId] = event.occupied
    payload = event.model_dump()
    payload["sourceType"] = "IOT"
    payload["timestamp"] = datetime.now(timezone.utc).isoformat()
    producer.send(TOPIC, payload)
    producer.flush()
    return {"status": "published", "event": payload}
