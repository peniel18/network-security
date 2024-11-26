import sys
import os 
import certifi 
from dotenv import load_dotenv 
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 
from networksecurity.pipelines.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates


load_dotenv()
MANGO_DB_URI = os.getenv("MANGO_DB_URI")
ca = certifi.where()
print(MANGO_DB_URI)


# mongodb client 
client = pymongo.MongoClient(MANGO_DB_URI, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True, 
    allow_methods = ["*"], 
    allow_headers = ["*"]
)

templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train") 
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.runPipeline()
        return Response("Training Successful")
    except Exception as e: 
        raise NetworkSecurityException(e, sys)
    
@app.get("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try: 
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        networkModel = NetworkModel(preprocessor=preprocessor, model=model)
        yHat = networkModel.predict(df)
        df["predicted_column"] = yHat 
        df.to_csv("predictions/output.csv")
        table_html = df.to_html(classes="tabel table-striped")
        context = {
            "request" : request, 
            "tabel" : table_html
        }
        return templates.TemplateResponse("table.html", context)
    except Exception as e: 
        raise NetworkSecurityException(e, sys)





if __name__ == "__main__":
    run(app, host="localhost", port=8000)
