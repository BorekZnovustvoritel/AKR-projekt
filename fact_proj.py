from rsa import RSA_key
from Crypto.Util import number
from sqroot import sqroot

def rsa_factorization(num):
    max_fact = int(sqroot(num))
    if max_fact % 2 == 0:
        max_fact -= 1
    for i in range(max_fact, 1, -2):
        if num % i == 0:
            return [i, num//i]

if __name__ == "__main__":
    from time import perf_counter
    bitlength = abs(int(input("Insert bitlength of modulo:  ")))
    key = RSA_key(bitlength)
    print(f"Modulo is: {key.mod}")
    print(f"Public exponent is: {key.public}")
    ref = perf_counter()
    print("Cracking, please wait...")
    p, q = rsa_factorization(key.mod)
    print([p, q])
    print("Time in seconds: %.2f" % (perf_counter() - ref))
    print("Generating Private key...")
    priv_key = number.inverse(key.public, (p - 1) * (q - 1))
    print(f"Private key is: {priv_key}")
    input("Program finished, press enter.")
