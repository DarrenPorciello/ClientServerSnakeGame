import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def decrypt_message(private_key, ciphertext):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=padding.SHA256()),
            algorithm=padding.SHA256(),
            label=None
        )
    )

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345
server_socket.bind((host, port))
server_socket.listen()

print(f"Server listening on {host}:{port}")

# Accept a connection
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

# Generate key pair
private_key, public_key = generate_key_pair()

# Send public_key to the client
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
client_socket.send(public_key_bytes)

# Receive encrypted message from the client
encrypted_message = client_socket.recv(4096)  # Adjust buffer size as needed
decrypted_message = decrypt_message(private_key, encrypted_message)
print("Decrypted Message:", decrypted_message.decode())

# Close the sockets
client_socket.close()
server_socket.close()
