# [START functions_cloudevent_pubsub]
import base64
import json

from cloudevents.http import CloudEvent
import functions_framework
import requests
import os

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    body = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode())

    requests.post(
        os.environ.get('API_URL') + '/predict-crop-yield-advice',
        json=body,
    )

    print('Call api for generate advice success')


# [END functions_cloudevent_pubsub]