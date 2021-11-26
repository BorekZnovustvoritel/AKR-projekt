from functionalities.rsa import RSA_key
from functionalities.fact_proj import RSA_cracker
from time import perf_counter
from functionalities.resources import logo, minimal_bitlength

def _crack(key: RSA_key):
    cracker = RSA_cracker(key)
    print(f"Assigned cores: {cracker.cores}")
    ref = perf_counter()
    try:
        print("Cracking, please wait...")
        cracker.start()
        print(f"Found primes: {cracker.p}, {cracker.q}.")
        print(f"Found private exponent: {cracker.private_key}.")
        print(f"Cracking took: {(perf_counter() - ref) : .3f} s.")
        path = input("Enter name of file to save this key. Dismiss by pressing just enter.")
        if path != "":
            path = cracker.save_key(path)
            if path:
                print(f"Key saved to '{path}'")
            else:
                print(f"Couldn't save  key to: '{path}'")
    except KeyboardInterrupt:
        print(f"Cancelled after {(perf_counter() - ref) : .3f} s.")

if __name__ == "__main__":
    print(logo)
    esc = False
    while not esc:
        inp = None
        while inp != 1 and inp != 2:
            try:
                inp = int(input("Enter 1 if you want to showcase, 2 if you want to crack: "))
            except ValueError:
                continue
        #MAIN SWITCH
        if inp == 1: #SHOWCASE
            inp = 0
            while inp < minimal_bitlength or inp % 2 == 1:
                try:
                    inp = int(input(f"Enter bitlength of the RSA modulo that is greater or equal to {minimal_bitlength} (must be even): "))
                except ValueError:
                    continue
            key = RSA_key().generate(inp)
            print("Generated key:")
            print(f"Modulo: {key.mod}")
            print(f"Public key {key.public}")
            _crack(key)
            temp = input("Enter '1' to run again.")
            if temp != '1':
                esc = True

        else: #CRACK EXTERNAL KEY
            mod = 0
            while mod < 33:
                try:
                    mod = int(input("Enter modulo of the RSA cryptosystem: "))
                except ValueError:
                    continue
            pub = 0
            while pub < 2:
                temp = input(f"Enter public key. Leave blank for value {RSA_key.default_pub}: ")
                if temp == '':
                    pub = RSA_key.default_pub
                    break
                try:
                    pub = int(temp)
                except ValueError:
                    continue
            key = RSA_key().upload(mod, pub)
            _crack(key)
            temp = input("Enter '1' to run again.")
            if temp != '1':
                esc = True