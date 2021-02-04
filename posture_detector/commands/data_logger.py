import io
import json
import time
import click
import serial
import pandas as pd
import datetime as dt
from pynput import keyboard
from posture_detector.utils import constants


ser: serial.Serial
should_stop: int = False
last_pressed_key: str = ''


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
