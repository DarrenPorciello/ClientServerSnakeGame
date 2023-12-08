import socket
from Crypto.PublicKey import RSA

# Generate key pairs
def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Server key pair
server_private_key, server_public_key = generate_key_pair()
# Server configuration
server_host = '127.0.0.1'
server_port = 12345

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((server_host, server_port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {server_host}:{server_port}")

# Accept a connection
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

# Send the server's public key to the client
client_socket.send(server_public_key)

# Receive the client's public key
client_public_key = client_socket.recv(4096)

while True:
    # Receive encrypted message from the client
    encrypted_message = client_socket.recv(4096)
    
    # Decrypt the message using the server's private key
    decrypted_message = RSA.import_key(server_private_key).decrypt(encrypted_message)
    
    print(f"Received message from client: {decrypted_message.decode('utf-8')}")

    # Send a response to the client
    response = input("Enter response: ")
    
    # Encrypt the response using the client's public key
    encrypted_response = RSA.import_key(client_public_key).encrypt(response.encode('utf-8'), 32)[0]
    
    # Send the encrypted response to the client
    client_socket.send(encrypted_response)
