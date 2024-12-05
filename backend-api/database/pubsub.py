import os
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()

topic_set_predict_crop_yield_advice = publisher.topic_path(os.getenv('GOOGLE_CLOUD_PROJECT'), 'set-predict-crop-yield-advice')