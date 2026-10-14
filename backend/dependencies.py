from pwdlib import PasswordHash

def hash_password(password):

    password_hash = PasswordHash.recommended()

    return password_hash.hash(password)

def verify_password(hashed_password, password):
    password_hash = PasswordHash.recommended()

    return password_hash.verify(password, hashed_password)