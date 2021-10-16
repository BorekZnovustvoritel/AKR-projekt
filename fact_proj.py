from math import sqrt
from rsa import RSA_key

def rsa_factorization(num):
    max_fact = int(sqrt(num))
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
    print(rsa_factorization(key.mod))
    print("Time in seconds: %.2f" % (perf_counter() - ref))
    input()
