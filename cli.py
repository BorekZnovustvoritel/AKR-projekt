import argparse
from functionalities.rsa import RSA_key
from functionalities.fact_proj import RSA_cracker
from time import perf_counter
from functionalities.resources import logo, minimal_bitlength

if __name__ == "__main__": # CLI standardised version of the app
    parser = argparse.ArgumentParser(description='RSA Cracker')
    parser.add_argument('-e', '--external-key', nargs=2, default=None, metavar=('<mod>', '<pub>'), type=int, help="Provide external key to crack.")
    parser.add_argument('-l', '--bitlength', type=int, default=64, metavar='<bitlength>', help="Provide bitlength of the RSA cryptosystem.")
    parser.add_argument('-s', '--silent', action='store_const', default=False, const=True, help="Do not output anything except the answer into the command line.")
    parser.add_argument('-o', '--out', type=str, default=None, metavar='<path>', help="Output the cracked key to a json file.")
    args = parser.parse_args().__dict__
    ex_key = args['external_key']
    bitlength = args['bitlength']
    silent = args['silent']
    path = args['out']


    if bitlength < minimal_bitlength:
        print("Bitlength too small.")
        exit() # Filtering invalid inputs. Smaller inputs break the code.

    key = RSA_key()
    if ex_key is not None:
        if ex_key[0] < 2 or ex_key[1] < 2:
            print("Invalid RSA key provided.")
            exit()  # Filtering invalid inputs. Smaller inputs break the code. Bigger invalid inputs still can.
        key.upload(ex_key[0], ex_key[1])
    else:
        key.generate(bitlength, silent=silent)

    cracker = RSA_cracker(key)
    if not silent:
        print(logo)
        print("Cracking key:")
        print(f"modulo = {key.mod}")
        print(f"public exponent = {key.public}")
        print(f"Assigned cores: {cracker.cores}")
        print("Cracking, please wait...")
        ref = perf_counter() # time reference
    try:
        cracker.start(silent=silent)
        if not silent:
            print(f"Found primes: {cracker.p}, {cracker.q}.")
            print(f"Cracking took: {(perf_counter() - ref) : .3f} s.")
        if path is None or not silent:
            print("Cracked key:")
            print(f"Modulo = {cracker.key.mod}")
            print(f"Public key = {cracker.key.public}")
            print(f"Private key = {cracker.private_key}")
        if path is not None:
            saved = cracker.save_key(path)
            if not silent and saved:
                print(f"Key saved to '{saved}'")
            elif not silent:
                print(f"Couldn't save  key to: '{saved}'")
    except KeyboardInterrupt:
        if not silent:
            print()
            print(f"Cancelled after {(perf_counter() - ref) : .3f} s.")
