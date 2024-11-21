import random
import string

def generatePassword(length):
    if length < 5:
        raise ValueError("Password length must be at least 5 characters.")
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    password = [
        random.choice(lowercase), random.choice(lowercase), 
        random.choice(uppercase),
        random.choice(digits), random.choice(digits),  
        random.choice(special_characters) 
    ]
    
    all_characters = lowercase + uppercase + digits + special_characters
    password += [random.choice(all_characters) for _ in range(length - len(password))]
    
    random.shuffle(password)
    
    return ''.join(password)


