from fastapi import FastAPI, HTTPException
import pymysql
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# import boto3
import json


app = FastAPI()

app.mount("/score_ui/static", StaticFiles(directory="static"), name="static")

# Database Connection (MySQL example)
DB_CONFIG = {
    "host": "localhost",
    "user": "grashin",
    "password": "Geeta#9320",
    "database": "score_database",
}

@app.get("/")
async def read_root():
    return FileResponse('index.html')

def get_db_data(unique_id):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT score FROM score_details WHERE unique_id = %s", (unique_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AWS S3 Configuration
# S3_BUCKET_NAME = "your-bucket-name"
# s3_client = boto3.client("s3")

# def get_s3_data(unique_id):
#     try:
#         response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=f"{unique_id}.json")
#         return json.loads(response["Body"].read().decode("utf-8"))
#     except Exception as e:
#         return None  # Handle missing files gracefully

@app.get("/fetch/{unique_id}")

def fetch_data(unique_id: str):
    db_result = get_db_data(unique_id)
    #s3_result = get_s3_data(unique_id)
    
    if db_result : #or s3_result
        return {"db_value": db_result}  #, "s3_value": s3_result}
    
    raise HTTPException(status_code=404, detail="Data not found")
