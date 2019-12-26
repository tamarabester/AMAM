import click

from client import upload_thought
from server import run_server
from webserver import run_webserver
import traceback

def ip_validator(s):
    if s == "localhost":
        return True
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def port_validator(port):
    if not port.isdigit():
        return False
    return int(port)>0 & int(port)<65000

def validate_address(ctx, param, address):
    try:
        ip, port = address.split(':')
        if (port_validator(port) & ip_validator(ip)):
           return address
        raise Exception()

    except Exception as ex:
        raise click.BadParameter('ADDRESS needs to be in format "ip:port"')



def tupled_address(string_address):
    try:
        address = string_address.split(":")
        address[1] = int(address[1])
        return tuple(address)
    except Exception as ex:
        raise Exception(f'Failed Parsing Address: "{string_address}". {ex}.')


@click.group()
def main():
    pass



@main.command('upload_thought', short_help="lala")
@click.option('--address', callback=validate_address)
@click.argument('address',type=str)
@click.argument('user',type=int)
@click.argument('thought',type=str)
def upload(address, user, thought):
    """ This is something"""
    try:    
        upload_thought(tupled_address(address), int(user), thought)
    except Exception as error:
        click.echo(f'ERROR: {error}')
        click.echo(f'ERROR: {error.__traceback__}')
        #traceback.print_tb((error.__traceback__))
        return 1


# @cli.command
# def run(address, data):
#     ip, port_as_string = address.split(":")
#     address = (ip, int(port_as_string))
#     dir_path = Path(data)
#     ## setup sockts and connect to a client
#     server = socket.socket() 
#     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
#     server.bind(address) 
#     server.listen(1000) 

#     ## connect to client and recive messege
#     while True:
#         try:
#             client_socket, client_address = server.accept()
#             hendler = Handler(client_socket, data)
#             hendler.start()
#         except Exception as error:
#             print(f'ERROR: {error}')
#             break
#     server.close()
#     return 0

if __name__ == '__main__':
    main()