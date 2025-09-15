import hashlib
def main_menu():
    while True:
        display_options()
        choice = input("choose an option: ")

        if choice == '3':
            print("Closing the program.")
            break
        elif choice == '1':
            handle_encryption()
        elif choice == '2':
            handle_decryption()
        else:
            print("Invalid choice. Try again.")


def display_options():
    print("Options:")
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    print("3. Exit")

def encrypt_message(text, key):
    binary_text = to_binary(text)
    adjusted_text = adjust_bits(binary_text, key)
    binary_key = to_binary(str(key))
    encrypted_text = xor_operation(adjusted_text, binary_key)
    hash_result = create_sha256_hash(encrypted_text)
    return encrypted_text, hash_result

def decrypt_message(encrypted_text, key, expected_hash):
    hash_result = create_sha256_hash(encrypted_text)
    if hash_result != expected_hash:
        print("Incorrect hash.")
        return None
    else:
        print("Hash verified successfully.")

    binary_key = to_binary(str(key))
    xor_result = xor_operation(encrypted_text, binary_key)
    original_text = undo_adjust_bits(xor_result, key)
    return binary_to_text(original_text)

def handle_encryption():
    text = input("Enter the message to encrypt: ")
    key = int(input("Enter an integer key: "))
    encrypted_text, hash_result = encrypt_message(text, key)
    print("Encrypted Message:", encrypted_text)
    print("Message Hash:", hash_result)

def handle_decryption():
    encrypted_text = input("Enter the message to decrypt: ")
    key = int(input("Enter the decryption key: "))
    hash_value = input("Enter the message hash: ")
    decrypted_message = decrypt_message(encrypted_text, key, hash_value)
    print("Decrypted Message:", decrypted_message)

# Convert string to binary
def to_binary(input_str):
    return ''.join(f"{ord(c):08b}" for c in input_str)

# Convert binary to string
def binary_to_text(binary):
    characters = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in characters)

# Adjust binary string based on key
def adjust_bits(binary, key):
    return right_shift(binary, 3) if key % 2 == 0 else left_shift(binary, 3)

# Undo the adjustment on binary string based on key
def undo_adjust_bits(binary, key):
    return left_shift(binary, 3) if key % 2 == 0 else right_shift(binary, 3)

# Right shift by n bits
def right_shift(binary, n):
    if len(binary) <= n:
        return '00'
    return binary[-n:] + binary[:-n]

# Left shift by n bits
def left_shift(binary, n):
    if len(binary) <= n:
        return '00'
    return binary[n:] + binary[:n]

# XOR operation
def xor_operation(binary_message, binary_key):
    extended_key = binary_key
    while len(extended_key) < len(binary_message):
        extended_key += binary_key
    return ''.join('0' if bm == bk else '1' for bm, bk in zip(binary_message, extended_key))

# Hashing method using SHA-256
def create_sha256_hash(input_str):
    return hashlib.sha256(input_str.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    main_menu()
