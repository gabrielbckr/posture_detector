from fastapi import FastAPI, Request
import pandas as pd
from posture_detector.api import handlers


api = FastAPI()


@api.post("/data/{device_id}")
async def post_data(device_id: int, payload: Request):
    await handlers.post_data_handler(payload)
    return {"Hello": f"World, {device_id}"}


@api.get("/data/{device_id}/")
async def get_data(device_id: int, content: Request):
    print(await content.json())
    return {"Hello": f"World, {device_id}"}


@api.get("/classification/{device_id}")
async def get_classification():
    return {'Hello': 'World'}
