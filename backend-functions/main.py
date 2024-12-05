# [START functions_cloudevent_pubsub]
import base64
import json

from cloudevents.http import CloudEvent
import functions_framework
from ai import predict
from model.predict import *
from database.memorystore import redis_client

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    body = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode())

    req = PredictCropYieldAdviceRequest(**body)

    advice = predict.advice_predict_generate(req)

    redis_client.set(req.as_redis_key(), advice)

    print('Saved advice to Redis: {}'.format(req.as_redis_key()))


# [END functions_cloudevent_pubsub]