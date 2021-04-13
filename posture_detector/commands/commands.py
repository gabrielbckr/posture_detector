import asyncio
import click
from .data_logger import *
from pathlib import Path
from posture_detector.api import api
import uvicorn


@click.group()
def cli_app():
    click.echo('Start cli app')


@cli_app.command()
@click.option('-path', default=f'../data/raw/datalog_at_{get_now_string()}', prompt='Path of output file')
@click.option('-port', default='COM0', prompt='Serial port to listen')
@click.option('-baud', default=9600, prompt='Baudrate of serial provaction')
def data_logger(path, port, baud):
    global should_stop, ser
    assert isinstance(path, str)
    assert isinstance(port, str)
    assert isinstance(baud, int)
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baud,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
    except serial.serialutil.SerialException:
        click.echo(f'Unavailable serial port: {port}')
        return
    start_keyboard_job()
    set_file_writer_job(ser, Path(path))

    should_create_metadata = click.prompt('Do you want to create metadata?', type=bool)
    if should_create_metadata:
        create_metadata(Path(path))


@cli_app.command()
def run_api():
    loop = asyncio.get_event_loop()
    config = uvicorn.Config(app=api, host='192.168.1.239', port=8686, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())
