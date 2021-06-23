from fastapi import FastAPI, Request
import pandas as pd
from .serial_logger import start_keyboard_job, should_stop, last_pressed_key, get_last_pressed_key
from posture_detector.constants.columns import Record
import asyncio
import uvicorn
from pathlib import Path


logger_api = FastAPI()

LOG_FILE: str = ''


@logger_api.post("/data/{device_id}")
async def post_data(device_id: int, payload: Request):
    write_sample(await payload.json())


def write_sample(sample):
    global LOG_FILE
    p = str(get_last_pressed_key())
    last_pressed_key = p[1] if len(p) > 2 else None
    sample.update({Record.Label: last_pressed_key})

    data = pd.DataFrame([sample])
    print(data[['FlS', 'Label']])
    data.to_csv(LOG_FILE, mode='a', header=False, index=False)


def set_log_file(file: str):
    global LOG_FILE
    LOG_FILE = Path(__file__).parents[2].joinpath(file).resolve()
    pd.DataFrame(columns=[
            Record.Ax, Record.Ay, Record.Az,
            Record.T,
            Record.Gx, Record.Gy, Record.Gz,
            Record.Flex, Record.Label
        ]).to_csv(LOG_FILE, index=False)


def start_http_logger(host, port, path):
    set_log_file(str(path))
    loop = asyncio.get_event_loop()
    config = uvicorn.Config(app=logger_api, host=host, port=port, loop=loop)
    server = uvicorn.Server(config)
    start_keyboard_job()
    loop.run_until_complete(server.serve())
