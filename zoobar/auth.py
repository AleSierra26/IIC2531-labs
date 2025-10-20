from zoodb import *
from debug import *

import hashlib
import random
import os
import pbkdf2

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput.encode()).hexdigest()

    db.commit()
    return cred.token

def login(username, password):
    db_person = person_setup()
    person = db_person.query(Person).get(username)
    if not person:
        return None

    db_cred = cred_setup()
    cred = db_cred.query(Cred).get(username)
    if not cred:
        return None

    salt_bytes = bytes.fromhex(cred.salt)
    hashed = pbkdf2.PBKDF2(password, salt_bytes).hexread(32)

    if cred.password == hashed:
        return newtoken(db_cred, cred)
    return None


def register(username, password):
    db_person = person_setup()
    person = db_person.query(Person).get(username)
    if person:
        return None

    salt = os.urandom(32)
    hashed = pbkdf2.PBKDF2(password, salt).hexread(32)

    db_cred = cred_setup()
    newcred = Cred()
    newcred.username = username
    newcred.password = hashed
    newcred.salt = salt.hex()
    db_cred.add(newcred)
    db_cred.commit()

    return newtoken(db_cred, newcred)



def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False
