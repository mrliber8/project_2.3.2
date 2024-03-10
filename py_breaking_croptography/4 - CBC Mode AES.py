from Crypto.Cipher import AES
from base64 import b64decode
from base64 import b64encode


def repeating_key_xor(text, key):
    """Takes two bytestrings and XORs them, returning a bytestring.
    Extends the key to match the text length.
    
    Parameters
    ----------
    text : bytes
        bytes-object to be xor'd w/ key
    key : bytes
        bytes-object to be xor'd w/ text
        
    Returns
    -------
    bytes
        binary XOR of text & key
    """
    counter = 0
    
    key = bytearray(key)
    while len(text) != len(key):
        key.append(key[counter])
        counter += 1    

    str = []
    for x in range(len(text)):
        str.append(text[x] ^key[x])

    xor_output = bytes(str)

    return xor_output


def ECB_decrypt(ciphertext, key):
    """Accepts a ciphertext in byte-form,
    as well as 16-byte key, and returns 
    the corresponding plaintext.

    Parameters
    ----------
    ciphertext : bytes
        ciphertext to be decrypted
    key : bytes
        key to be used in decryption

    Returns
    -------
    bytes
        decrypted plaintext
    """

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext



def CBC_decrypt(ciphertext, key, IV):
    """Decrypts a given plaintext in CBC mode.
    First splits the ciphertext into keylength-size blocks,
    then decrypts them individually w/ ECB-mode AES
    and XOR's each result with either the IV
    or the previous ciphertext block.
    Appends decrypted blocks together for the output.

    Parameters
    ----------
    ciphertext : bytes
        ciphertext to be decrypted
    key : bytes
        Key to be used in decryption
    IV : bytes
        IV to be used for XOR in first block

    Returns
    -------
    bytes
        Decrypted plaintext
        """
    

    plaintext = b''
    previous_block = IV

    # First splits the ciphertext into keylength-size blocks,
    for i in range(0, len(ciphertext), 16):
        current_block = ciphertext[i:i+16]
        # then decrypts them individually w/ ECB-mode AES
        decrypted_block = ECB_decrypt(current_block, key)
        # and XOR's each result with either the IV or the previous ciphertext block.
        plaintext_block = repeating_key_xor(decrypted_block, previous_block)
        # Appends decrypted blocks together for the output.
        plaintext += plaintext_block
        # Reset the block
        previous_block = current_block

    return(plaintext)


# Laat dit blok code onaangetast & onderaan je code!
a_ciphertext = b64decode('e8Fa/QnddxdVd4dsL7pHbnuZvRa4OwkGXKUvLPoc8ew=')
a_key = b'SECRETSAREHIDDEN'
a_IV = b'WE KNOW THE GAME'
assert CBC_decrypt(a_ciphertext, a_key, a_IV)[:18] == \
    b64decode('eW91IGtub3cgdGhlIHJ1bGVz')



def ECB_encrypt(plaintext, key):
    # Moved the padding to CBC to better handle different lengths

    # Initialise the cipher in AES-ECb mode
    cipher = AES.new(key, AES.MODE_ECB)
    # Encrypt
    ciphertext = cipher.encrypt(plaintext)

    return ciphertext



def CBC_encrypt(plaintext, key, IV):

    ciphertext = b''
    previous_block = IV

    padding_length = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_length]) * padding_length


    for i in range(0, len(plaintext), 16):
        current_block = ciphertext[i:i+16]
        # XOR current plaintext block with the previous ciphertext block
        xor_block = repeating_key_xor(current_block, previous_block)
        # Encrypt the XOR'd block
        ciphertext_block = ECB_encrypt(xor_block, key)
        # Append the encrypted block to the ciphertext
        ciphertext += ciphertext_block
        # Update the previous block for the next iteration
        previous_block = ciphertext_block


    return ciphertext
