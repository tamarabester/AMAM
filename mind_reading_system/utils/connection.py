import socket

class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        peer = self.socket.getpeername()
        me = self.socket.getsockname()
        return f'<Connection from {me[0]}:{me[1]} to {peer[0]}:{peer[1]}>'

    def send(self, data):
        self.socket.sendall(data)
    
    def close(self):
        self.socket.close()

    def receive(self, size):
        recived_size = 0
        msg = b''
        while recived_size < size:
            sub_msg = self.socket.recv(size)
            if not sub_msg:
                break;
            msg += sub_msg
            recived_size += len(sub_msg)
        if recived_size < size:
            raise(ConnectionAbortedError)
        return msg

    def __enter__(self):
        return self
    
    def __exit__(self, exception, error, traceback):
        self.socket.close()

    def connect(host, port):
        conn = Connection(socket.socket())
        conn.socket.connect((host,port))
        return conn
