from base64 import b64decode
from Crypto.Cipher import AES
from secrets import token_bytes
from base64 import b64encode

def pkcs7_pad(plaintext, blocksize):
    """Appends the plaintext with n bytes,
    making it an even multiple of blocksize.
    Byte used for appending is byteform of n.

    Parameters
    ----------
    plaintext : bytes
        plaintext to be appended
    blocksize : int
        blocksize to conform to

    Returns
    -------
    plaintext : bytes
        plaintext appended with n bytes
    """

    # Determine how many bytes to append
    n = blocksize - len(plaintext)%blocksize
    # Append n*(byteform of n) to plaintext
    # n is in a list as bytes() expects iterable
    plaintext += (n*bytes([n]))
    return plaintext

def ECB_oracle(plaintext, key):
    """Appends a top-secret identifier to the plaintext
    and encrypts it under AES-ECB using the provided key.

    Parameters
    ----------
    plaintext : bytes
        plaintext to be encrypted
    key : bytes
        16-byte key to be used in decryption

    Returns
    -------
    ciphertext : bytes
        encrypted plaintext
    """
    plaintext += b64decode('U2F5IG5hIG5hIG5hCk9uIGEgZGFyayBkZXNlcnRlZCB3YXksIHNheSBuYSBuYSBuYQpUaGVyZSdzIGEgbGlnaHQgZm9yIHlvdSB0aGF0IHdhaXRzLCBpdCdzIG5hIG5hIG5hClNheSBuYSBuYSBuYSwgc2F5IG5hIG5hIG5hCllvdSdyZSBub3QgYWxvbmUsIHNvIHN0YW5kIHVwLCBuYSBuYSBuYQpCZSBhIGhlcm8sIGJlIHRoZSByYWluYm93LCBhbmQgc2luZyBuYSBuYSBuYQpTYXkgbmEgbmEgbmE=')
    plaintext = pkcs7_pad(plaintext, len(key))
    cipher = cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

# Genereer een willekeurige key
key = token_bytes(16)

#####################################
###  schrijf hieronder jouw code  ###
### verander code hierboven niet! ###
#####################################

def find_block_length():
    """Finds the block length used by the ECB oracle.

    Returns
    -------
    blocksize : integer
        blocksize used by ECB oracle
    """
    # Start by sending an empty string
    data = b''
    initial_len = len(ECB_oracle(data, key))

    while True:
        data += b'X'
        new_len = len(ECB_oracle(data, key))  # Encrypt the data
        if new_len > initial_len:  # Check if the ciphertext length increased
            blocksize = new_len - initial_len  # The increase in length is the blocksize
            return blocksize


blocksize = find_block_length()
print('Blocksize is: ', blocksize)


#target_ciphertext = ECB_oracle(data, key)

def get_target_ciphertext(blocksize):
    data = b''
    for x in range(blocksize-1):
        data += b'X'


    #padding = b'X' * (blocksize - 1)  # Create padding one byte short of the blocksize
    #target_ciphertext = ECB_oracle(padding, key)  # Encrypt the padding
    target_ciphertext = ECB_oracle(data, key)
    return target_ciphertext

# Gebruik de eerder gevonden blocksize
target_ciphertext = get_target_ciphertext(blocksize)
print(f"Target ciphertext: {target_ciphertext}")


def discover_first_byte(blocksize, target_ciphertext):
    discovered_byte = b''

    # bytes = 8bit = 11111111 = 256
    for byte in range(256):

        # Padding - 1
        data = b''
        for x in range(blocksize-1):
            data += b'X'

        # Send it to the oracle
        guess = data + bytes([byte])
        guessed_ciphertext = ECB_oracle(guess, key)

        # If it matches, we found it!
        if guessed_ciphertext[:blocksize] == target_ciphertext[:blocksize]:  # Vergelijk met doelciphertext
            discovered_byte = bytes([byte])  # Byte gevonden
            break

    return discovered_byte



first_byte = discover_first_byte(blocksize, target_ciphertext)
print('First byte: ', first_byte)


def find_secret_text():
    '''
    Herhaal stap c & e voor de resterende bytes, totdat je de geheime tekst hebt gevonden. 
    Doe dit door je padding steeds één byte kleiner te maken en aan te vullen met de 
    ontdekte letter uit de geheime tekst. 
    Hint: Je zal je functie per blok te werken moeten laten gaan.
    
    '''
    pass