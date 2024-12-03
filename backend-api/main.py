import os
from google.cloud import firestore
import tensorflow as tf
from fastapi import FastAPI, UploadFile
import numpy as np
from pydantic import BaseModel, Field
from enum import Enum
from formula import crop

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

class RainfallStatus(str, Enum):
    sangat_rendah = "sangat rendah"
    rendah = "rendah"
    normal = "normal"
    tinggi = "tinggi"
    sangat_tinggi = "sangat tinggi"

class DiseaseLevel(str, Enum):
    sangat_rendah = "sangat rendah"
    rendah = "rendah"
    normal = "normal"
    tinggi = "tinggi"
    sangat_tinggi = "sangat tinggi"

class PlantingDistance(str, Enum):
    _20cmx20cm = "20cmx20cm"
    _25cmx25cm = "25cmx25cm"
    _30cmx30cm = "30cmx30cm"

class PredictCropYieldRequest(BaseModel):
    land_area: int = Field(examples=[1000])
    rainfall: RainfallStatus = Field(examples=[RainfallStatus.normal])
    disease_level: DiseaseLevel = Field(examples=[DiseaseLevel.normal])
    temperature: float = Field(examples=[21.8])
    planting_distance: PlantingDistance = Field(examples=[PlantingDistance._20cmx20cm])

@app.post('/predict-crop-yield')
async def predict_crop_yield(req: PredictCropYieldRequest):
    seed_weight = crop.seed_amount(req.land_area, req.planting_distance)  # Jumlah bibit padi (kg)

    gkp = crop.fuzzy_yield_prediction(
        req.land_area,
        req.rainfall,
        req.disease_level,
        req.temperature,
        req.planting_distance,
    )
    gkg = crop.gkg_from_gkp(gkp)
    rice = crop.rice_from_gkg(gkg)

    return {
        'land_area': req.land_area, # m2
        'rainfall': req.rainfall,
        'disease_level': req.disease_level, 
        'temperature': req.temperature, #C
        'planting_distance': req.planting_distance, 
        'seed_weight': seed_weight, 
        'gkp': gkp, 
        'gkg': gkg, 
        'rice': rice,
    }