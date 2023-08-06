#!/usr/bin/python
# coding:utf-8
import base64
from Crypto.Cipher import AES
import hashlib
import requests


class AESCipher:

    def __init__(self):
        appkey = '8ca391611637072ae15557651b70387e'
        self.key = appkey
        self.iv = self.gen_iv(appkey)

    def __pad(self, text):
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    def gen_iv(self, app_key):
        m = hashlib.md5()
        m.update(app_key.encode("utf-8"))
        return m.hexdigest()[:16]

    def encrypt(self, raw):
        """加密"""
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def aes_256_encrypt(plain_str, app_key):
        raw = pad(plain_str)
        iv = gen_iv(app_key)
        cipher = AES.new(app_key, AES.MODE_CBC, iv)
        r = base64.b64encode(cipher.encrypt(raw)).decode()
        return base64.b64encode(r.encode()).decode()

    def decrypt(self, enc, app_key):
        """解密"""
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.__unpad(cipher.decrypt(enc).decode("utf-8"))


if __name__ == '__main__':
    e = AESCipher()
    phone_err = ['18622726417']
    for secret_data in phone_err:
        enc_str = e.encrypt(secret_data, app_key)
        data = {}
        data['phone'] = enc_str
        data['appid'] = 'a10a7a6deea7112b0786babbbf08f7aa'
        r = requests.post('https://api-alpha.immomo.com/zombie/spam/check', data=data)
        print('enc_str: ' + r.text)
