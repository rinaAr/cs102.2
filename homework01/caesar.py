def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
        ciphertext += char
    return ciphertext
 
def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            char = chr((ord(char) - shift_base - shift) % 26 + shift_base)
        plaintext += char
    return plaintext
