#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: D3TA (Dear Diary, Don't Tell Anyone)
Package: d3lib

Based on https://stackoverflow.com/a/44212550

Copyright (C) 2018  Korvin F. Ezüst

This module is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This module is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

__authors__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "GNU Lesser General Public License 3.0"
__version__ = "1.0"
__email__ = "dev@korvin.eu"
__status__ = "Working"


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
    # encode key and source to bytes
    key = key.encode("utf-8")
    source = source.encode("utf-8")
    # use SHA-256 over our key to get a proper-sized AES key
    key = SHA256.new(key).digest()
    # generate IV
    iv = Random.new().read(AES.block_size)
    cip = AES.new(key, AES.MODE_CBC, iv)
    # calculate needed padding
    padding = AES.block_size - len(source) % AES.block_size
    source += bytes([padding]) * padding
    # store the IV at the beginning and encrypt
    data = iv + cip.encrypt(source)
    # decode to string
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
    # encode key and source to bytes
    key = key.encode("utf-8")
    source = base64.b64decode(source.encode("utf-8"))
    # use SHA-256 over our key to get a proper-sized AES key
    key = SHA256.new(key).digest()
    # extract the IV from the beginning
    iv = source[:AES.block_size]
    cip = AES.new(key, AES.MODE_CBC, iv)
    # decrypt
    data = cip.decrypt(source[AES.block_size:])
    # pick the padding value from the end
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")
    # remove the padding, decode to string
    return data[:-padding].decode("utf-8")


if __name__ == "__main__":
    passphrase = "example passphrase"
    text = "Hello, مرحبا, ਸਤ ਸ੍ਰੀ ਅਕਾਲ, สวัสดี, 你好, こんにちは"
    encrypted = encrypt(passphrase, text)
    print(encrypted)

    decrypted = decrypt(passphrase, encrypted)
    print(decrypted)
