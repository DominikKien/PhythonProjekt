from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_aes_256(plaintext, key):
    # Ensure the key is 32 bytes (256 bits)
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long.")

#Generate a random 16-byte IV
    iv = get_random_bytes(16)

#Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

#Pad plaintext to be a multiple of 16 bytes
    padded_plaintext = pad(plaintext.encode(), AES.block_size)

#Encrypt the plaintext
    ciphertext = cipher.encrypt(padded_plaintext)

#Return the IV and ciphertext (both are needed for decryption)
    return iv + ciphertext

def decrypt_aes_256(ciphertext, key):
    # Ensure the key is 32 bytes (256 bits)
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long.")

#Extract the IV and actual ciphertext
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]

#Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

#Decrypt and unpad the plaintext
    padded_plaintext = cipher.decrypt(actual_ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)

    return plaintext.decode()

#Example usage
key = get_random_bytes(32)  # Generate a random 32-byte key
plaintext = "This is a secret message."

ciphertext = encrypt_aes_256(plaintext, key)
print("Ciphertext:", ciphertext)

decrypted_text = decrypt_aes_256(ciphertext, key)
print("Decrypted text:", decrypted_text)