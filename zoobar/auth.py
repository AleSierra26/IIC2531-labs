from zoodb import *
from debug import *
import hashlib
import os
import secrets  # más seguro que random para criptografía
import pbkdf2

ITERATIONS = 100_000
SALT_SIZE = 16 
TOKEN_BYTES = 32 


def hash_password(password: str, salt: bytes) -> str:
    return pbkdf2.PBKDF2(password.encode(), salt, iterations=ITERATIONS).hexread(32)

def newtoken(db, cred):
    cred.token = secrets.token_hex(TOKEN_BYTES)
    db.commit()
    return cred.token

def register(username: str, password: str):
    db_person = person_setup()
    if db_person.query(Person).get(username):
        return None

    db_cred = cred_setup()
    if db_cred.query(Cred).get(username):
        return None

    salt = os.urandom(SALT_SIZE)
    hashed = hash_password(password, salt)

    newcred = Cred()
    newcred.username = username
    newcred.password = hashed
    newcred.salt = salt.hex()
    db_cred.add(newcred)
    db_cred.commit()

    person = Person(username=username, profile="")
    db_person.add(person)
    db_person.commit()

    return newtoken(db_cred, newcred)

def login(username: str, password: str):
    db_cred = cred_setup()
    cred = db_cred.query(Cred).get(username)
    if not cred:
        return None

    try:
        salt_bytes = bytes.fromhex(cred.salt)
    except Exception:
        return None 

    hashed = hash_password(password, salt_bytes)
    if hashed != cred.password:
        return None

    return newtoken(db_cred, cred)

def check_token(username: str, token: str) -> bool:
    """Verifica si el token del usuario es válido."""
    db = cred_setup()
    cred = db.query(Cred).get(username)
    return bool(cred and cred.token == token)
