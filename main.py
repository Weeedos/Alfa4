import socket
import json
import time


def send_udp_broadcast(message, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.sendto(message.encode('utf-8'), ('<broadcast>', port))


def handle_discovery_response(response, my_peer_id):
    try:
        data = json.loads(response)
        if data.get('status') == 'ok' and data.get('peer_id') != my_peer_id:
            print(f"Discovered peer: {data['peer_id']} at {data['ip']}")
    except json.JSONDecodeError:
        print("Invalid JSON format in discovery response")


my_peer_id = "testing-peer1"
udp_port = 9876

while True:
    discovery_query = {"command": "hello", "peer_id": my_peer_id, "ip": socket.gethostbyname(socket.gethostname())}
    send_udp_broadcast(json.dumps(discovery_query), udp_port)

    time.sleep(5)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(1)

    try:
        while True:
            response, address = udp_socket.recvfrom(1024)
            response = response.decode('utf-8')
            handle_discovery_response(response, my_peer_id)
    except socket.timeout:
        pass

    udp_socket.close()