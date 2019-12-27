import click
from pathlib import Path
import traceback

from .client import upload_thought
from .server import run_server
from .webserver import run_webserver

########################## parameter validators ##########################

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

##########################################################################

############################## helpers ###################################

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


if __name__ == '__main__':
    main()

##########################################################################

################################# cli ####################################

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
        return 1


@main.command('run_server', short_help="tata")
@click.option('--address', callback=validate_address)
@click.argument('address',type=str)
@click.argument('storing_path', type=click.Path(exists=True))
def initiate_server(address, storing_path):
    """ Initiates a server in the given ADDRESS, that stores it's data at the given STORING_PATH"""
    try:    
        run_server(tupled_address(address), Path(storing_path))
        print("here")
    except Exception as error:
        click.echo(f'ERROR: {error}')
        click.echo(f'ERROR: {error.__traceback__}')
        return 1


@main.command('run_server', short_help="tata")
@click.option('--address', callback=validate_address)
@click.argument('address',type=str)
@click.argument('storing_path', type=click.Path(exists=True))
def initiate_server(address, storing_path):
    """ Initiates a server in the given ADDRESS, that stores it's data at the given STORING_PATH"""
    try:    
        run_webserver(tupled_address(address), Path(storing_path))
        print("here")
    except Exception as error:
        click.echo(f'ERROR: {error}')
        click.echo(f'ERROR: {error.__traceback__}')
        return 1

##########################################################################