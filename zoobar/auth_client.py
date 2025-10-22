# zoobar/auth_client.py
from debug import *
import rpclib
import sys, os
sys.path.append(os.getcwd())
import readconf

def _connect_to_auth():
    host = readconf.read_conf().lookup_host('auth')
    if isinstance(host, tuple) or isinstance(host, list):
        return rpclib.client_connect((host[0], int(host[1])))
    if isinstance(host, str) and ':' in host:
        ip, port = host.split(':', 1)
        return rpclib.client_connect((ip, int(port)))
    return rpclib.client_connect(('127.0.0.1', 8081))

def login(username, password):
    kwargs = {'username': username, 'password': password}
    try:
        conn = _connect_to_auth()
        return conn.call('login', **kwargs)
    except Exception as e:
        log("auth_client.login: RPC error: %r" % (e,))
        return None

def register(username, password):
    kwargs = {'username': username, 'password': password}
    try:
        conn = _connect_to_auth()
        return conn.call('register', **kwargs)
    except Exception as e:
        log("auth_client.register: RPC error: %r" % (e,))
        return None

def check_token(username, token):
    kwargs = {'username': username, 'token': token}
    try:
        conn = _connect_to_auth()
        return conn.call('check_token', **kwargs)
    except Exception as e:
        log("auth_client.check_token: RPC error: %r" % (e,))
        return False
