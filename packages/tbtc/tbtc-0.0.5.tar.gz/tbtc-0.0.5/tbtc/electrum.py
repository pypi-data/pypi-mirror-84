import socket
import ssl
import json
import time
import errno

class Electrum():
    def __init__(self, host, port, protocol, timeout=5):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.timeout = timeout
        self.connection = None
        self._connect()

    def _connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(self.timeout)
        if self.protocol=="ssl":
            self.connection = ssl.wrap_socket(self.connection)
        self.connection.connect((self.host, self.port))

    def _receive(self):
        buffer = self.connection.recv(1024)
        r = json.loads(buffer)
        return r

    def send(self, method, params):
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": int(time.time()*1000),
                "method": method,
                "params": params
            }
        ) + '\n'
        payload = payload.encode()
        self.connection.send(payload)
        return self._receive()