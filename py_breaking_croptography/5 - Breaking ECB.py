from base64 import b64decode
from Crypto.Cipher import AES
from secrets import token_bytes
#from base64 import b64encode

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
    '''
    a. Breid de functie find_block_length() uit zodat deze de orakel-functie een steeds 
    grotere reeks van dezelfde bytes voert (e.g. "X", dan "XX", "XXX", etc.), zo'n reeks bytes 
    heet padding. Doe dit tot je ziet dat het begin van de ciphertekst niet meer verandert; dit 
    levert je de blocksize die de orakel-functie gebruikt. 
    
    '''
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
    '''
    Voer de orakel-functie een padding van een formaat dat één byte kleiner is dan de 
    blocksize (e.g. bij een blocksize van 4 stuur je de bytestring "XXX"). Dit geeft je 
    je “doelciphertekst”. Hint: Vergeet niet om je blok te vullen met bytes en niet een string!
    '''
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
    '''
    Ga nu de ciphertekst van alle mogelijke combinaties van [padding] + [laatste byte] 
    plainteksten bij langs (Als je bloklengte 4 bytes zou zijn, zou je dus de plainteksten 
    "XXXA", "XXXB", "XXXC", etc. proberen) tot je een combinatie vindt die overeen komt 
    met het eerste blok van je doelciphertekst. Je hebt nu de eerste byte van de geheime 
    tekst ontdekt! 
    Hint: Hoeveel mogelijke waardes bestaan er voor deze laatste byte? Hoe 'loop' je 
    door al die waardes heen?
    '''
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


def find_secret_text(blocksize, key):
    '''
    Herhaal stap c & e voor de resterende bytes, totdat je de geheime tekst hebt gevonden. 
    Doe dit door je padding steeds één byte kleiner te maken en aan te vullen met de 
    ontdekte letter uit de geheime tekst. 
    Hint: Je zal je functie per blok te werken moeten laten gaan.
    
    '''

    # Bereken de lengte van de geheime tekst
    initial_data = b'X' * (blocksize * 2)
    initial_length = len(ECB_oracle(initial_data, key))
    secret_length = initial_length - len(initial_data)
    
    discovered_text = b''
    # Int is nodig en geen float daarom floor divider
    for block in range((secret_length // blocksize) + 1):  # Voor elk blok in de geheime tekst
        for byte_index in range(blocksize):  # Voor elke byte in het huidige blok
            # Maak de padding een byte kleiner voor elke ontdekte byte
            padding = b'A' * (blocksize - byte_index - 1)
            current_block_start = block * blocksize
            current_block_end = (block + 1) * blocksize
            # Send it tot he oracle
            block_to_match = ECB_oracle(padding, key)[current_block_start:current_block_end]

            # bytes = 8bit = 11111111 = 256
            for byte in range(256):  # Probeer elke mogelijke byte
                guess = padding + discovered_text + bytes([byte])
                guess_block = ECB_oracle(guess, key)[current_block_start:current_block_end]
                if guess_block == block_to_match:
                    discovered_text += bytes([byte])
                    break

            # Controleer of we aan het einde van de geheime tekst zijn
            if len(discovered_text) >= secret_length:
                break

    return discovered_text


secret_text = find_secret_text(blocksize, key)
print('Geheime tekst:', secret_text)