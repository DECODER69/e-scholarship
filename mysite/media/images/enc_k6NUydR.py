import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Generate a key
password = b"my_secret_password"
salt = b"unique_salt"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256,
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))

# Encrypt a message
f = Fernet(key)
ciphertext = f.encrypt(b"my secret message")
print(ciphertext)

# Decrypt the message
plaintext = f.decrypt(ciphertext)
print(plaintext)
