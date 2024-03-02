import socket
import json
import time

from tcp import TcpPeer
from udp import Udp


def main():
    udp = Udp()
    peer_id = "vosol-peer"
    udp_ip = "172.31.255.255"
    port = 9876

    while True:
        query = {"command": "hello", "peer_id": peer_id}
        query_message = json.dumps(query)
        udp.send_udp_broadcast(query_message, udp_ip, port)

        responses = []
        start_time = time.time()

        while time.time() - start_time < 5:
            try:
                udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_socket.settimeout(1)
                udp_socket.bind(('', port))
                response, address = udp_socket.recvfrom(1024)

                peer_ip = address[0]

                peer_response = udp.handle_udp_response(response.decode('utf-8'))
                if peer_response and 'peer_id' in peer_response and peer_response['peer_id'] != peer_id:
                    responses.append(peer_response)
                    print(peer_response)

                    tcp_peer = TcpPeer(peer_id, port)
                    try:
                        tcp_socket = tcp_peer.establish_tcp_connection(peer_ip, timeout=5.0)
                    except TimeoutError:
                        print(f"Connection to {peer_response['peer_id']} timed out. Retrying...")
                        continue
                    handshake_response = tcp_peer.perform_handshake(tcp_socket)

                    if handshake_response and handshake_response.get('status') == 'ok':
                        print(f"Navázáno trvalé spojení s {peer_response['peer_id']}")
                        chat_history = tcp_peer.messages
                        print(f"Historie chatu s {peer_response['peer_id']}: {chat_history}")

                        """
                        timestamp = str(int(time.time() * 1000))
                        message_id = f"{timestamp}"
                        message = "Test"
                        tcp_peer.send_chat_message(tcp_socket, message_id, message)
                        

                        received_message = tcp_peer.receive_chat_message(tcp_socket)
                        print(f"Přijata nová zpráva od {peer_response['peer_id']}: {received_message}")
                        """

                        tcp_socket.close()

            except socket.timeout:
                pass
            except json.JSONDecodeError as err:
                print(err)
            finally:
                udp_socket.close()


if __name__ == "__main__":
    main()
