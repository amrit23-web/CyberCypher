def caesar_cipher(message, key):
    encrypted = ""
    for char in message:
        if char.isalpha():
            shifted = ord(char) + key
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted += chr(shifted)
        else:
            encrypted += char
    return encrypted

def main():
    message = input("Enter the message to encrypt: ")
    key = int(input("Enter the key for Caesar Cipher (an integer): "))
    encrypted_message = caesar_cipher(message, key)
    print("Encrypted message:", encrypted_message)

if __name__ == "__main__":
    main()
