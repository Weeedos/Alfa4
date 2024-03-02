# Peer Communication System

## Overview

This project consists of two Python modules (`tcp.py` and `udp.py`) and a main script (`main.py`) designed for peer communication over TCP and UDP protocols.

### `main.py`

The `main.py` script is the central component that orchestrates the discovery of peers through UDP broadcasts and establishes persistent TCP connections with discovered peers.

#### Usage

1. **Configuration:** Peer information such as ID, UDP IP address, and port is read from the `./cfg/config.ini` configuration file.

2. **Peer Discovery:** The script sends a "hello" command as a UDP broadcast to discover other peers on the network.

3. **TCP Connection:** For each responding peer, the script attempts to establish a TCP connection and perform a handshake.

4. **Chat History:** If the TCP connection is successful, the script prints the chat history with the connected peer.

### `tcp.py`

The `tcp.py` module contains the `TcpPeer` class, which manages the TCP communication between peers.

#### Class: `TcpPeer`

- `__init__(self, peer_id, tcp_port)`: Initializes a `TcpPeer` instance with a peer ID and TCP port.

- `establish_tcp_connection(self, peer_ip)`: Establishes a TCP connection with the specified peer IP.

- `perform_handshake(self, tcp_socket)`: Initiates a handshake by sending a "hello" command and processes the response.

- `send_chat_message(self, tcp_socket, message_id, message)`: Sends a new chat message to the connected peer.

- `receive_chat_message(self, tcp_socket)`: Receives and processes incoming chat messages.

### `udp.py`

The `udp.py` module contains the `Udp` class, which handles UDP communication, including sending broadcast messages and processing UDP responses.

#### Class: `Udp`

- `send_udp_broadcast(self, message, ip, port)`: Sends a UDP broadcast message to the specified IP and port.

- `handle_udp_response(self, response)`: Processes and decodes a received UDP response.
