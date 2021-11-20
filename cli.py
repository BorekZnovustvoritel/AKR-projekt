import argparse
from functionalities.rsa import RSA_key
from functionalities.fact_proj import RSA_cracker
from time import perf_counter
from functionalities.resources import logo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RSA Cracker')
    parser.add_argument('-e', '--external-key', nargs=2, default=None, metavar=('mod', 'pub'), type=int, help="Provide external key to crack.")
    parser.add_argument('-l', '--bitlength', type=int, default=64, metavar='bitlength', help="Provide bitlength of the RSA cryptosystem.")
    parser.add_argument('-s', '--silent', action='store_const', default=False, const=True, help="Do not output anything except the answer into the command line.")
    args = parser.parse_args().__dict__
    ex_key = args['external_key']
    bitlength = args['bitlength']
    silent = args['silent']

    key = RSA_key()
    if ex_key is not None:
        key.upload(ex_key[0], ex_key[1])
    else:
        key.generate(bitlength, silent=silent)

    ref = 0
    cracker = RSA_cracker(key)
    if not silent:
        print(logo)
        print("Cracking key:")
        print(f"modulo = {key.mod}")
        print(f"public exponent = {key.public}")
        print(f"Assigned cores: {cracker.cores}")
        print("Cracking, please wait...")
        ref = perf_counter()
    try:
        cracker.start(silent=silent)
        if not silent:
            print(f"Found primes: {cracker.p}, {cracker.q}.")
            print(f"Cracking took: {(perf_counter() - ref) : .3f} s.")
        print("Cracked key:")
        print(f"Modulo = {cracker.key.mod}")
        print(f"Public key = {cracker.key.public}")
        print(f"Private key = {cracker.private_key}")
    except KeyboardInterrupt:
        if not silent:
            print()
            print(f"Cancelled after {(perf_counter() - ref) : .3f} s.")
