import bcrypt


def hash_password(password: str) -> str:
    # Generate a salt and hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return the hashed password as a string
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Convert strings to bytes for bcrypt
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        # Verify the password
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except ValueError:
        # If there's any issue with the hash format, return False
        return False