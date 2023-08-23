import secrets

def generate_flag():
    hash = secrets.token_hex(nbytes=16)
    return "LKS{%s}" % hash