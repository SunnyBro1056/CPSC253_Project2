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


############################
# 4-STEP ENCRYPTION METHOD #
############################
# Docstrings will lead through an example encryption of the string "ABCD"


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


