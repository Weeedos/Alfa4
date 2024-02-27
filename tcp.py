import socket
import json


class TcpPeer:
    def __init__(self, peer_id, tcp_port):
        self.peer_id = peer_id
        self.tcp_port = tcp_port
        self.messages = {}

    def establish_tcp_connection(self, peer_ip):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((peer_ip, self.tcp_port))
        return tcp_socket

    def perform_handshake(self, tcp_socket):
        handshake_message = {"command": "hello", "peer_id": self.peer_id}
        tcp_socket.send(json.dumps(handshake_message).encode('utf-8'))
        response = tcp_socket.recv(65536).decode('utf-8')
        print(f"Odpověď na handshake: {response}")
        handshake_response = json.loads(response)
        if 'messages' in handshake_response:
            self.messages.update(handshake_response['messages'])
        return handshake_response

    def send_chat_message(self, tcp_socket, message_id, message):
        new_message = {"command": "new_message", "message_id": message_id, "message": message}
        tcp_socket.send(json.dumps(new_message).encode('utf-8'))

    def receive_chat_message(self, tcp_socket):
        response = tcp_socket.recv(1024).decode('utf-8')
        received_message = json.loads(response)
        if 'message_id' in received_message:
            self.messages[received_message['message_id']] = received_message
        return received_message
