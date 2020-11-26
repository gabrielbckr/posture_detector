import io
import time
import click
import serial
import datetime as dt
from pynput import keyboard


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
        print('special key {0} pressed'.format(key))


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


def set_file_writer_job(file):
    global ser, last_pressed_key, should_stop
    writing_file = io.open(file, 'w+')
    while not should_stop:
        ser.flush()
        time.sleep(0.1)
        serial_content = str(ser.read_all().decode('UTF-8'))
        serial_content = f', {last_pressed_key}\n'.join(serial_content.split())
        writing_file.write(serial_content)


def get_now_string():
    d = str(dt.datetime.now())
    d = d.replace(' ', '_')
    d = d.replace(':', '_')
    return d




