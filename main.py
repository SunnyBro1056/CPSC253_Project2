import base64
import sys
from tkinter import Tk, filedialog
from encryptor import Encryptor
from decryptor import Decryptor

def main():
    DIVIDER = f"{'-' * 8}"
    # User will choose '1' for encryption or '2' for decryption
    user_choice = startup_sequence()

    # ENCRYPTION
    if user_choice == 1:
        encryptor = Encryptor()
        print("Encryptor engine started..\n\nPlease use the GUI to choose your plaintext file to encrypt..")

        plaintext_file = get_location_gui()
        with open(plaintext_file, "r") as f:
            plaintext = f.read()

        ciphertext = encryptor.encrypt_text(plaintext)
        print(f"\n\nEncryption succeeded! Your original string was: \n\n{DIVIDER}\n{plaintext}\n{DIVIDER}\n\nand it was turned into: \n\n{DIVIDER}\n{ciphertext}\n{DIVIDER}\n\n")

        # Base64 is used to encode the raw ciphertext so that it can safely be 
        # written to a UTF-8 text file. This does not do any extra encryption work; 
        # I was just getting errors trying to write my ciphertext to a file and found
        # out why.
        safe_text = base64.b64encode(ciphertext.encode('utf-16')).decode('utf-8')

        _ = input("Your encrypted file is ready to save. Please enter any value into the terminal to start the GUI:\n> ")
        encrypted_text_location = get_savefileas_gui()
        with open(encrypted_text_location, "w") as f:
            _ = f.write(safe_text)

    # DECRYPTION 
    elif user_choice == 2: 
        decryptor = Decryptor()

        print("Decryptor engine started.. \n\nPlease use the GUI to choose your encrypted file to decrypt..")

        raw_text_file = get_location_gui()
        with open(raw_text_file, "r") as f:
            raw_text = f.read()
        ciphertext = base64.b64decode(raw_text).decode('utf-16')

        original_text = decryptor.decrypt_text(ciphertext)
        print(f"\n\nDecryption succeeded! Your ciphertext was: \n\n{DIVIDER}\n{ciphertext}\n{DIVIDER}\n\nand its original string was: \n\n{DIVIDER}\n{original_text}\n{DIVIDER}\n\n")
        _ = input("Your decrypted file is ready to save. Please enter any value into the terminal to start the GUI:\n> ")

        decrypted_text_location = get_savefileas_gui()
        with open(decrypted_text_location, "w") as f:
            _ = f.write(original_text)


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


##########################
# FILESYSTEM GUI METHODS #
##########################


def get_location_gui() -> str:
    """This method is for selecting files that the program will use."""
    root = Tk()
    root.withdraw()
    location = filedialog.askopenfilename()
    root.destroy()

    if not location:
        print("No file selected. Stopping program..")
        sys.exit(1)

    if not location.endswith('.txt'):
        print("Invalid file selected. This program only officially runs with '.txt' files.")
        sys.exit(1)

    return location


def get_savefileas_gui():
    """This method is for selecting a location to save files that the program has produced."""
    root = Tk()
    root.withdraw()
    location = filedialog.asksaveasfilename(
        title="Choose where to save the file",
        defaultextension=".txt")  
    root.destroy()

    if not location:
        print("No location selected. Stopping program..")
        sys.exit(1)

    if not location.endswith('.txt'):
        location = location + '.txt'

    return location


main()
