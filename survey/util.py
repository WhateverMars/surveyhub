import random


# this is used to generate a link for the users survey
def random_string(size):
    rand_str = ""
    for i in range(size):
        rand_int = random.randint(97, 122)
        if random.randint(0, 1):
            rand_int -= 32
        rand_str += chr(rand_int)
    return rand_str
