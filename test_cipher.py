"""
test_cipher.py
--------------
Automated test script for the Running Key Cipher + DJB2 hash.
Demonstrates encrypt → hash → decrypt round-trip with multiple examples.
"""

from cipher import clean_text, load_key, djb2_hash, encrypt, decrypt


def run_test(label: str, message: str, key: str) -> None:
    print(f"\n{'='*55}")
    print(f"Test : {label}")
    print(f"{'='*55}")

    original_clean = clean_text(message)
    print(f"Plaintext (raw)    : {message}")
    print(f"Plaintext (cleaned): {original_clean}")

    cipher_text, hash_val = encrypt(message, key)
    print(f"Ciphertext         : {cipher_text}")
    print(f"DJB2 Hash          : {hash_val}")

    decrypted = decrypt(cipher_text, hash_val, key)
    print(f"Decrypted          : {decrypted}")

    assert decrypted == original_clean, \
        f"FAIL: expected '{original_clean}', got '{decrypted}'"
    print("Result             : PASS ")


def test_tamper_detection(key: str) -> None:
    print(f"\n{'='*55}")
    print("Test : Tamper Detection")
    print(f"{'='*55}")

    message = "integrity test"
    cipher_text, hash_val = encrypt(message, key)

    # Flip one character in ciphertext
    tampered = list(cipher_text)
    tampered[0] = 'z' if tampered[0] != 'z' else 'a'
    tampered_text = ''.join(tampered)

    print(f"Original ciphertext : {cipher_text}")
    print(f"Tampered ciphertext : {tampered_text}")

    result = decrypt(tampered_text, hash_val, key)
    assert result is None, "FAIL: tamper was not detected!"
    print("Result              : PASS   (tamper correctly detected)")


if __name__ == "__main__":
    print("Loading key from alice.txt + sherlock.txt ...")
    key = load_key()
    print(f"Key length: {len(key):,} characters\n")

    # Example 1 – simple lowercase message
    run_test(
        label="Simple message",
        message="hello world",
        key=key
    )

    # Example 2 – mixed case with spaces and punctuation
    run_test(
        label="Mixed case with punctuation",
        message="Running Key Cipher, CIA Assignment 2026!",
        key=key
    )

    # Example 3 – longer sentence
    run_test(
        label="Longer sentence",
        message="The quick brown fox jumps over the lazy dog",
        key=key
    )

    # Example 4 – tamper detection
    test_tamper_detection(key)

    print(f"\n{'='*55}")
    print("All tests passed!")
    print(f"{'='*55}")
