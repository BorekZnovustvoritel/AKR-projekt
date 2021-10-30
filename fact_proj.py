from rsa import RSA_key
from Crypto.Util import number
from sqroot import sqroot
import multiprocessing
from time import perf_counter, sleep
from math import floor

def rsa_factorization(num: int, starting_point: int, queue: multiprocessing.Queue):
    max_fact = starting_point
    if max_fact % 2 == 0:
        max_fact -= 1
    for i in range(max_fact, 1, -2):
        if num % i == 0:
            #return [i, num//i]
            queue.put([i, num//i])

if __name__ == "__main__":
    bitlength = abs(int(input("Insert bitlength of modulo:  ")))
    key = RSA_key(bitlength)
    print(f"Modulo is: {key.mod}")
    print(f"Public exponent is: {key.public}")
    ref = perf_counter()
    print("Cracking, please wait...")
    #p, q = rsa_factorization(key.mod, sqroot(key.mod))
    queue = multiprocessing.Queue()
    cpus = floor(0.75 * multiprocessing.cpu_count())
    smallest = 2**((bitlength//2)-1)
    biggest = sqroot(key.mod)
    number_count = biggest - smallest
    number_count_per_process = number_count//cpus
    processes = []
    print(f"Assigned cores: {cpus}")
    for cpu in range(cpus):
        pr = multiprocessing.Process(target=rsa_factorization, args=(key.mod, biggest, queue))
        processes.append(pr)
        pr.start()
        biggest = biggest - number_count_per_process
    p = 0
    q = 0
    while p == 0:
        sleep(0.1)
        p, q = queue.get()
    for pr in processes:
        pr.terminate()
    print([p, q])
    print("Time in seconds: %.2f" % (perf_counter() - ref))
    print("Generating Private key...")
    priv_key = number.inverse(key.public, (p - 1) * (q - 1))
    print(f"Private key is: {priv_key}")
    input("Program finished, press enter.")
