def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    keyword_repeat = (keyword * (len(plaintext) // len(keyword))) + keyword[:len(plaintext) % len(keyword)]
    for p, k in zip(plaintext, keyword_repeat):
        if p.isalpha():
            shift_base = 65 if p.isupper() else 97
            shift = ord(k.upper()) - 65
            p = chr((ord(p) - shift_base + shift) % 26 + shift_base)
        ciphertext += p
    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    keyword_repeat = (keyword * (len(ciphertext) // len(keyword))) + keyword[:len(ciphertext) % len(keyword)]
    for c, k in zip(ciphertext, keyword_repeat):
        if c.isalpha():
            shift_base = 65 if c.isupper() else 97
            shift = ord(k.upper()) - 65
            c = chr((ord(c) - shift_base - shift) % 26 + shift_base)
        plaintext += c
    return plaintext
