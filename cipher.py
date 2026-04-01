"""
CIA Assignment - Classical Cipher & Hashing Implementation
Roll Number  : 15  -->  15 % 10 = 5  -->  Running Key Cipher
Hash Function: DJB2 (Daniel J. Bernstein Hash 2)
Books used as key source:
    alice.txt   - Alice's Adventures in Wonderland (Lewis Carroll)
    sherlock.txt - A Study in Scarlet (Arthur Conan Doyle)
"""


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """Keep only lowercase English letters (a-z)."""
    text = text.lower()
    result = ""
    for c in text:
        if 'a' <= c <= 'z':
            result += c
    return result


# ---------------------------------------------------------------------------
# Key Loading
# ---------------------------------------------------------------------------

def load_key() -> str:
    """
    Concatenate and clean two book files to produce the running key.
    The combined text forms a very long, non-repeating key stream.
    """
    with open("alice.txt", "r", encoding="utf-8", errors="ignore") as f:
        text1 = f.read()

    with open("sherlock.txt", "r", encoding="utf-8", errors="ignore") as f:
        text2 = f.read()

    combined = clean_text(text1 + text2)
    return combined


# ---------------------------------------------------------------------------
# DJB2 Hash Function
# ---------------------------------------------------------------------------

def djb2_hash(text: str, mod_size: int = 256) -> int:
    """
    DJB2 hashing algorithm by Daniel J. Bernstein.

    Why DJB2?
    ---------
    DJB2 is a well-known, fast, non-cryptographic hash function that
    produces good distribution.  The core idea is:
        hash = 5381
        for each character c:
            hash = hash * 33 + ord(c)          (equivalently: (hash << 5) + hash + ord(c))

    The magic constant 5381 and multiplier 33 were chosen empirically by
    Bernstein for their excellent avalanche effect and speed on ASCII text.
    We fold the 32-bit result into [0, mod_size) using modulo so it fits
    neatly in a single byte for our integrity check.

    This is different from every built-in Python hash and from SHA/MD5
    families, making it unique per the assignment requirement.
    """
    h = 5381
    for c in text:
        # (h << 5) + h  ==  h * 33
        h = ((h << 5) + h + ord(c)) & 0xFFFFFFFF   # keep 32-bit unsigned
    return h % mod_size


# ---------------------------------------------------------------------------
# Running Key Cipher - Encrypt
# ---------------------------------------------------------------------------

def encrypt(plaintext: str, key: str) -> tuple[str, int]:
    """
    Running Key Cipher encryption.

    Each plaintext letter p[i] is shifted by the corresponding key letter
    k[i], both treated as values in 0-25:
        c[i] = (p[i] + k[i]) mod 26

    The key must be at least as long as the plaintext (guaranteed here
    because the key is built from two full books).

    Returns (ciphertext, djb2_hash_of_ciphertext).
    """
    plaintext = clean_text(plaintext)   # normalise

    if len(plaintext) > len(key):
        raise ValueError(
            f"Plaintext length ({len(plaintext)}) exceeds key length ({len(key)}). "
            "Use longer book files."
        )

    cipher_chars = []
    for i, char in enumerate(plaintext):
        p = ord(char) - ord('a')
        k = ord(key[i]) - ord('a')
        c = (p + k) % 26
        cipher_chars.append(chr(c + ord('a')))

    cipher_text = ''.join(cipher_chars)
    hash_val = djb2_hash(cipher_text)
    return cipher_text, hash_val


# ---------------------------------------------------------------------------
# Running Key Cipher - Decrypt
# ---------------------------------------------------------------------------

def decrypt(cipher_text: str, received_hash: int, key: str) -> str | None:
    """
    Verify integrity via DJB2 hash, then reverse the Running Key Cipher:
        p[i] = (c[i] - k[i]) mod 26
    """
    # --- Integrity check ---
    computed_hash = djb2_hash(cipher_text)
    if computed_hash != received_hash:
        print("[ERROR] Hash mismatch – ciphertext may have been tampered with!")
        return None

    print("[OK] Hash verified successfully.")

    # --- Decrypt ---
    plaintext_chars = []
    for i, char in enumerate(cipher_text):
        c = ord(char) - ord('a')
        k = ord(key[i]) - ord('a')
        p = (c - k) % 26
        plaintext_chars.append(chr(p + ord('a')))

    return ''.join(plaintext_chars)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    key = load_key()
    print(f"[INFO] Key loaded – {len(key):,} characters available.\n")

    message = input("Enter message to encrypt: ")

    print("\n--- Encryption ---")
    print(f"Original  : {message}")

    cipher, hash_val = encrypt(message, key)

    print(f"Encrypted : {cipher}")
    print(f"DJB2 Hash : {hash_val}")

    print("\n--- Decryption ---")
    decrypted = decrypt(cipher, hash_val, key)

    if decrypted:
        print(f"Decrypted : {decrypted}")
