from functionalities.rsa import RSA_key
from functionalities.fact_proj import RSA_cracker
from time import perf_counter

logo = """
  _____   _____            _____                _             
 |  __ \ / ____|  /\      / ____|              | |            
 | |__) | (___   /  \    | |     _ __ __ _  ___| | _____ _ __ 
 |  _  / \___ \ / /\ \   | |    | '__/ _` |/ __| |/ / _ \ '__|
 | | \ \ ____) / ____ \  | |____| | | (_| | (__|   <  __/ |   
 |_|  \_\_____/_/    \_\  \_____|_|  \__,_|\___|_|\_\___|_|   
                                                              
                                                              """
minimal_bitlength = 8
def _crack(key: RSA_key):
    cracker = RSA_cracker(key)
    print(f"Assigned cores: {cracker.cores}")
    ref = perf_counter()
    try:
        cracker.start()
        print(f"Found primes: {cracker.p}, {cracker.q}.")
        print(f"Found private exponent: {cracker.private_key}.")
        print(f"Private key in hex: {hex(cracker.private_key)}")
        print(f"Cracking took: {(perf_counter() - ref) : .3f} s.")
        # TODO implementace JSON ukládání
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
            while inp < minimal_bitlength:
                try:
                    inp = int(input(f"Enter bitlength of the RSA modulo that is greater or equal to {minimal_bitlength}: "))
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