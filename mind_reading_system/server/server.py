
from ..utils.connection import Connection
from .hendler import Handler
from ..utils.listener import Listener

def run_server(address, data_path):
    listener = listener(*address)
    with listener:
        while True:
            connection = listener.accept()
            hendler = Handler(connection, data_path)
            hendler.start()
    return 0