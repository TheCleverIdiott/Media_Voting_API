from passlib.context import CryptContext

pass_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(plain_password):
    return pass_context.hash(plain_password)

def password_verify(plain_password,hash_password):
    return pass_context.verify(plain_password,hash_password)