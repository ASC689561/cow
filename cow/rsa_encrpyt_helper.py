import base64
import os

import rsa


class RSAEncryptHelper:

    def __init__(self, path=os.getenv("HOME") + '/.ssh'):
        self.path = path
        self.public_path = os.path.join(self.path, 'public.pem')
        self.private_path = os.path.join(self.path, 'private.pem')
        self.load_or_create()

    def load_or_create(self):
        if not (os.path.isfile(self.private_path) and os.path.isfile(self.public_path)):
            (pubkey, privkey) = rsa.newkeys(512)

            with open(self.private_path, mode='wb') as f:
                f.write(privkey.save_pkcs1('PEM'))

            with open(self.public_path, mode='wb') as f:
                f.write(pubkey.save_pkcs1('PEM'))

        with open(self.private_path, mode='rb') as f:
            key_data = f.read()
            self.privkey = rsa.PrivateKey.load_pkcs1(key_data)

        with open(self.public_path, mode='rb') as f:
            key_data = f.read()
            self.pubkey = rsa.PublicKey.load_pkcs1(key_data)

    def encrypt(self, message):
        m = message.encode()
        crypto = rsa.encrypt(m, self.pubkey)
        return base64.b64encode(crypto).decode()

    def decrypt(self, encoded_message):
        m = base64.b64decode(encoded_message)
        return rsa.decrypt(m, self.privkey).decode()


if __name__ == '__main__':
    h = RSAEncryptHelper()
    print(h.encrypt('xin chao'))
    print(h.decrypt(h.encrypt('xin chao')))
