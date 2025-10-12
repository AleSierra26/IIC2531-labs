#!/usr/bin/env python3
import rpclib
import sys
import bank
from debug import *

class BankRpcServer(rpclib.RpcServer):
    def rpc_balance(self,username):
        return bank.balance(username)       
    
    def rpc_register_user(self, username):
        return bank.register_user(username)
 

    def rpc_transfer(self,sender,recipient,zoobars):
        return bank.transfer(sender,recipient,zoobars)

    def rpc_get_log(self,username):
        return bank.get_log(username)

    def rpc_check_in(self,username):
        return bank.check_in(username)


if len(sys.argv) != 2:
    print(sys.argv[0], "too few args")

s = BankRpcServer()
s.run_fork(sys.argv[1])
