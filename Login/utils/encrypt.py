from passlib.context import CryptContext
from .env import config_object
from cryptography.fernet import Fernet

# Security
SECRET_KEY = config_object["KEY"].get("secret", "321ed8e7990903e774116c75553022ab99b3744ba0cd4d3fd5889770bcc4cc2c")
ALGORITHM = config_object["KEY"].get("algorithm", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config_object["KEY"].getint("token_expire", 120)
SALT = config_object["KEY"].get("salt", "this_is_salt")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
fernet = Fernet(config_object["KEY"].get("key"))


def verify_password(raw_pwd, hashed_pwd):
    return pwd_context.verify(raw_pwd + SALT, hashed_pwd)


def get_pwd_hashed(pwd):
    return pwd_context.hash(pwd + SALT)


def get_project_key(name: str):
    return fernet.encrypt(name.encode())


def get_project_from_key(key: str):
    return fernet.decrypt(key.encode())
