import datetime as dt
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
        
        # get thought
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



# gets an int that represents the length of the messege we want to get, and the socket through which the connection of the client and server is performed

# returns a byte-array with the messege 

def get_msg(msg_len,c_socket): 
    recived_len = 0
    msg = b''
    while len(msg) < msg_len:
        sub_msg = c_socket.recv(msg_len - recived_len) 
        msg += sub_msg
        recived_len = len(msg)
    return msg

# gets an a local-time array and returns a string of the formatted time

def file_format_time(timeStemp):
    paddeded_time = [f'{num:02}' for num in timeStemp]
    date = paddeded_time[0]+"-"+paddeded_time[1]+"-"+paddeded_time[2]
    time = paddeded_time[3]+"-"+paddeded_time[4]+"-"+paddeded_time[5]
    return f'{date}_{time}.txt'

def run_server(address, data_dir):
    print(f'in run_server with {address} and {data_dir}')
    return 0
    ## setup sockts and connect to a client
    server = socket.socket() 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind(address) 
    server.listen(1000) 

    ## connect to client and recive messege
    while True:
        try:
            client_socket, client_address = server.accept()
            hendler = Handler(client_socket, data_dir)
            hendler.start()
        except Exception as error:
            print(f'ERROR: {error}')
            break

    server.close()
    return 0



def main(argv):

    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address><date_path>')
        return 1

    ip, port_as_string = argv[1].split(":")
    address = (ip, int(port_as_string))

    dir_path = Path(argv[2])

    try:
        run_server(address, dir_path)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))