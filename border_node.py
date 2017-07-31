import requests
import gpsd
import time


def connect():
    gpsd.connect()


def post_data(data):
    r = requests.post('https://pagina-do-manas.com/', data=data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        import traceback
        traceback.print_exc()


def read_sensors_data():
    raise NotImplementedError()
    # Lê de nó 802.15.4
    # Lê de velocidade
    gpsd_packet = gpsd.get_current()
    return {
        "seats": 14,
        "weight": 140,
        "speed": 50,
        "position": gpsd_packet.position,
    }


def main():
    connect()
    while True:
        data = read_sensors_data()
        post_data(data)
        time.sleep(5)


if __name__ == '__main__':
    main()
