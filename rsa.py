from Crypto.Util import number
from Crypto.Random import random

class RSA_key():
    def __init__(self, bitlength, public=65537):
        if bitlength % 2 != 0:
            raise ValueError("Unable to generate RSA modulo with odd bitlength.")
        prime_bitlength = bitlength // 2
        print("Generating RSA public key...")
        r = number.getPrime(prime_bitlength)
        print("1/2 done.")
        s = number.getPrime(prime_bitlength)
        self.mod = r * s
        print("Done.")
        phi_mod = (r - 1) * (s - 1)
        self.public = public % phi_mod
        while number.GCD(phi_mod, self.public) != 1:
            self.public = random.randint(2, phi_mod - 1)

if __name__ == "__main__":
    key = RSA_key(1024)
    print(key.mod)
    print(key.public)