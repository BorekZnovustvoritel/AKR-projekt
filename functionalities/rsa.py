from Crypto.Util import number
from Crypto.Random import random

class RSA_key():
    default_pub = 65537 # commonly used public key, can be changed
    def __init__(self):
        self.mod: int = 0
        self.public: int = 0
        self.bitlength: int = 0

    def generate(self, bitlength: int, public: int = default_pub, silent: bool = False):
        """Populate the object with self-generated values."""
        self.bitlength = bitlength
        if bitlength % 2 != 0:
            raise ValueError("Unable to generate RSA modulo with odd bitlength.")
            # Actually you can but it would require to check if the primes are lower than certain value, which would reduce strength
        prime_bitlength = bitlength // 2 # bitlength of primes
        if not silent: # You want your talking app? You get it. You don't? You won't get it. As simple as that.
            print(f"Generating RSA public key of bitlength: {bitlength}...")
        r = number.getPrime(prime_bitlength) # external library is used here
        s = number.getPrime(prime_bitlength)
        self.mod = r * s
        if not silent:
            print("Done.")
        phi_mod = (r - 1) * (s - 1)
        self.public = public % phi_mod # we shouldn't really have a public exponent bigger than neccessary
        while number.GCD(phi_mod, self.public) != 1: # if the numbers have a common divider bigger than 1, we need to regenerate the public key
            self.public = random.randint(2, phi_mod - 1)
        return self # returns the object of the key, because it's cool, that's why

    def upload(self, mod, public=default_pub):
        """Populate the object with external values."""
        self.mod = mod
        self.public = public
        self.__set_bitlength() # we need a bitlength in the cracker object
        return self

    def __set_bitlength(self):
        """Computes the bitlength of an uploaded key."""
        mod = self.mod
        base = 4 # we need an even number for the cracker even if the bitlength is actually odd, because it would generate bad starting points
        bitlength = 2
        while base < mod: # just comparing to a number 4 to the power of (num of cycles)
            base *= 4
            bitlength += 2
        self.bitlength = bitlength

if __name__ == "__main__": # testing and external key generating purposes
    key = RSA_key().generate(64)
    print(key.mod)
    print(key.public)