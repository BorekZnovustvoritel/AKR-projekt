from rsa import RSA_key
from fact_proj import RSA_cracker
from time import perf_counter

logo = """
  _____   _____            _____                _             
 |  __ \ / ____|  /\      / ____|              | |            
 | |__) | (___   /  \    | |     _ __ __ _  ___| | _____ _ __ 
 |  _  / \___ \ / /\ \   | |    | '__/ _` |/ __| |/ / _ \ '__|
 | | \ \ ____) / ____ \  | |____| | | (_| | (__|   <  __/ |   
 |_|  \_\_____/_/    \_\  \_____|_|  \__,_|\___|_|\_\___|_|   
                                                              
                                                              """
if __name__ == "__main__":
    print(logo)
    inp = None
    while inp != 1 and inp != 2:
        try:
            inp = int(input("Enter 1 if you want to showcase, 2 if you want to crack: "))
        except ValueError:
            continue
    if inp == 1:
        inp = 0
        while inp < 6:
            try:
                inp = int(input("Enter bitlength of the RSA modulo: "))
            except ValueError:
                continue
        key = RSA_key().generate(inp)
        print(f"Generated key:")
        print(f"Modulo: {key.mod}")
        print(f"Public key {key.public}")
        cracker = RSA_cracker(key)
        print(f"Assigned cores: {cracker.cores}")
        ref = perf_counter()
        cracker.start()
        print(f"Found primes: {cracker.p}, {cracker.q}")
        print(f"Found private exponent: {cracker.private_key}")
        print(f"Cracking took: {(perf_counter() - ref) : .3f} s.")
        input("Program finished, press enter.")

    else:
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
        cracker = RSA_cracker(key)
        print(f"Assigned cores: {cracker.cores}")
        ref = perf_counter()
        cracker.start()
        print(f"Found primes: {cracker.p}, {cracker.q}")
        print(f"Found private exponent: {cracker.private_key}")
        print(f"Cracking took: {(perf_counter() - ref) : .3f} s.")
        input("Program finished, press enter.")