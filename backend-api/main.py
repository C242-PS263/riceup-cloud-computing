import os
from google.cloud import firestore
import tensorflow as tf
from fastapi import FastAPI, UploadFile
import numpy as np

PROJECT_ROOT: str = os.path.dirname(os.path.abspath(__file__))
DISEASE_MODEL_PATH = os.path.abspath(PROJECT_ROOT + '/storage/models/rice_disease_detector_model.json')
DISEASE_WEIGHTS_PATH = os.path.abspath(PROJECT_ROOT + '/storage/models/rice_disease_detector_weights.weights.h5')

MODEL_DISEASE_CLASS = (
    "leaf blast",
    "leaf scald",
    "tungro",
    "brown spot",
    "rice hispa",
    "bacterial leaf blight",
    "neck blast",
    "sheath blight",
    "narrow brown spot",
    "healthy",
)

firestore_db = firestore.Client()
diseases_ref = firestore_db.collection(u'diseases')

with open(DISEASE_MODEL_PATH, 'r') as f:
    disease_model = tf.keras.models.model_from_json(f.read())
disease_model.load_weights(DISEASE_WEIGHTS_PATH)

app = FastAPI()

@app.get("/")
def root():
    return "service is working"

@app.post('/predict')
async def predict(file: UploadFile):
    img = tf.io.decode_image(file.file.read(), channels=3)
    img = tf.image.resize(img, (150, 150))
    img = tf.expand_dims(img, axis=0)
    prediction = disease_model.predict(img)
    predicted_class = MODEL_DISEASE_CLASS[np.argmax(prediction) - 1]
    information = diseases_ref.document(predicted_class).get().to_dict()
    return {
        "prediction": predicted_class,
        "raw_prediction": str(prediction),
        "information": information,
    }