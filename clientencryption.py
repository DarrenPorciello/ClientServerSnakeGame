from Crypto.PublicKey import RSA
import socket
# Generate key pairs
def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key



# Client key pair
client_private_key, client_public_key = generate_key_pair()



# Client configuration
server_host = '127.0.0.1'
server_port = 12345

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_host, server_port))
print(f"Connected to server at {server_host}:{server_port}")

# Receive the server's public key
server_public_key = client_socket.recv(4096)

# Send the client's public key to the server
client_socket.send(client_public_key)

while True:
    # Get user input
    message = input("Enter message: ")
    
    # Encrypt the message using the server's public key
    encrypted_message = RSA.import_key(server_public_key).encrypt(message.encode('utf-8'), 32)[0]
    
    # Send the encrypted message to the server
    client_socket.send(encrypted_message)

    # Receive the response from the server
    encrypted_response = client_socket.recv(4096)
    
    # Decrypt the response using the client's private key
    decrypted_response = RSA.import_key(client_private_key).decrypt(encrypted_response)
    
    print(f"Received response from server: {decrypted_response.decode('utf-8')}")
