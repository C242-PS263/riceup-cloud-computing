import os
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()

topic_set_predict_crop_yield_advice = 'projects/{project_id}/topics/{topic}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    topic='set-predict-crop-yield-advice ',
)