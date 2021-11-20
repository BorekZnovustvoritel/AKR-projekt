from Crypto.Util import number
from Crypto.Random import random

class RSA_key():
    default_pub = 65537
    def __init__(self):
        self.mod: int = 0
        self.public: int = 0
        self.bitlength: int = 0

    def generate(self, bitlength: int, public: int = default_pub, silent: bool = False):
        self.bitlength = bitlength
        if bitlength % 2 != 0:
            raise ValueError("Unable to generate RSA modulo with odd bitlength.")
        prime_bitlength = bitlength // 2
        if not silent:
            print(f"Generating RSA public key of bitlength: {bitlength}...")
        r = number.getPrime(prime_bitlength)
        s = number.getPrime(prime_bitlength)
        self.mod = r * s
        if not silent:
            print("Done.")
        phi_mod = (r - 1) * (s - 1)
        self.public = public % phi_mod
        while number.GCD(phi_mod, self.public) != 1:
            self.public = random.randint(2, phi_mod - 1)
        return self

    def upload(self, mod, public=default_pub):
        self.mod = mod
        self.public = public
        self.__set_bitlength()
        return self

    def __set_bitlength(self):
        mod = self.mod
        base = 4
        bitlength = 2
        while base < mod:
            base *= 4
            bitlength += 2
        self.bitlength = bitlength

if __name__ == "__main__":
    key = RSA_key().generate(64)
    print(key.mod)
    print(key.public)