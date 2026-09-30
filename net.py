import socket
import libs.belacomInfo as belacomInfo
import json
import sys
import threading
import os

 # Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class net:
    def initialize(self, handler = None):
        try:
            args = sys.argv
            if args[1] == "host":
                port = int(args[2])
                conn = self.listen(port, handler=handler)
            elif args[1] == "join":
                ip = args[2]
                port = int(args[3])
                conn = self.connect(ip, port)
            return conn
        except Exception as e:
            belacomInfo.error(f"Failed to initialize. Error: {e} (Awooga)")

    def connect(self, host, port): # connect to server
        try:
            
            # Connect to the server
            s.connect((host, port))
            
            belacomInfo.info(f"Successfully connected to {host}:{port}")
            return s # return the socket object
        except Exception as e:
            belacomInfo.error(f"Failed to connect to {host}:{port}. Error: {e} (Awooga)")

    def listen(self, port, handler=None, backlog=5): # listen for incoming connections
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("", port))
            server.listen(backlog)
            belacomInfo.info(f"Listening on port {port}...")

            if handler is None:
                conn, addr = server.accept() # accept a connection
                belacomInfo.info(f"Connection established with {addr[0]}:{addr[1]}")
                server.close()
                return conn # return the connection

            def _accept_loop():
                while True:
                    try:
                        conn, addr = server.accept()
                        belacomInfo.info(f"Connection established with {addr[0]}:{addr[1]}")
                        thread = threading.Thread(target=handler, args=(conn, addr, port))
                        thread.start()
                    except Exception as e:
                        belacomInfo.error(f"Failed to accept client on port {port}. Error: {e} (Awooga)")

            thread = threading.Thread(target=_accept_loop)
            thread.start()
            return server

        except Exception as e:
            belacomInfo.error(f"Failed to listen on port {port}. Error: {e} (Awooga)")

    def sendData(self, conn, datum):
        try:
            if isinstance(datum, str):
                data = [len(datum.encode("utf-8")), datum] # encode string to bytes
                conn.sendall(data[0].to_bytes(4, byteorder='big')) # send length of data
                conn.sendall(data[1].encode("utf-8"))
            elif isinstance(datum, (bytes, bytearray)):
                data = [len(datum), datum] # convert bytes to list with length
                conn.sendall(data[0].to_bytes(4, byteorder='big')) # send length of data
                conn.sendall(data[1])
            elif isinstance(datum, int):
                data = [len(str(datum)), str(datum)]
                conn.sendall(data[0].to_bytes(4, byteorder='big')) # send length of data
                conn.sendall(data[1].encode("utf-8"))
            else:
                data = [len(json.dumps(datum).encode("utf-8")), json.dumps(datum)] # convert to JSON
                conn.sendall(data[0].to_bytes(4, byteorder='big')) # send length of data
                conn.sendall(data[1].encode("utf-8"))
            belacomInfo.info(f"Data sent to {conn.getpeername()[0]}:{conn.getpeername()[1]}")
        except Exception as e:
            try:
                target = conn.getpeername()
                belacomInfo.error(f"Failed to send data to {target[0]}:{target[1]}. Error: {e} (Awooga)")
            except Exception:
                belacomInfo.error(f"Failed to send data. Error: {e} (Awooga)")

    def recvExact(self, conn, length):
        data = b''
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data
    def recvData(self, conn):
        try:
            length = int.from_bytes(self.recvExact(conn, 4), byteorder='big') # receive length of data
            data = self.recvExact(conn, length) # receive data
            try:
                data = json.loads(data.decode("utf-8")) # try to decode JSON
            except Exception:
                data = data.decode("utf-8")
            belacomInfo.info(f"Data received from {conn.getpeername()[0]}:{conn.getpeername()[1]}")
            return data # return data
        except Exception as e:
            try:
                target = conn.getpeername()
                belacomInfo.error(f"Failed to receive data from {target[0]}:{target[1]}. Error: {e} (Awooga)")
            except Exception:
                belacomInfo.error(f"Failed to receive data. Error: {e} (Awooga)")

    def portUse(self, port, host=""):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.bind((host, port))
            return False  # port is NOT in use
        except OSError:
            return True   # port IS in use
        finally:
            sock.close()