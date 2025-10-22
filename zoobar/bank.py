# bank.py (cliente wrapper)
import time
from debug import *
import bank_client as _bank_client

def balance(username):
    return _bank_client.balance(username)

def create_account(username, initial_balance=10):
    return _bank_client.create_account(username, initial_balance)

def transfer(sender, recipient, zoobars, token):
    return _bank_client.transfer(sender, recipient, zoobars, token)

def get_log(username):
    raise NotImplementedError("Use bank RPC to fetch audit logs (implement rpc_get_log)")
