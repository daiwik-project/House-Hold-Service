import random
import string

def generate_code():
    parts = []
    for i in range(4):
        part = ''
        for j in range(5):
            random_char = random.choice(string.ascii_uppercase + string.digits)
            part += random_char
        parts.append(part) 

    return '-'.join(parts)  


id = generate_code()
generate_code()
