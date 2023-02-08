import cryptocode

key = "!Bertulio123"

password = "123"


def encryp_Password(password):
    encryp_Password = cryptocode.encrypt(password, key)
    return encryp_Password


def return_Password(hash):
    password = cryptocode.decrypt(hash, key)
    return password
