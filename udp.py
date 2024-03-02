import socket
import json

"""
UDP Communication Module

This module defines the `Udp` class, which handles UDP communication, including sending broadcast messages
and processing UDP responses.

Class:
- Udp: Manages UDP communication, including sending broadcast messages and processing UDP responses.

Methods:
- send_udp_broadcast(self, message, ip, port): Sends a UDP broadcast message to the specified IP and port.
- handle_udp_response(self, response): Processes and decodes a received UDP response.
"""

class Udp:
    def send_udp_broadcast(self, message, ip, port):
        """
            Sends a UDP broadcast message to the specified IP and port.

            :param: Message to be broadcasted.
            :param: IP address for broadcasting.
            :param: UDP port for communication.
        """

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        udp_socket.sendto(message.encode('utf-8'), (ip, port))

        udp_socket.close()

    def handle_udp_response(self, response):
        """
            Processes and decodes a received UDP response.

            :param: UDP response message.
            :return: Decoded data from the response or None if decoding fails.
        """
        try:
            data = json.loads(response)
            return data
        except json.JSONDecodeError:
            pass
        return None
