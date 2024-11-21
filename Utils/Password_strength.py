import re
import math

def check_password_strength(password):
    min_length = 5
    char_set = {
        'lowercase': re.compile(r'[a-z]'),
        'uppercase': re.compile(r'[A-Z]'),
        'digits': re.compile(r'[0-9]'),
        'special': re.compile(r'[!@#$%^&*(),.?":{}|<>]')
    }

    if len(password) < min_length:
        return "Weak", "Password is too short. It should be at least 8 characters long."

    checks = {
        'lowercase': bool(char_set['lowercase'].search(password)),
        'uppercase': bool(char_set['uppercase'].search(password)),
        'digits': bool(char_set['digits'].search(password)),
        'special': bool(char_set['special'].search(password))
    }

    if all(checks.values()):
        strength = "Strong"
        feedback = "Your password is strong! It contains a good mix of characters and is sufficiently long."
    elif any(checks.values()):
        strength = "Medium"
        feedback = "Your password is decent, but it could be stronger. Consider increasing the length and adding more complexity."
    else:
        strength = "Weak"
        feedback = "Your password is weak. Use at least one lowercase letter, one uppercase letter, one number, and one special character."

    # time to crack (Brute Force)
    entropy, crack_time = calculate_crack_time(password)

    feedback += f"\nEntropy: {entropy:.2f} bits"
    feedback += f"\nEstimated crack time: {crack_time}"

    return strength, feedback


def calculate_crack_time(password):
    lower = 26  
    upper = 26 
    digits = 10 
    specials = 32  
    
    total_chars = lower + upper + digits + specials
    entropy = math.log2(total_chars ** len(password))  
    combinations = total_chars ** len(password)
    crack_time_seconds = combinations / (10**9)  # 1 billion attempts per second

    if crack_time_seconds < 60:
        crack_time = f"{crack_time_seconds:.2f} seconds"
    elif crack_time_seconds < 3600:
        crack_time = f"{crack_time_seconds / 60:.2f} minutes"
    elif crack_time_seconds < 86400:
        crack_time = f"{crack_time_seconds / 3600:.2f} hours"
    elif crack_time_seconds < 31536000:
        crack_time = f"{crack_time_seconds / 86400:.2f} days"
    else:
        crack_time = f"{crack_time_seconds / 31536000:.2f} years"

    return entropy, crack_time


