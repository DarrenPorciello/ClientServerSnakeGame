import random
import math

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(bits):
    p = q = 0
    while not is_prime(p):
        p = random.getrandbits(bits)
    while not is_prime(q) or q == p:
        q = random.getrandbits(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537  # Commonly used public exponent
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted

def decrypt(ciphertext, private_key):
    d, n = private_key
    decrypted = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(decrypted)

def main():
    # Generate key pair
    public_key, private_key = generate_keypair(8)

    # Message to be encrypted
    message = "Hello, RSA encryption!"

    # Encrypt the message
    encrypted_message = encrypt(message, public_key)
    print("Encrypted message:", encrypted_message)

    # Decrypt the message
    decrypted_message = decrypt(encrypted_message, private_key)
    print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    main()
