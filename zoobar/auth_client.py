from debug import *
import rpclib
import sys, os
sys.path.append(os.getcwd())
import readconf

def login(username, password):
    host = readconf.read_conf().lookup_host('auth')
    with rpclib.client_connect(host) as c:
        return c.call('login', username=username, password=password)

def register(username, password):
    host = readconf.read_conf().lookup_host('auth')
    with rpclib.client_connect(host) as c:
        token = c.call('register', username=username, password=password)

    if token:
        from zoodb import person_setup, bank_setup, Person, Bank
        db_person = person_setup()
        if not db_person.query(Person).get(username):
            newperson = Person()
            newperson.username = username
            db_person.add(newperson)
            db_person.commit()

            db_bank = bank_setup()
            newbank = Bank()
            newbank.username = username
            newbank.balance = 10
            db_bank.add(newbank)
            db_bank.commit()

    return token



def check_token(username, token):
    host = readconf.read_conf().lookup_host('auth')
    with rpclib.client_connect(host) as c:
        return c.call('check_token', username=username, token=token)