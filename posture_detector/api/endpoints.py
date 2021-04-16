from fastapi import FastAPI, Request
import pandas as pd


api = FastAPI()


@api.post("/data/{device_id}")
async def post_data(device_id: int, payload: Request):
    content = await payload.json()
    pd.DataFrame(content.values()).T\
        .rename(columns=dict(enumerate(content.keys())))\
        .to_csv('../data/raw/session0', mode='a', header=False)
    print(content)
    return {"Hello": f"World, {device_id}"}


@api.get("/data/{device_id}/")
async def get_data(device_id: int, content: Request):
    print(await content.json())
    return {"Hello": f"World, {device_id}"}


@api.get("/classification/{device_id}")
async def get_classification():
    return {'Hello': 'World'}
