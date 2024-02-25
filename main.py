import socket
import json
import time


def send_udp_broadcast(message, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(message.encode('utf-8'), ('<broadcast>', port))


def main():
    try:
        peer_id = "testing-peer1"
        port = 9876

        while True:
            query = {"command": "hello", "peer_id": peer_id}
            query_str = json.dumps(query)
            send_udp_broadcast(query_str, port)

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind(('', port))
                s.settimeout(5)

                while True:
                    try:
                        data, addr = s.recvfrom(1024)
                        response = json.loads(data.decode('utf-8'))

                        if response.get("peer_id") != peer_id:
                            print(f"A: {json.dumps(response)}")
                    except socket.timeout:
                        break
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()