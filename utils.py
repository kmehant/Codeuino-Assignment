import os
import binascii


def generate_api_key():
    # creates a 32 Byte => 256 bit random value
    # this serves as our API key
    return binascii.hexlify(os.urandom(32)).decode()
