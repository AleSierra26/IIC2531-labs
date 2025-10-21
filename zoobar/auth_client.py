from debug import *
import rpclib
import sys, os
sys.path.append(os.getcwd())
import readconf


def login(username, password) :
    host = readconf.read_conf().lookup_host('auth')
    kwargs = {'username': username, 'password': password}
    return rpclib.client_connect(('10.1.3.4', 8081)).call('login', **kwargs)
def register(username, password) :
    host = readconf.read_conf().lookup_host('auth')
    kwargs = {'username': username, 'password': password}
    return rpclib.client_connect(('10.1.3.4', 8081)).call('register', **kwargs)
def check_token(username, token) :
    host = readconf.read_conf().lookup_host('auth')
    kwargs = {'username': username, 'token': token}
    return rpclib.client_connect(('10.1.3.4', 8081)).call('check_token', **kwargs)
    
