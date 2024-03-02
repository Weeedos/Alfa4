import socket
import json

"""
TCP Peer Communication Module

This module defines the `TcpPeer` class, which facilitates communication between peers over TCP.

Class:
- TcpPeer: Manages the TCP connection, performs handshakes, sends and receives chat messages.

Methods:
- __init__(self, peer_id, tcp_port): Initializes a TcpPeer instance with a peer ID and TCP port.
- establish_tcp_connection(self, peer_ip): Establishes a TCP connection with the specified peer IP.
- perform_handshake(self, tcp_socket): Initiates a handshake by sending a "hello" command and processes the response.
- send_chat_message(self, tcp_socket, message_id, message): Sends a new chat message to the connected peer.
- receive_chat_message(self, tcp_socket): Receives and processes incoming chat messages.
"""

class TcpPeer:
    def __init__(self, peer_id, tcp_port):
        """
            Initializes a TcpPeer instance.

            :param: ID of the peer.
            :param: TCP port for communication.
        """

        self.peer_id = peer_id
        self.tcp_port = tcp_port
        self.messages = {}

    def establish_tcp_connection(self, peer_ip):
        """
            Establishes a TCP connection with the specified peer IP.

            :param: IP address of the peer to connect to.
            :return: Established TCP socket.
        """

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((peer_ip, self.tcp_port))
        return tcp_socket

    def perform_handshake(self, tcp_socket):
        """
            Initiates a handshake by sending a "hello" command and processes the response.

            :param: Established TCP socket.
            :return: Handshake response from the peer.
        """

        handshake_message = {"command": "hello", "peer_id": self.peer_id}
        tcp_socket.send(json.dumps(handshake_message).encode('utf-8'))
        response = tcp_socket.recv(10000000000).decode('utf-8')
        handshake_response = json.loads(response)
        if 'messages' in handshake_response:
            self.messages.update(handshake_response['messages'])
        return handshake_response

    def send_chat_message(self, tcp_socket, message_id, message):
        """
            Sends a new chat message to the connected peer.

            :param: Established TCP socket.
            :param: ID of the new message.
            :param: Content of the new message.
        """

        new_message = {"command": "new_message", "message_id": message_id, "message": message}
        tcp_socket.send(json.dumps(new_message).encode('utf-8'))

    def receive_chat_message(self, tcp_socket):
        """
            Receives and processes incoming chat messages.

            :param: Established TCP socket.
            :return: Received chat message.
        """
        response = tcp_socket.recv(10000000000).decode('utf-8')
        received_message = json.loads(response)
        if 'message_id' in received_message:
            self.messages[received_message['message_id']] = received_message
        return received_message
