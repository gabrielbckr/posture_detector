import asyncio
from .serial_logger import *
from pathlib import Path
from posture_detector.api import api
import uvicorn
from posture_detector.models.classification import process_classification as classification_job
from .serial_logger import data_logger_handler
from .http_logger import start_http_logger


@click.group()
def cli_app():
    click.echo('Start cli app')


@cli_app.command()
@click.option('-path', default=f'data/raw/datalog_at_{get_now_string()}', prompt='Path of output file')
@click.option('-port', default='/dev/ttyACM0', prompt='Serial port to listen')
@click.option('-baud', default=9600, prompt='Baudrate of serial provaction')
def serial_logger(path, port, baud):
    data_logger_handler(path, port, baud)


@cli_app.command()
@click.option('-h', '--host', default='192.168.1.239')
@click.option('-p', '--port', default=8686)
def run_api(host, port):
    loop = asyncio.get_event_loop()
    config = uvicorn.Config(app=api, host=host, port=port, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


@cli_app.command()
@click.option('-h', '--host', default='192.168.1.239')
@click.option('-p', '--port', default=8686)
@click.option('-path', default=f'data/raw/datalog_at_{get_now_string()}', prompt='Path of output file')
def http_logger(host, port, path):
    start_http_logger(host, port, path)


@cli_app.command()
@click.argument('training_data_path')
@click.option('--model_path', default='test.pkl')
def process_classification(training_data_path, model_path):
    classification_job(Path(training_data_path).resolve(), model_path)
