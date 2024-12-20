import os
import tensorflow as tf
from fastapi import FastAPI, UploadFile
import numpy as np
from formula import crop
from ai import disease, predict as predict_field
from fastapi.middleware.cors import CORSMiddleware
from model.predict import *
from database.firestore import diseases_ref
from database.memorystore import redis_client
from database.pubsub import publisher, topic_set_predict_crop_yield_advice
import json

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

with open(DISEASE_MODEL_PATH, 'r') as f:
    disease_model = tf.keras.models.model_from_json(f.read())
disease_model.load_weights(DISEASE_WEIGHTS_PATH)

app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    cache_key = "disease:" + predicted_class
    cached_data = redis_client.get(cache_key)

    if cached_data:
        advice = cached_data
    else:
        advice =  disease.advice_disease_generate(predicted_class)
        
        redis_client.set(cache_key, advice, ex=3600)

    return {
        "prediction": predicted_class,
        "raw_prediction": str(prediction),
        "information": information,
        "advice": advice,
    }

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

    result = {
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

    advice_req = PredictCropYieldAdviceRequest(**result)
    cache_key = advice_req.as_redis_key()
    cached_data = redis_client.get(cache_key)

    if not cached_data:
        publisher.publish(topic_set_predict_crop_yield_advice, json.dumps(result).encode('utf-8'))

    return result

@app.post('/predict-crop-yield-advice')
async def predict_crop_yield_advice(req: PredictCropYieldAdviceRequest):
    cache_key = req.as_redis_key()
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return {
            "advice": cached_data,
        }
    
    advice = predict_field.advice_predict_generate(req)

    redis_client.set(cache_key, advice, ex=3600)

    return {
        "advice": advice,
    }