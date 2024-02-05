from django.contrib.auth.hashers import check_password, make_password



def hash_pass(raw_password):
    hashed_password = make_password(raw_password)
    return hashed_password


def check_pass(password,hashed_password):
    res = check_password(password,hashed_password)
    return res