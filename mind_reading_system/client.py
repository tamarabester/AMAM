import datetime as dt

from utils import Connection
from thought import Thought

import click

def upload_thought(address, user_id, thought):
    WriteTxtFile = open("write-demo.txt", "w")
    WriteTxtFile.write ("This is new text for the \n demo of writing in text file.")
    WriteTxtFile.close()
    # thought = Thought(user_id, dt.datetime.now(),thought)
    # data = thought.serialize()
    # conn = Connection()
    # conn.socket.connect(address)
    # conn.send(data)
    return 0

# if __name__ == '__main__':
#     cli.main()

