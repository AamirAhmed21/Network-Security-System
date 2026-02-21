from flask import Flask, render_template, request
import os
import sys

from gql import Client
import pymongo
from networksecurity.logging import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.pipeline.training_pipeline import TrainingPipeline 

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from fastapi.responses import Response 
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from fastapi.templating import Jinja2Templates

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
templates = Jinja2Templates(directory="./templates")

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
print(mongo_uri)

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def root():
    return RedirectResponse(url="/docs")

@app.get("/train", tags=["training"])
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response(content="Training pipeline started successfully", media_type="text/plain")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

@app.get("/predict", tags=["prediction"])
async def predict_form(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})

@app.post("/predict", tags=["prediction"])
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        print(df.iloc[0])
        predictions = network_model.predict(df)
        print(predictions)
        df['prediction_column'] = predictions
        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)