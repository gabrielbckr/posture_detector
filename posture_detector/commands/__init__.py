import click
from .data_logger import *
from pathlib import Path


@click.group()
def cli_app():
    click.echo('Start cli app')

@cli_app.command()
@click.option('-path', default=f'data/datalog_at_{get_now_string()}', prompt='Path of output file')
@click.option('-port', default='COM0', prompt='Serial port to listen')
@click.option('-baud', default=9600, prompt='Baudrate of serial provaction')
def data_logger(path, port, baud):
    global should_stop, ser
    assert isinstance(path, str)
    assert isinstance(port, str)
    assert isinstance(baud, int)
    ser = serial.Serial(
        port=port,
        baudrate=baud,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )
    start_keyboard_job()
    set_file_writer_job(Path(path))
