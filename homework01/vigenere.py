def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    """
    ciphertext = []
    keyword = keyword.upper()
    keyword_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(keyword[keyword_index % len(keyword)]) - ord('A')
            encrypted_char = chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
            if char.islower():
                encrypted_char = encrypted_char.lower()
            ciphertext.append(encrypted_char)
            keyword_index += 1
        else:
            ciphertext.append(char)

    return ''.join(ciphertext)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    """
    plaintext = []
    keyword = keyword.upper()
    keyword_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(keyword[keyword_index % len(keyword)]) - ord('A')
            decrypted_char = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
            if char.islower():
                decrypted_char = decrypted_char.lower()
            plaintext.append(decrypted_char)
            keyword_index += 1
        else:
            plaintext.append(char)

    return ''.join(plaintext)


if __name__ == "__main__":
    # Test cases
    print(encrypt_vigenere("PYTHON", "A"))  # Output: PYTHON
    print(encrypt_vigenere("python", "a"))  # Output: python
    print(encrypt_vigenere("ATTACKATDAWN", "LEMON"))  # Output: LXFOPVEFRNHR

    print(decrypt_vigenere("PYTHON", "A"))  # Output: PYTHON
    print(decrypt_vigenere("python", "a"))  # Output: python
    print(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"))  # Output: ATTACKATDAWN
