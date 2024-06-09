
import random  # generate random numbers


def diffie_hellman():
    p = 23  # 1) large prime number p
    g = 5   # 2) primitive root g

    # each user generate their secret key
    a = random.randint(1, p- 1)
    b = random.randint(1, p - 1)

    # each user make their public keys
    A = pow(g, a, p)
    B = pow(g, b, p)

    # each user calculate the shared secret key
    shared_key_a = pow(B, a, p)
    shared_key_b = pow(A, b, p)

    # check if the shared keys match
    if shared_key_a == shared_key_b:
        return shared_key_a  # return shared secret key


def vigenere(plaintext, key, mode):

    output = ""  # Initialize the output string, put the final result in output

    key_indices = [ord(k.upper()) - 65 for k in key]  # Iterate over each char in key, get the uppercase
    # ASCII code of it and subtract by 65 to get the correct char in the alphabet (0 - 25)

    for i, char in enumerate(plaintext):  # Iterate through each character in the plaintext with its index i

        if char.isalpha():  # Check if the character is alphabetic

            key_shift = key_indices[i % len(key)]  # repeats the key if the plaintext is longer than key

            if mode == 'Encrypt':  # Check if the chosen mode is encryption

                # convert to uppercase, find its correct index, add the key shift, % 26 to make sure it stays within
                # character range, then return it back to character
                new_index = (ord(char.upper()) - 65 + key_shift) % 26
                result = chr(new_index + 65)

            else:  # Decryption

                # Do the reverse for decryption
                new_index = (ord(char.upper()) - 65 - key_shift) % 26
                result = chr(new_index + 65)

            if char.islower():  # Return to lower case if the given text was in lower case
                result = result.lower()

            output += result  # Append the result character to the output
        else:
            output += char  # If the character is not alphabetic, add it unchanged to the output

    return output


def playfair_cipher(message, key, mode):
    # Create the Playfair cipher square
    playfair_square = create_playfair_square(key)

    # Prepare the message
    if mode == 'encrypt':
        message = preprocess_message(message)
    pairs = [message[i:i + 2] for i in range(0, len(message), 2)]

    result = ""

    for pair in pairs:
        row1, col1 = find_in_square(playfair_square, pair[0])
        row2, col2 = find_in_square(playfair_square, pair[1])

        if mode == 'encrypt':
            if row1 == row2:
                result += playfair_square[row1][(col1 + 1) % 5] + playfair_square[row2][(col2 + 1) % 5]
            elif col1 == col2:
                result += playfair_square[(row1 + 1) % 5][col1] + playfair_square[(row2 + 1) % 5][col2]
            else:
                result += playfair_square[row1][col2] + playfair_square[row2][col1]
        else:
            if row1 == row2:
                result += playfair_square[row1][(col1 - 1) % 5] + playfair_square[row2][(col2 - 1) % 5]
            elif col1 == col2:
                result += playfair_square[(row1 - 1) % 5][col1] + playfair_square[(row2 - 1) % 5][col2]
            else:
                result += playfair_square[row1][col2] + playfair_square[row2][col1]

    if mode == 'decrypt':
        result = remove_padding(result)

    return result


def preprocess_message(message):
    message = message.replace('J', 'I').upper().replace(" ", "")
    preprocessed_message = ""
    i = 0
    while i < len(message):
        preprocessed_message += message[i]
        if i + 1 < len(message) and message[i] == message[i + 1]:
            preprocessed_message += 'X'
        elif i + 1 == len(message):
            preprocessed_message += 'X'
        else:
            preprocessed_message += message[i + 1]
        i += 2
    if len(preprocessed_message) % 2 != 0:
        preprocessed_message += 'X'
    return preprocessed_message


def remove_padding(message):
    result = ""
    i = 0
    while i < len(message):
        if i + 1 < len(message) and message[i + 1] == 'X' and (i + 2 >= len(message) or message[i] != message[i + 2]):
            result += message[i]
            i += 1  # Skip the 'X'
        else:
            result += message[i]
        i += 1
    return result


def create_playfair_square(key):
    # Remove duplicate letters from the key
    unique_key = ''.join(sorted(set(key.upper().replace('J', 'I')), key=key.index))

    # Create the Playfair cipher square
    playfair_square = []
    remaining_letters = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) not in unique_key and chr(i) != 'J']
    for char in unique_key + ''.join(remaining_letters):
        if len(playfair_square) == 0 or len(playfair_square[-1]) == 5:
            playfair_square.append([])
        playfair_square[-1].append(char)

    return playfair_square


def find_in_square(playfair_square, char):
    for i, row in enumerate(playfair_square):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None, None


def main():

    # Vigenere cipher inputs
    PlainText = "PROJECT"
    key = "Key"
    encrypted = vigenere(PlainText, key, 'Encrypt')
    decrypted = vigenere(encrypted, key, 'Decrypt')
    print(f"Encryption of Vigenere Cipher: {encrypted}")
    print(f"Decryption of Vigenere Cipher:  {decrypted}")

    # Diffie hellman
    shared_key = diffie_hellman()
    print(f"Shared Key: {shared_key}")  # return the shared key from diffie hellman

    # Playfair cipher inputs
    message = "PROJECT".replace("J", "I")
    key = "KEY"
    encrypted_message = playfair_cipher(message, key, 'encrypt')
    decrypted_message = playfair_cipher(encrypted_message, key, 'decrypt')
    print(f"Playfair Cipher: Encrypted Message: {encrypted_message}")
    print(f"Playfair Cipher: Decrypted Message: {decrypted_message}")



if __name__ == "__main__":
    main()
