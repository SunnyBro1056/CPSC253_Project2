import base64
import binascii
import sys
from tkinter import Tk, filedialog

def main():
    DIVIDER = f"{'-' * 8}"

    # User will choose '1' for encryption or '2' for decryption
    user_choice = startup_sequence()

    ###########################
    # ENCRYPTION CLI DIALOGUE #
    ###########################

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


    ###########################
    # DECRYPTION CLI DIALOGUE #
    ###########################


    elif user_choice == 2: 
        decryptor = Decryptor()

        print("Decryptor engine started.. \n\nPlease use the GUI to choose your encrypted file to decrypt..")

        raw_text_file = get_location_gui()
        with open(raw_text_file, "r") as f:
            raw_text = f.read()

        # Wrapping this in a try/except block since program crashes when trying to decrypt plaintext
        try:
            ciphertext = base64.b64decode(raw_text).decode('utf-16')
        except binascii.Error:
            print('You are trying to decrypt a plaintext file! That will not work. Please use a file encrypted with SuCryptor.')
            sys.exit(1)

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
    print(f"{"/"*6}* Welcome to the SuCryptor Program. Please choose what you would like to do *{"/"*6}\n")
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


############################
# 4-STEP ENCRYPTION METHOD #
############################
# Docstrings will lead through an example encryption of the string "ABCD"


class Encryptor():
    def __init__(self):
        pass
    
    def encrypt_text(self, text: str):
        # See methods defined below for implementation details
        key = len(text) + 4 # The choice of '4' here is arbitrary.
        text = self.transpose_text(text)
        text = self.shift_text(text, key)
        text = self.reverse_text(text)
        text = self.xor_text(text, key)
        return(text)


    def transpose_text(self, text: str) -> str:
        """This function transposes text by calculating half of its length, then 
        shifting the first half and second half. For example: 'ABCD' 
        becomes 'CDAB'. In the case of odd strings, the remaining character
        is tagged onto the end: 'ABCDE' becomes 'CDABE'."""    

        transpose_val = len(text) // 2
        first_half = text[:transpose_val]
        second_half = text[transpose_val: transpose_val * 2]
        new_text = second_half + first_half + text[transpose_val * 2:]

        return new_text


    def shift_text(self, text: str, shift_key: int) -> str: 
        """This function shifts the UNICODE values of each character by
        a predetermined shift key. The string 'CDAB' is transformed to 
        string 'STQR'. Note that since these are UNICODE values, this 
        transformation is case-sensitive."""

        max_value = 0x110000 # 1 value greater than the maximum UNICODE val: 0x10FFFF
        return ''.join(
            chr((ord(char) + shift_key) % max_value)
                for char in text
        )


    def reverse_text(self, text: str) -> str:
        """This function simply reverses the string. This is another layer of 
        transposition. The string 'STQR' becomes 'RQTS'."""
        return text[::-1]


    def xor_text(self, text: str, key: int) -> str:
        """This function uses the built-in Python XOR bitwise operator
        on each character in the string to add another layer of encryption.
        This is easily reversible in decryption, since using the same key
        will reverse it. The string 'RQTS' becomes 'BADC' """
        return ''.join(
            chr(ord(char) ^ key)
            for char in text
        )


############################
# 4-STEP DECRYPTION METHOD #
############################
# Docstrings will lead through an example decryption of the string "BADC"


class Decryptor():
    def __init__(self):
        pass
    
    def decrypt_text(self, text: str):
        key = len(text) + 4 # Arbitrary key; same as encryption algorithm

        # Steps to decrypt are the opposite order of encryption
        text = self.unxor_text(text, key)
        text = self.unreverse_text(text)
        text = self.unshift_text(text, key)
        text = self.untranspose_text(text)

        return text


    def unxor_text(self, text: str, key: int) -> str:
        """This is a perfect example of how using the same key twice with
        an XOR undoes the encryption. Our string 'BADC' is decrypted to 
        'RQTS' using the same exact logic as encryption"""
        return ''.join(
            chr(ord(char) ^ key)
            for char in text
        )

    def unreverse_text(self, text: str) -> str:
        """This is the same logic as encryption; reversing our 
        reversed text will give us the original back.
        Our string 'RQTS' becomes 'STQR'"""
        return text[::-1]

 
    def unshift_text(self, text: str, shift_key: int) -> str:
        """Here we use the same logic with UNICODE values but instead of adding our key, we 
        subtract our key to get the original UNICODE values. Our string 'STQR' becomes
        'CDAB'"""
        max_value = 0x110000
        return ''.join(
            chr((ord(char) - shift_key) % max_value)
                for char in text
        )

  
    def untranspose_text(self, text: str) -> str:
        """This function reverses the transposition by the encryption algorithm.
        We can use the same underlying math in reverse order, and if a string was
        odd, the last remaining character never changed.
        Our string 'CDAB' becomes 'ABCD'"""
        transpose_val = len(text) // 2

        original_second_half = text[:transpose_val]
        original_first_half = text[transpose_val: transpose_val * 2]
        remainder = text[transpose_val * 2:]

        original_text = original_first_half + original_second_half + remainder
        return original_text

main()
