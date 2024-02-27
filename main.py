import socket
import json
import time
from udp import Udp


def main():
    udp = Udp()
    peer_id = "vosol-peer"
    udp_ip = "172.31.255.255"
    udp_port = 9876

    while True:
        query = {"command": "hello", "peer_id": peer_id}
        query_message = json.dumps(query)
        udp.send_udp_broadcast(query_message, udp_ip, udp_port)

        responses = []
        start_time = time.time()

        while time.time() - start_time < 5:
            try:
                udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_socket.settimeout(1)
                udp_socket.bind(('', udp_port))
                response, _ = udp_socket.recvfrom(1024)

                peer_response = udp.handle_udp_response(response.decode('utf-8'))
                if peer_response and 'peer_id' in peer_response and peer_response['peer_id'] != peer_id:
                    responses.append(peer_response)
                    print(peer_response)

            except socket.timeout:
                pass
            finally:
                udp_socket.close()


if __name__ == "__main__":
    main()
