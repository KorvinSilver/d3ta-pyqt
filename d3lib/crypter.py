#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: D3TA (Dear Diary, Don't Tell Anyone)
Package: d3lib

Copyright (C) 2018  Korvin F. Ezüst

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

__authors__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "GNU General Public License version 3"
__version__ = "1.0"
__email__ = "dev@korvin.eu"
__status__ = "Production"


def encrypt(key, source):
    """
    Encrypts a string using AES encryption
    and returns it encoded in base64 as a string

    :param key: password
    :type key: str
    :param source: text to be encrypted
    :type source: str
    :return: encrypted text encoded in base64
    :rtype: str
    """
    # Encode key and source to bytes
    key = key.encode("utf-8")
    source = source.encode("utf-8")
    # Use SHA-256 over the key to get an AES key
    key = SHA256.new(key).digest()
    # Generate IV
    iv = Random.new().read(AES.block_size)
    cip = AES.new(key, AES.MODE_CBC, iv)
    # Calculate padding
    padding = AES.block_size - len(source) % AES.block_size
    source += bytes([padding]) * padding
    # Store the IV at the beginning and encrypt
    data = iv + cip.encrypt(source)
    # Decode to string
    return base64.b64encode(data).decode("utf-8")


def decrypt(key, source):
    """
    Decrypts a string that was encoded in base64
    and encrypted using AES encryption

    :param key: password
    :type key: str
    :param source: encrypted text in base64
    :type source: str
    :return: decrypted text
    :rtype: str
    """
    # Encode key and source to bytes
    key = key.encode("utf-8")
    source = base64.b64decode(source.encode("utf-8"))
    # Use SHA-256 over the key to get an AES key
    key = SHA256.new(key).digest()
    # Extract the IV from the beginning
    iv = source[:AES.block_size]
    cip = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt
    data = cip.decrypt(source[AES.block_size:])
    # Pick the padding value from the end
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")
    # Remove the padding, decode to string
    return data[:-padding].decode("utf-8")


if __name__ == "__main__":
    passphrase = "example passphrase"
    text = "Hello, مرحبا, ਸਤ ਸ੍ਰੀ ਅਕਾਲ, สวัสดี, 你好, こんにちは"
    encrypted = encrypt(passphrase, text)
    print(encrypted)

    decrypted = decrypt(passphrase, encrypted)
    print(decrypted)
