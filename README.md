# SuCryptor

This encryption algorithm is a school-grade level encryption algorithm. It should not be used to encrypt real or sensitive data. SuCryptor is an encryption algorithm that can both encrypt and decrypt using three methods of cryptography: transposition, shifting, and bitwise XOR operations. We first generate a simple key that two steps of the encryption algorithm will use. This key is just the length of the string + 4. For example, for string “ABCD” the key would be the integer 8. The algorithm then works in four phases:

1. The plaintext is divided into two halves: the first half and the second half. These two halves are then swapped. For example, the string “ABCD” will become “CDAB”. In the event of an odd length string, the last remaining character is left untouched at the end of the string. For example, the string “ABCDE” is transposed into “CDABE” with the “E” left untouched. 

2. The text is shifted in a Caesar-Cipher-like manner with the pre-computed shift key. We shift each character’s UNICODE value forward by the key integer. For example, in string “CDAB” we will take the first character, “C” which has a Unicode value of 67, and we will add “8” making its UNICODE value 75. Unicode value 75 is “K”. This is repeated for all other characters, and we end with the string “KLIJ”. 

3. We then add another layer of simple transposition: reversing the string. This is easily done and turns the string “KLIJ” to “JILK”. 

4. The final cryptographic operation performed on this string is an XOR. Each character is compared against the XOR of the precomputed key (8 for our original string). From our bitwise operation, our string “JILK” turns into “BADC”. This concludes the cryptographic algorithm. 

In order to use this program, you must provide input. This input is provided through a .txt file with plaintext written inside of it for encryption, or an encrypted .txt file for decryption. Once you start the program, you can choose between encryption and decryption. Afterwards, a file picker GUI opens, and you can select the file you want to input. The program does not accept files that do not end in .txt. I did test this encryption algorithm with other text files, and it worked without problems (I even successfully encrypted and decrypted the whole main.py), although, the code has been hardened to only allow .txt files for simplicity. Once the encryption algorithm has finished encrypting your plaintext, or finished decrypting your ciphertext, another file picker GUI will appear where you can save finished file in .txt format. 

# How to operate the program 

In order to run, the program needs Python (preferably Python 3 or any newer version), and Tkinter (for the file picker GUI). Tkinter comes pre-installed with most Python installations, however, if not, it may be installed on Debian/Ubuntu with “sudo apt install python3-tk". Tkinter is always included on Windows. 

Before running the program, prepare your plaintext file. Make a .txt file including any plaintext you wish to encrypt. For example, you can write “Hello” and save it as ‘plaintext.txt’. Now, run the python program from the CLI by navigating to the project’s root directory and running the command python main.py. You will be asked if you wish to encrypt or decrypt. Type the number 1 to encrypt, and then a file picker GUI will pop up. Select your plaintext.txt file you created. The program will then encrypt the message and show you the final ciphertext. Enter anything in the terminal to confirm, and then you will be able to save the file anywhere via another file picker GUI that pops up. 

In order to decrypt, this will be a similar process. Start the program in the console with python main.py and this time enter 2 to decrypt. You can then choose your encrypted .txt file and input it into the program. The program will show you your ciphertext and your original plaintext. You can then input anything into the terminal to confirm, and you will be asked to save your original plaintext string anywhere on your computer in the form of a .txt file.  
