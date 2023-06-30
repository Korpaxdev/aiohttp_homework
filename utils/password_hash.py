import bcrypt


def hash_psw(password):
    password = str(password).encode()
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode()


def check_password(password, hashed_password):
    password = str(password).encode()
    hashed_password = str(hashed_password).encode()
    return bcrypt.checkpw(password, hashed_password)
