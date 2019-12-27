import datetime as dt
from pathlib import Path
import threading

from ..utils.connection import Connection

class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, dir_path):
        super().__init__()
        self.connection = connection
        self.path = dir_path

    def run(self):     
        # get thought
        userID = int.from_bytes(self.connection.recive(8), byteorder='little')
        timeStemp = dt.datetime.fromtimestamp(int.from_bytes(self.connection.recive(8), byteorder='little'))
        msglen = int.from_bytes(self.connection.recive(4), byteorder='little')
        msg = self.connection.recive(msglen).decode()

        folder_path = self.path / str(userID)
        full_path = folder_path / timeStemp.strftime('%Y-%m-%d_%H-%M-%S')

        # write thought tos file
        self.lock.acquire()
        if not folder_path.exists():
            folder_path.mkdir(parents=True) 

        if not full_path.is_file():
            full_path.touch()
            full_path.write_text(msg)

        else:
            with open(str(full_path), "a") as f:
                f.write('\n'+msg)

        self.lock.release()
        self.connection.close()
        return 0


