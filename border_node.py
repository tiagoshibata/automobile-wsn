from flask import Flask, request
import requests
import gpsd
import serial
import threading
import time


measurements = {}
serial = serial.Serial('/dev/ttyUSB0')
gpsd.connect()
app = Flask(__name__)


def seats_monitor():
    while True:
        data = serial.readline().rstrip()
        if data:
            measurements['seats'] = 'True' in data


@app.route('/', methods=['POST'])
def get_measurements():
    measurements.update(request.form)
    return 'OK'


def speed_monitor():
    app.run('0.0.0.0')


def post_data(data):
    r = requests.post('https://api-labredes.herokuapp.com/data', data=data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        import traceback
        traceback.print_exc()


def read_sensors_data():
    gpsd_packet = gpsd.get_current()
    position = gpsd_packet.position
    return {
        "position": position,
        **measurements,
    }


def main():
    threading.Thread(target=seats_monitor).start()
    threading.Thread(target=speed_monitor).start()
    while True:
        data = read_sensors_data()
        print('Posting {}'.format(data))
        post_data(data)
        time.sleep(5)


if __name__ == '__main__':
    main()
