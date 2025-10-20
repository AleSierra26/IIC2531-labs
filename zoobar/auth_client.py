from debug import *
import rpclib
import sys, os
sys.path.append(os.getcwd())
import readconf

def _connect():
    conf = readconf.read_conf ()
    host = ('10.1.3.4', 8081)
    return rpclib.client_connect(host)

def login(username, password) :
    with _connect() as c:
        return c.call('login', username=username, password=password)
def register(username, password) :
    with _connect() as c:
        return c.call('register',username=username,password=password)
def check_token(username, token) :
    with _connect() as c:
        return c.call('check_token', username=username, token=token)