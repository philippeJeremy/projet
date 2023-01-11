import mlflow 
import joblib
import uvicorn
import json
import numpy as np
import pandas as pd 

from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile

# mlflow.set_tracking_uri("https://model-vin.herokuapp.com/")

target = open("target.json")
target = json.load(target)


description = """
Welcome to  API.  Try it out 🕹️

## Introduction Endpoints

"""
tags_metadata = [
    {
        "name": "Introduction Endpoints",
        "description": "Simple endpoints to try out!",
    },
    {
        "name": "Machine Learning",
        "description": "Prediction price."
    }
]

app = FastAPI(
    title="On boit quoi avec ça ?",
    description=description,
    version="0.1",
    contact={
        "name": "On boit quoi avec ça ?",
        "url": "https://model-vin.herokuapp.com/",
    },
    openapi_tags=tags_metadata
)
class PredictionFeatures(BaseModel):
    plat: str = "osso buco"
    

@app.get("/", tags=["Introduction Endpoints"])
async def index():
    """
    Renvoie simplement un message de bienvenue !
    """
    message = "Bonjour! Ce `/` est le point de terminaison le plus simple et par défaut. Si vous voulez en savoir plus, consultez la documentation de l'API sur `/docs`"
    return message

@app.post("/predict", tags=["Machine Learning"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Prediction du prix à la journée. 
    """
    
    plat = pd.DataFrame(dict(predictionFeatures), index=[0])

    # plat = tf.data.Dataset.from_tensor_slices(plat)
                            
    logged_model = 'runs:/2b9989c49d6c44628a0a49b77a512e71/./models.joblib'

    # logged_model = tf.keras.models.load_model('s3://projet-vin/model/2/e1fd7b75c49b40c8bf71c150c7508b32/artifacts/vin/path.h5', custom_objects={'KerasLayer':hub.KerasLayer})
    # my_reloaded_model = mlflow.pyfunc.load_model(model_uri='runs:/e1fd7b75c49b40c8bf71c150c7508b32/./models.joblib', )
    #  ('s3://projet-vin/model/2/e1fd7b75c49b40c8bf71c150c7508b32/artifacts/vin/path.h5')
    # loaded_model = joblib.load('../projet/api/model.joblib')
    logged_model = mlflow.pyfunc.load_model(logged_model)

    prediction = logged_model.predict(plat)


    # response = np.argmax(prediction)
    # print(type(prediction))

    response = prediction.values.tolist()[0]

    max_value = max(response)
    max_index = response.index(max_value)
    
    # print(response)

    return max_index

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
