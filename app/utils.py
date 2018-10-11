import hashlib


def pass_hash(password):
    '''

    :param password(str):
    :return: password(b)
    '''
    md = hashlib.md5()
    md.update(password.encode())
    password = md.digest()
    return password
