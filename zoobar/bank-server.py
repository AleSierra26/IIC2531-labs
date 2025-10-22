#!/usr/bin/env python3
import rpclib
import sys
import time

from debug import *
from zoodb import *
import auth_client

class BankRpcServer(rpclib.RpcServer):
    def rpc_zoobars(self, username):
        db = bank_setup()
        acc = db.query(Bank).get(username)
        if not acc:
            return None
        return acc.zoobars

    def rpc_create_account(self, username, initial_balance=10):
        db = bank_setup()
        acc = db.query(Bank).get(username)
        if acc:
            return False
        newacc = Bank()
        newacc.username = username
        newacc.zoobars = int(initial_balance)
        db.add(newacc)
        db.commit()
        return True

    def rpc_transfer(self, sender, recipient, zoobars, token):
        if not auth_client.check_token(sender, token):
            if getattr(self, 'caller', None) == 'profile':
                log(f"bank_server: transfer autorizado desde profile para {sender}")
                authorized = True
            else:
                log(f"bank_server: invalid token for sender={sender}")
                return False
        else:
            authorized = True

        if authorized:
            bankdb = bank_setup()
            transferdb = transfer_setup()
            sender_acc = bankdb.query(Bank).get(sender)
            recipient_acc = bankdb.query(Bank).get(recipient)

            if not sender_acc or not recipient_acc:
                log("bank_server.transfer: Bank missing sender=%s recipient=%s" % (sender, recipient))
                return False

            try:
                zoobars = int(zoobars)
            except Exception:
                return False

            new_sender = sender_acc.zoobars - zoobars
            new_recipient = recipient_acc.zoobars + zoobars
            if new_sender < 0 or new_recipient < 0:
                log("bank_server.transfer: insufficient funds or overflow")
                return False

            sender_acc.zoobars = new_sender
            recipient_acc.zoobars = new_recipient
            bankdb.commit()

            t = Transfer()
            t.sender = sender
            t.recipient = recipient
            t.amount = zoobars
            t.time = time.asctime()
            transferdb.add(t)
            transferdb.commit()

            return True

    def rpc_get_log(self, username):
        log(f"bank_server: fetching log for {username}")
        db = transfer_setup()
        logs = db.query(Transfer).filter_by(sender=username).all()
        result = []
        for t in logs:
            result.append({
                "sender": t.sender,
                "recipient": t.recipient,
                "amount": t.amount,
                "time": t.time
            })
        return result


if len(sys.argv) != 2:
    print(sys.argv[0], "too few args")
    sys.exit(1)

s = BankRpcServer()
s.run_fork(sys.argv[1])
