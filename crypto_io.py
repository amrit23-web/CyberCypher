import io
import os
import uuid

# Define shift cipher function
def shift_cypher(message, key):
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

# Define block cipher functions
def block_pad(message):
    chunk_size = 3
    padded_chunks = [message[i:i+chunk_size].ljust(chunk_size) for i in range(0, len(message), chunk_size)]
    return padded_chunks

def block_shift(chunks, key):
    encrypted_chunks = []
    for chunk in chunks:
        encrypted_chunks.append("".join([chr(ord(char) + key) for char in chunk]))
    return encrypted_chunks

def block_unshift(chunks, key):
    decrypted_chunks = []
    for chunk in chunks:
        decrypted_chunks.append("".join([chr(ord(char) - key) for char in chunk]))
    return decrypted_chunks

def block_rebuild(chunks):
    return "".join(chunks)

# Define Diffie-Hellman functions
def find_shared_key(private_key, public_key):
    shared_key = public_key ** private_key % dh_mod
    return shared_key

def apply_shift(message, key):
    encrypted = ""
    for char in message:
        encrypted += chr(ord(char) + key)
    return encrypted

def remove_shift(message, key):
    decrypted = ""
    for char in message:
        decrypted += chr(ord(char) - key)
    return decrypted

# Set Diffie-Hellman parameters
dh_base = 8
dh_mod = 29
dh_private_key = 49
dh_public_key = dh_base ** dh_private_key % dh_mod

def main():
    print("Hello iD Campers, Parents, and Staff!")
    print("Welcome to the iD Cryptography Package, cryptoIO!!")
    print("Here you can encrypt messages and save them for others to read.")
    print("But they will only be able to decrypt them if you (remember and) share the secret keys!")

    while True:
        print()
        choice = input("Type 1 to encrypt, 2 to decrypt, or 0 to quit: ")
        
        try: 
            choice = int(choice)
        except: 
            print("Sorry, that is not a valid choice.")
            continue

        if choice == 1:
            encrypt()
        elif choice == 2:
            decrypt()
        elif choice == 0:
            print("Thank you for using iD Tech cryptoIO!")
            print("Have a good summer!")
            break
        else:
            print("Sorry, '{}' is not a valid choice. Pick 1, 2, or 0.".format(choice))
            continue

def encrypt():
    print("Preparing to encrypt...")
    data = get_encrypt_input()

    file_name = str(uuid.uuid4())  # Generate a unique filename using UUID

    while "{}.txt".format(file_name) in os.listdir("msgs"):
        file_name = str(uuid.uuid4())  # Regenerate filename if it already exists
    
    cypher = input(
        "1   : Ceaser (shift) Cypher\n2   : Block Cypher\n3   : Diffie-Hellman Cypher\nPlease select a cypher (1, 2, or 3): ")

    try:
        cypher = int(cypher)
    except ValueError:
        print("Sorry, {} is not a valid choice. Pick 1, 2, or 3.".format(cypher))
        return

    if cypher == 1:
        encrypted = shift_cypher(data[0], data[1])
    elif cypher == 2:
        chunk_list = block_pad(data[0])
        encrypted = block_shift(chunk_list, data[1])
        encrypted = "\n".join(str(s) for s in encrypted)
    elif cypher == 3:
        shared_key = find_shared_key(dh_private_key, data[1])
        encrypted = apply_shift(data[0], shared_key)

    with io.open("msgs/{}.txt".format(file_name), 'w+', encoding="utf-8") as file:
        file.write(encrypted)
    print("Your message was successfully encrypted and saved as {}!\n".format(file_name))

def get_encrypt_input():
    msg = input("Please enter your secret message: ")
    key = get_key()
    return msg, key

def decrypt():
    print("Preparing to decrypt...")
    data = get_decrypt_input()

    while True:
        cypher = input(
            "1   : Ceaser (shift) Cypher\n2   : Block Cypher\n3   : Diffie-Hellman Cypher\nPlease select a cypher (1, 2, or 3): ")

        try:
            cypher = int(cypher)
        except ValueError:
            print("Sorry, {} is not a valid choice. Pick 1, 2, or 3.".format(cypher))
            continue

        if cypher == 1:
            decrypted = shift_cypher(data[0], -data[1])
            break
        elif cypher == 2:
            chunk_list = list(map(int, data[0].split("\n")))
            chunk_list = block_unshift(chunk_list, data[1])
            decrypted = block_rebuild(chunk_list)
            break
        elif cypher == 3:
            shared_key = find_shared_key(dh_private_key, data[1])
            decrypted = remove_shift(data[0], shared_key)
            break
        elif cypher == 0:
            return

    print("The decrypted message is:\n'{}'".format(decrypted))

    return

def get_decrypt_input():
    localMsgs = os.listdir("msgs")
    for i in range(len(localMsgs)):
        n = i + 1   
        padding = " "
        if n <= 99:
            padding += " "
        if n <= 9:
            padding += " "
        print("{}{}: {}".format(n, padding, localMsgs[i]))
    print()

    while True:
        choice = input("Please choose a message from above to decrypt (or, type 0 for manual entry): ")

        try:
            choice = int(choice)
        except ValueError:
            print("Sorry, {} is not a valid choice. Pick between 0 and {}.".format(choice, len(localMsgs)))
            continue

        if choice == 0:
            msg = input("Manually enter the encrypted message: ").strip()
            break
        elif choice <= len(localMsgs):
            with io.open("msgs/{}".format(localMsgs[choice - 1]), 'r', encoding="utf-8") as file:
                msg = file.read()
            break
        else:
            print("Sorry, {} is not a valid choice. Pick between 0 and {}.".format(choice, len(localMsgs)))

    key = get_key()
    return msg, key

def get_key():
    while True:
        try:
            key = int(input("Please enter your secret key (or recipient's public key): "))
            break
        except ValueError:
            print("The secret key should be a number. Try again. ")
    return key

if __name__ == "__main__":
    main()
