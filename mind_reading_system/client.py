
#from connection import Connection
#from thought import Thought
from cli import CommandLineInterface

import datetime as dt

cli = CommandLineInterface()

# connection should be a Connection type object that its socket already has an address
def upload_thought(address, user_id, thought):
    thought = Thought(user_id, dt.datetime.now(),thought)
    data = thought.serialize()
    conn = Connection()
    conn.socket.connect(address)
    conn.send(data)
    return 0

@cli.command
def upload(address, user, thought):
    try:
        address = address.split(":")
        address[1] = int(address[1])
        address = tuple(address)
        upload_thought(address, int(user), thought)
        print('done')

    except Exception as error:
        print(f'ERROR: {error}')
        return 1

if __name__ == '__main__':
    cli.main()

