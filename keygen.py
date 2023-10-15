import rsa
import os

# Generate an RSA key pair
(private_key, public_key) = rsa.newkeys(2048)

# Save the private key to a .pem file
with open('private_key.pem', 'wb') as private_key_file:
    private_key_pem = private_key.save_pkcs1()
    private_key_file.write(private_key_pem)

# Save the public key to a .pem file
with open('public_key.pem', 'wb') as public_key_file:
    public_key_pem = public_key.save_pkcs1()
    public_key_file.write(public_key_pem)

# Print the private key to the terminal
print("RSA Private Key:")
print(private_key.export_key().decode('utf-8'))

# Print the public key to the terminal
print("\nRSA Public Key:")
print(public_key.export_key().decode('utf-8'))
