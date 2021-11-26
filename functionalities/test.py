from time import perf_counter
from functionalities.rsa import RSA_key
from functionalities.fact_proj import RSA_cracker

if __name__ == "__main__": # compares the speed of cracking with filtering out non-primes and without this utility.
    bitlength = 40 # spoiler alert: without it the cracking is much, much faster an resource-friendly
    keyAA = RSA_key()
    keyAA.generate(bitlength)
    print(f"mod: {keyAA.mod}, public: {keyAA.public}")
    crackerA = RSA_cracker(keyAA)
    ref = perf_counter()
    crackerA.start()
    print(f"Without test: {perf_counter() - ref} s.")
    print(f"Private: {crackerA.private_key}")

    keyAB = RSA_key()
    keyAB.upload(keyAA.mod, keyAA.public)
    crackerB = RSA_cracker(keyAB)
    ref = perf_counter()
    crackerB.start(True)
    print(f"With test: {perf_counter() - ref} s.")
    print(f"Private: {crackerB.private_key}")