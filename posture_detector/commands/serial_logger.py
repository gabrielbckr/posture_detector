import datetime as dt
import io
import os
import json
import time
from pathlib import Path
import click
import pandas as pd
import serial
from pynput import keyboard

import constants

ser: serial.Serial
should_stop: int = False
last_pressed_key: str = ''


def get_last_pressed_key():
    global last_pressed_key
    return last_pressed_key


def set_on_keyboard_press_action(key):
    global last_pressed_key, should_stop
    if key == keyboard.Key.esc:
        should_stop = True
        click.echo('End key ESC pressed. Ending jobs.')
        return False
    try:
        last_pressed_key = key
        click.echo(f'Key pressed, new label set: {last_pressed_key}.')
    except AttributeError:
        click.echo('special key {0} pressed'.format(key))


def set_on_keyboard_release_action(key):
    global should_stop
    if key == keyboard.Key.esc:
        should_stop = True
        click.echo('End key ESC pressed. Ending jobs.')
        return False


def start_keyboard_job():
    listener = keyboard.Listener(
        on_press=set_on_keyboard_press_action,
        on_release=set_on_keyboard_release_action)
    listener.start()


def set_file_writer_job(s, file):
    global ser, last_pressed_key, should_stop
    ser = s
    writing_file = io.open(file, 'w+')
    add_header_to_file = True
    while not should_stop:
        ser.flush()
        time.sleep(0.1)
        serial_content = str(ser.read_all().decode('UTF-8'))
        list_of_entries = serial_content.replace('\r\n', '').replace('}{', '}||{').split('||')
        list_of_entries = map(lambda x: parse_json_from_byte_stream(x, last_pressed_key), list_of_entries)
        list_of_entries = list(filter(lambda x: x is not None, list_of_entries))
        pandas_from_content = pd.DataFrame(list_of_entries)
        pandas_from_content.to_csv(writing_file, sep=';', header=add_header_to_file, mode='a')
        add_header_to_file = False


def parse_json_from_byte_stream(entre, last_pressed_key):
    try:
        dict_entre: dict = json.loads(entre)
        dict_entre[constants.label] = last_pressed_key
    except json.decoder.JSONDecodeError:
        return None
    return dict_entre


def get_now_string():
    d = str(dt.datetime.now())
    d = d.replace(' ', '_')
    d = d.replace(':', '_')
    return d


def create_metadata(path):
    df = pd.read_csv(path, sep=';')
    metadata_path = os.getenv(constants.metadata, None)
    if metadata_path is None:
        metadata_path = click.prompt('Enter metadata path: ', type=str)

    column_descriptions = {}
    if click.prompt('Add column labels?', type=str) == 'yes':
        for column in df.columns:
            desc = click.prompt(f'Enter description to column {column}: ', type=str, default='')
            column_descriptions.update({column: desc})

    description = click.prompt("Write the experiment description: ", type=str, default='')

    try:
        if click.prompt('Would you like to replace keys with label values?', type=str) == 'yes':
            keys_descriptions = {}
            values = {}
            for keys in df[constants.label].unique():
                val = click.prompt(f"Enter new value for key '{keys}' of column {constants.label}: ", type=str, default='')
                values.update({keys: val})
                desc = click.prompt(f"Enter description to key '{keys}' of column {constants.label}: ", type=str, default='')
                keys_descriptions.update({keys: desc})
        else:
            keys_descriptions = {}
            for keys in df[constants.label].unique():
                desc = click.prompt(f"Enter description to key '{keys}' of column {constants.label}: ", type=str, default='')
                keys_descriptions.update({keys: desc})
    except KeyError:
        print('Could not access Label')
        print(df.head())
        print(df.columns)

    metadata = {
        'experiment': str(path),
        'description': description,
        'columns_description': column_descriptions,
        'keys_descriptions': keys_descriptions
    }

    with io.open(str(metadata_path), 'r+') as file:
        data = json.loads(''.join(file.readlines()))
    if not isinstance(data, list):
        data = [metadata]
    else:
        data.append(metadata)
    with io.open(str(metadata_path), 'w+') as file:
        json.dump(data, file)


def data_logger_handler(path, port, baud):
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
