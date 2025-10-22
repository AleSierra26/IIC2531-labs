# zoobar/bank_client.py
from debug import *
import rpclib
import sys, os
sys.path.append(os.getcwd())
import readconf

def _connect_to_bank():
    host = readconf.read_conf().lookup_host('bank')
    if isinstance(host, (tuple, list)):
        return rpclib.client_connect((host[0], int(host[1])))
    if isinstance(host, str) and ':' in host:
        ip, port = host.split(':', 1)
        return rpclib.client_connect((ip, int(port)))
    return rpclib.client_connect(('127.0.0.1', 8081))

def balance(username):
    try:
        conn = _connect_to_bank()
        return conn.call('balance', username=username)
    except Exception as e:
        debug("bank_client.balance: RPC error: %r" % (e,))
        return None

def create_account(username, initial_balance=10):
    try:
        conn = _connect_to_bank()
        return conn.call('create_account', username=username, initial_balance=initial_balance)
    except Exception as e:
        debug("bank_client.create_account: RPC error: %r" % (e,))
        return False

def transfer(sender, recipient, zoobars, token):
    try:
        conn = _connect_to_bank()
        return conn.call('transfer', sender=sender, recipient=recipient, zoobars=zoobars, token=token)
    except Exception as e:
        debug("bank_client.transfer: RPC error: %r" % (e,))
        return False

def get_log(username):
    try:
        conn = _connect_to_bank()
        return conn.call('get_log', username=username)
    except Exception as e:
        debug("bank_client.get_log: RPC error: %r" % (e,))
        return []
