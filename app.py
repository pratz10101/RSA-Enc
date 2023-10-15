from flask import Flask, request, render_template, redirect, url_for, flash
import rsa
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random value in production

# Directory to store user key pairs
KEYS_DIR = 'user_keys'

# Create the KEYS_DIR if it doesn't exist
if not os.path.exists(KEYS_DIR):
    os.makedirs(KEYS_DIR)

# Users dictionary for demonstration purposes (replace with a real authentication system)
users = {'user1': 'password1', 'user2': 'password2'}

# Messages dictionary for storing messages
messages = {}

# Dictionary to store user's private key passphrases
private_key_passphrases = {}

def generate_key_pair(username):
    # Check if key pair already exists
    public_key_path = os.path.join(KEYS_DIR, f'{username}_public.pem')
    private_key_path = os.path.join(KEYS_DIR, f'{username}_private.pem')

    if not (os.path.exists(public_key_path) and os.path.exists(private_key_path)):
        # Generate RSA key pair if it doesn't exist
        (pubkey, privkey) = rsa.newkeys(512)

        # Store the keys in .pem files
        with open(public_key_path, 'wb') as public_file:
            public_file.write(pubkey.save_pkcs1('PEM'))

        with open(private_key_path, 'wb') as private_file:
            private_file.write(privkey.save_pkcs1('PEM'))



def encrypt_message(message, receiver_username):
    # Load the receiver's public key
    with open(os.path.join(KEYS_DIR, f'{receiver_username}_public.pem'), 'rb') as public_file:
        receiver_public_key = rsa.PublicKey.load_pkcs1(public_file.read())

    # Encrypt the message with the receiver's public key
    encrypted_message = rsa.encrypt(message.encode('utf-8'), receiver_public_key)
    
    return encrypted_message

def decrypt_message(encrypted_message, username, private_key_passphrase):
    # Load the user's private key using the passphrase
    with open(os.path.join(KEYS_DIR, f'{username}_private.pem'), 'rb') as private_file:
        private_key_data = private_file.read()
    
    # Decrypt the private key using the passphrase
    try:
        private_key = rsa.PrivateKey.load_pkcs1(private_key_data, private_key_passphrase)
    except ValueError as e:
        return str(e)

    # Decrypt the message using the user's private key
    try:
        decrypted_message = rsa.decrypt(encrypted_message, private_key).decode('utf-8')
        return decrypted_message
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # Generate RSA key pair for the user if it doesn't exist
            generate_key_pair(username)
            return redirect(url_for('chat', username=username))
        else:
            flash("Invalid login credentials. Please try again.", 'danger')
            return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/chat/<username>', methods=['GET', 'POST'])
def chat(username):
    if request.method == 'POST':
        receiver = request.form['receiver']
        message = request.form['message']
        if receiver in users:
            # Encrypt the message using the receiver's public key
            encrypted_message = encrypt_message(message, receiver)

            # Store the encrypted message
            messages.setdefault(receiver, []).append((username, encrypted_message))
        else:
            flash(f"User '{receiver}' not found. Please try again.", 'danger')

    return render_template('chat.html', username=username, messages=messages.get(username, []))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    username = request.form['username']
    receiver = request.form['receiver']
    encrypted_message = request.form['encrypted_message']
    private_key_passphrase = request.form['private_key_passphrase']

    receiver_private_key_passphrase = private_key_passphrases.get(receiver)

    if receiver_private_key_passphrase == private_key_passphrase:
        decrypted_message = decrypt_message(encrypted_message.encode('utf-8'), username, private_key_passphrase)

        if decrypted_message:
            flash(f"Decrypted Message: {decrypted_message}", 'success')
        else:
            flash("Failed to decrypt the message. Please check your passphrase.", 'danger')
    else:
        flash("Wrong Private Key", 'danger')

    return redirect(url_for('chat', username=username))

if __name__ == '__main__':
    app.run(debug=True)
    