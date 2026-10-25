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

############################
# 4-STEP DECRYPTION METHOD #
############################
# Docstrings will lead through an example decryption of the string "BADC"

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

