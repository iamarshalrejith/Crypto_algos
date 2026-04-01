# CIA Assignment – Running Key Cipher & DJB2 Hashing

**Roll Number:** 23011102015 → `15 % 10 = 5` → **Running Key Cipher**  
**Language:** Python 3.10+  
**Hash Function:** DJB2 (Daniel J. Bernstein Hash 2)

---

## Theory

### Running Key Cipher

The Running Key Cipher is a classical polyalphabetic substitution cipher. Unlike the Vigenère cipher (which uses a short, repeating keyword), the Running Key Cipher uses a key that is **as long as the plaintext itself**, typically taken from a book or other long text. This eliminates the periodicity that makes Vigenère vulnerable to the Kasiski test.

**Encryption:**
```
c[i] = (p[i] + k[i]) mod 26
```
where `p[i]` is the numeric value of the i-th plaintext letter (a=0, b=1, …, z=25), and `k[i]` is the corresponding key letter.

**Decryption:**
```
p[i] = (c[i] - k[i]) mod 26
```

**Key source:**  
Two public-domain books are concatenated to form the key stream:
- `alice.txt` – *Alice's Adventures in Wonderland* by Lewis Carroll  
- `sherlock.txt` – *A Study in Scarlet* by Arthur Conan Doyle  

Only alphabetic characters (a–z) are retained from the books; all punctuation, digits and whitespace are stripped. This ensures the key and plaintext use the same alphabet.

---

### DJB2 Hash Function

**DJB2** is a non-cryptographic hash function designed by **Daniel J. Bernstein**. It is used here as an integrity check to detect any tampering with the ciphertext.

**Algorithm:**
```python
hash = 5381
for each character c in text:
    hash = (hash * 33 + ord(c)) & 0xFFFFFFFF
return hash % 256
```

Equivalently, `hash * 33` is computed as `(hash << 5) + hash`, which is a common bit-shift optimisation.

**Why DJB2?**
- The seed `5381` and multiplier `33` were chosen empirically by Bernstein for excellent **avalanche effect** (a single character change propagates widely through the hash).
- It is fast, simple, and produces good distribution over ASCII text.
- It is distinct from SHA/MD5 families and from Python's built-in `hash()`, satisfying the "unique hash function" requirement of this assignment.
- The final `% 256` folds the 32-bit value into a single byte (0–255), making the hash compact and easy to store/transmit alongside the ciphertext.

---

## Files

| File | Description |
|---|---|
| `cipher.py` | Main implementation (encrypt, decrypt, DJB2 hash) |
| `test_cipher.py` | Automated round-trip test script with 4 test cases |
| `alice.txt` | Key source book 1  |
| `sherlock.txt` | Key source book 2 |
| `README.md` | This file |

---

## How to Run

### Interactive encryption/decryption

```bash
python cipher.py
```

**Sample session:**
```
[INFO] Key loaded – 250,000+ characters available.

Enter message to encrypt: hello world

--- Encryption ---
Original  : hello world
Encrypted : hptnsoough
DJB2 Hash : 180

--- Decryption ---
[OK] Hash verified successfully.
Decrypted : helloworld
```

> **Note:** Spaces and punctuation are stripped from the plaintext before encryption (only a–z are kept). The decrypted output therefore shows only letters.

### Automated tests

```bash
python test_cipher.py
```

---

## Worked Examples

### Example 1 – Simple message

| Field | Value |
|---|---|
| Plaintext | `helloworld` |
| Key (first 10 chars from books) | e.g. `alicewasbe…` |
| Ciphertext | (varies by key) |
| DJB2 Hash | 0–255 |

**Formula for each character:**  
`c[i] = (ord(p[i]) - ord('a') + ord(k[i]) - ord('a')) % 26 + ord('a')`

### Example 2 – Mixed case with punctuation

| Field | Value |
|---|---|
| Plaintext (raw) | `Running Key Cipher, CIA Assignment 2026!` |
| Plaintext (cleaned) | `runningkeycipherciaassignment` |
| Ciphertext | depends on key stream |
| DJB2 Hash | 0–255 |

Run `python test_cipher.py` to see live output with actual key-derived values.

---

## Tamper Detection

If the ciphertext is modified after encryption, the DJB2 hash of the received ciphertext will not match the transmitted hash, and decryption is aborted:

```
[ERROR] Hash mismatch – ciphertext may have been tampered with!
```

This is demonstrated automatically in `test_cipher.py` (Test 4: Tamper Detection).

---

## Constraints Checklist

- [x] No built-in cryptography libraries used (`Crypto`, `hashlib`, etc.)
- [x] Cipher implemented from scratch in pure Python
- [x] Hash function implemented from scratch (DJB2) – distinct from SHA/MD5 and from any built-in
- [x] Language: Python 3
- [x] README includes theory, instructions, and worked examples
- [x] Test script demonstrates encrypt → hash → decrypt round-trip
