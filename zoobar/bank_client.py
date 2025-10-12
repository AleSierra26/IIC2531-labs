from debug import *
import rpclib
import sys, os
sys.path.append(os.getcwd())
import readconf

def transfer(sender,recipient,zoobars):
    host = readconf.read_conf().lookup_host('bank')
    with rpclib.client_connect(host) as c:
        kwargs = {'sender':sender,'recipient':recipient,'zoobars':zoobars}
        ret = c.call('transfer',**kwargs)
        return ret

def balance(username):
    host = readconf.read_conf().lookup_host('bank')
    with rpclib.client_connect(host) as c:
        kwargs = {'username':username}
        ret = c.call('balance',**kwargs)
        return ret

def get_log(username):
    host = readconf.read_conf().lookup_host('bank')
    with rpclib.client_connect(host) as c:
        kwargs = {'username':username}
        ret = c.call('get_log',**kwargs)
        return ret

def check_in(username):
    host = readconf.read_conf().lookup_host('bank')
    with rpclib.client_connect(host) as c:
        kwargs = {'username':username}
        ret = c.call('check_in',**kwargs)
        return ret