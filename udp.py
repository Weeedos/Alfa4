import socket
import json


class Udp:
    def send_udp_broadcast(message, ip, port):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        udp_socket.sendto(message.encode('utf-8'), (ip, port))

        udp_socket.close()

    def handle_udp_response(response):
        try:
            data = json.loads(response)
            return data
        except json.JSONDecodeError:
            pass
        return None
