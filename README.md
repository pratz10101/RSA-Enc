# Secure Chat Application

A Flask-based web application that enables secure communication between users using RSA encryption. Messages are encrypted with the recipient's public key and can only be decrypted using the recipient's private key.

## Features

- User authentication system
- RSA key pair generation for each user
- End-to-end encryption for messages
- Secure message storage
- Private key passphrase protection

## Prerequisites

- Python 3.x
- Flask
- rsa

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pratz10101/RSA-Enc.git
cd secure-chat-app
```

2. Install the required dependencies:
```bash
pip install flask rsa
```

3. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Configuration

1. Update the `app.secret_key` in `app.py` with a secure random value
2. The application creates a `user_keys` directory to store RSA keys
3. Default users are stored in a dictionary (replace with a proper database in production)

## Project Structure

```
secure-chat-app/
├── app.py
├── templates/
│   ├── login.html
│   └── chat.html
└── user_keys/
    └── (generated key pairs)
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

3. Log in using the default credentials:
   - Username: user1, Password: password1
   - Username: user2, Password: password2

4. To send a message:
   - Enter the recipient's username
   - Type your message
   - Click Send

5. To decrypt a received message:
   - Enter your private key passphrase
   - Click Decrypt

## Security Notes

- This is a demonstration project and should not be used in production without proper security improvements
- In a production environment:
  - Replace the in-memory user storage with a secure database
  - Implement proper session management
  - Use HTTPS
  - Implement proper key management
  - Add input validation and sanitization
  - Add rate limiting
  - Add proper error handling

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
