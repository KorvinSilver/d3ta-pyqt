#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: Dear Diary, Don't Tell Anyone

Based on https://stackoverflow.com/a/44212550

Copyright 2018, Korvin F. Ezüst

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


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
