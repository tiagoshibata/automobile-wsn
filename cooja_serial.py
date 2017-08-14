import serial
import socket


class SlipRadio():
    def __init__(self):
        self.conn = socket.create_connection(('localhost', 60001))

    def set_channel(self, channel):
        self.conn.send(b'!C' + bytes([channel]))
        self.conn.send(b'?C')

    def set_mac(connection, mac):
        assert(len(mac) == 8)
        connection.send(bytes('!M', mac))

    def recv(self):
        return self.conn.recv(4096)


def connect_serial():
    serial_port = serial.Serial('/dev/ttyUSB0')
    print('Connected to serial {}'.format(serial_port.name))
    return serial_port


def main():
    serial_port = connect_serial()
    cooja_socket = SlipRadio()
    cooja_socket.set_channel(7)
    while True:
        data = cooja_socket.recv()
        if not data:
            print('Disconnected from cooja, exiting')
            break
        serial_port.write(data)
    serial_port.close()
    cooja_socket.close()


if __name__ == '__main__':
    main()
