from pathlib import Path
import threading
import time
import socket

class Handler(threading.Thread):
    lock = threading.Lock()
    def __init__(self, connection, dir_path):
        super().__init__()
        self.connection = connection
        self.path = dir_path

    def run(self):
        self.connection
        userID = int.from_bytes(get_msg(8,self.connection),byteorder='little')
        timeStemp = time.localtime(int.from_bytes(get_msg(8,self.connection),byteorder='little'))
        msgLen = int.from_bytes(get_msg(4,self.connection),byteorder='little')
        msg = get_msg(msgLen,self.connection).decode()

        folder_path = self.path / str(userID)
        full_path = folder_path / file_format_time(timeStemp)


        # write thought to file
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
        return

# gets an int that represents the length of the messege we want to get, 
# and the socket through which the connection of the client and server is performed
# returns a byte-array with the messege 
def get_msg(msg_len,c_socket): 
    recived_len = 0
    msg = b''
    while len(msg) < msg_len:
        sub_msg = c_socket.recv(msg_len - recived_len) 
        msg += sub_msg
        recived_len = len(msg)
    return msg


def file_format_time(timeStemp):
    paddeded_time = [f'{num:02}' for num in timeStemp]
    date = paddeded_time[0]+"-"+paddeded_time[1]+"-"+paddeded_time[2]
    time = paddeded_time[3]+"-"+paddeded_time[4]+"-"+paddeded_time[5]
    return f'{date}_{time}.txt'

def run_server():
    pass

if __name__ == '__main__':
    cli.main()
