def encrypt(message, public_key):
    encrypted_message = [pow(ord(char), public_key, 1000) for char in message]
    return encrypted_message

def decrypt(encrypted_message, private_key):
    decrypted_message = ''.join([chr(pow(char, private_key, 1000)) for char in encrypted_message])
    return decrypted_message

# Example usage
message = "Hello, RSA!"
public_key = 13  # Public key (e)
private_key = 937  # Private key (d)

# Encryption
encrypted_message = encrypt(message, public_key)
print("Encrypted message:", encrypted_message)

# Decryption
decrypted_message = decrypt(encrypted_message, private_key)
print("Decrypted message:", decrypted_message)
