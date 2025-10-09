from debug import *
from zoodb import *
import rpclib
import sys

sys.path.append(os.getcwd())
import readconf

def _get_auth_host():
    conf = readconf.read_conf()
    return conf.lookup_host('auth')

def login(username, password):
    host = _get_auth_host()
    with rpclib.client_connect(host) as c:
        return c.call('login', username=username, password=password)

def register(username, password):
    host = _get_auth_host()
    with rpclib.client_connect(host) as c:
        return c.call('register', username=username, password=password)

def check_token(username, token):
    host = _get_auth_host()
    with rpclib.client_connect(host) as c:
        return c.call('check_token', username=username, token=token)
