import base64
from encryptor import Encryptor
from decryptor import Decryptor

def main():

    # User will choose '1' for encryption or '2' for decryption
    user_choice = startup_sequence()

    # ENCRYPTION
    if user_choice == 1:
        encryptor = Encryptor()
        print("Encryptor engine started..\n")
        text_input = input("Input text to be encrypted..\n")

        ciphertext = encryptor.encrypt_text(text_input)
        print(f"\n\nHere is your ciphertext. Your original string was '{text_input}' and it was turned into '{ciphertext}'")

        # Base64 is used to encode the raw ciphertext so that it can safely be 
        # written to a UTF-8 text file. This does not do any extra encryption work; 
        # I was just getting errors trying to write my ciphertext to a file and found
        # out why.
        safe_text = base64.b64encode(ciphertext.encode('utf-16')).decode('utf-8')
        with open("encrypted.txt", "w") as f:
            _ = f.write(safe_text)

    # DECRYPTION 
    elif user_choice == 2: 
        decryptor = Decryptor()

        with open("encrypted.txt", "r") as f:
            raw_text = f.read()

        ciphertext = base64.b64decode(raw_text).decode('utf-16')

        original_text = decryptor.decrypt_text(ciphertext)
        print(f"Your original text was '{original_text}'") 
        #decryptor


####################################
# PICKING ENCRYPTION OR DECRYPTION #
####################################


def startup_sequence() -> int:
    """This function exists to decide the main operation of the program: 
    encryption or decryption. This function will return a '1' for encryption 
    or '2' for decryption."""

    # Startup CLI text-sequence
    print(f"{"/"*6}* Welcome to the SuEncryptor Program. Please choose what you would like to do *{"/"*6}\n")
    print("1) Encrypt a text file\n2) Decrypt a text file\n\n")

    # Receive user input: encryption or decryption
    user_input = False
    while user_input is not True:
        user_choice = input("Please enter '1' or '2': ") 
        user_input = validate_input(user_choice)

    return int(user_choice)


def validate_input(text: str) -> bool:
    """This function ensures that the user has entered '1' or '2' correctly."""
    ERROR_MESSAGE = f"You entered {text} which is not valid. Please only enter integers '1' or '2'"
    try:
        if int(text) not in range(1, 3):
            print(ERROR_MESSAGE)
            return False

        # If the value makes it here, that means it is sucesfully an integer 1 or 2
        return True

    except ValueError:
        print(ERROR_MESSAGE)
        return False


main()
