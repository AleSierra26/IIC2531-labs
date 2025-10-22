from zoodb import *
from debug import *
import hashlib
import os
import secrets  # más seguro que random para criptografía
import pbkdf2

# --- Configuración de parámetros criptográficos ---
ITERATIONS = 100_000  # aumenta el costo del PBKDF2
SALT_SIZE = 16        # 128 bits de sal (suficiente)
TOKEN_BYTES = 32      # 256 bits de token

# -------------------------------------------------

def hash_password(password: str, salt: bytes) -> str:
    """Devuelve el hash PBKDF2 del password usando la sal dada."""
    # Usamos la versión binaria del password
    return pbkdf2.PBKDF2(password.encode(), salt, iterations=ITERATIONS).hexread(32)

def newtoken(db, cred):
    """Genera un nuevo token aleatorio para el usuario."""
    # secrets.token_hex produce 64 caracteres hexadecimales (32 bytes)
    cred.token = secrets.token_hex(TOKEN_BYTES)
    db.commit()
    return cred.token

def register(username: str, password: str):
    """Crea un nuevo usuario y guarda el hash y la sal."""
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

    # también crea el registro en la tabla Person
    person = Person(username=username, zoobars=10, profile="")
    db_person.add(person)
    db_person.commit()

    return newtoken(db_cred, newcred)

def login(username: str, password: str):
    """Valida las credenciales y retorna un nuevo token si es correcto."""
    db_cred = cred_setup()
    cred = db_cred.query(Cred).get(username)
    if not cred:
        return None

    try:
        salt_bytes = bytes.fromhex(cred.salt)
    except Exception:
        return None  # si la sal está corrupta

    hashed = hash_password(password, salt_bytes)
    if hashed != cred.password:
        return None

    return newtoken(db_cred, cred)

def check_token(username: str, token: str) -> bool:
    """Verifica si el token del usuario es válido."""
    db = cred_setup()
    cred = db.query(Cred).get(username)
    return bool(cred and cred.token == token)
