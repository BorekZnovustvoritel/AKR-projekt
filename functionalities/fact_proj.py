from functionalities.rsa import RSA_key
from Crypto.Util import number
from functionalities.sqroot import sqroot
import multiprocessing
from time import perf_counter
from functionalities.time_format import time_format
from functionalities.prime_test import gen_primes
import json

class RSA_cracker():
    """Class for the actual cracker. The constructor requires a RSA public key to initiate this object."""
    def __init__(self, key: RSA_key):
        self.cores: int = multiprocessing.cpu_count() # num of cores == num of spawned processes
        self.key: RSA_key = key
        self.queue: multiprocessing.Queue = multiprocessing.Queue() # a way to output from multiprocessing
        self.p: int = 0 # prime 1
        self.q: int = 0 # prime 2
        self.timers_per_thousand: list = [] # every process measures the time it takes to iterate through 1000 numbers. Used for time estimation
        self.biggest: int = sqroot(self.key.mod) # biggest possible prime number
        self.smallest: int = 2**((key.bitlength//2)-1) # smallest possible prime number
        self.number_count_per_proces: int = (self.biggest - self.smallest) // self.cores # how many numbers there is per core?
        self.starting_points: list = [int(self.biggest)] # starting points for different cores in order to split the huge number interval between cores
        for core in range(self.cores - 1):
            self.starting_points.append(self.starting_points[-1] - self.number_count_per_proces) # here we fill it
        self.private_key: int = None # output

    def factorization(self, starting_point: int):
        """Method that cracks the modulo. Is passed to a multiprocessing library."""
        max_fact = starting_point
        if max_fact % 2 == 0:
            max_fact -= 1 # we want to start on an odd number
        res = max_fact % 1000 # residuum after dividing by 1000 (to find the point where we stop measuring time)
        ref = perf_counter() # time reference
        last_stop = 0 # where do we stop measuring time and start going full speed
        for i in range(max_fact, 1, -2): # loop with time measuring, hopping on odd numbers from higher to lower
            if self.key.mod % i == 0: # have we found the prime number?
                self.queue.put([i, self.key.mod//i]) # we output list of the 2 primes
            if i % 1000 == res: # have we reached 1000 iterations yet?
                self.queue.put(perf_counter() - ref) # we output it into the same queue in order not to wait for time measurement when answer has already been found
                last_stop = i # save where we interrupt the loop
                break
        for i in range(last_stop, 1, -2): # countinue cracking at full speed
            if self.key.mod % i == 0:
                self.queue.put([i, self.key.mod//i])

    def factorization_with_prime_test(self, starting_point: int):
        """Discontinued, experimental, slower version of factorization. Do not use this!"""
        ref = perf_counter()
        last_stop = 0
        for i in gen_primes(starting_point): # uses primetest: gen_primes to generate numbers to iterate through.
            if self.key.mod % i == 0:
                self.queue.put([i, self.key.mod // i])
            if starting_point - i >= 1000: # we cannot measuer the 1000 numbers exactly here because we skip a lot of numbers
                self.queue.put(perf_counter() - ref)
                last_stop = i
                break
        for i in gen_primes(last_stop): # same logic as in factorization
            if self.key.mod % i == 0:
                self.queue.put([i, self.key.mod//i])

    def stop(self, processes): # processes cannot be a cracker's attribute due to a bug on MS Windows' implementation of Python 3.9 and newer
        """Takes Iterable of cracker's processes and stops them."""
        for process in processes:
            process.terminate()

    def start(self, with_prime_test: bool = False, silent: bool = False):
        """Start the cracker. Please do not use the version with prime test."""
        processes = [] # list of processes in order to stop them when needed
        for i in range(self.cores): # MULTIPROCESSING LOGIC
            pr: multiprocessing.Process = None
            if with_prime_test: # seriously pls don't use this, it froze my PC
                pr = multiprocessing.Process(target=self.factorization_with_prime_test, args=(self.starting_points[i],))
            else: # this is much better and resource-light
                pr = multiprocessing.Process(target=self.factorization, args=(self.starting_points[i],))
            processes.append(pr)
            pr.start()
        try: # to gracefully stop when being KeyboardInterrupted
            temp = None # temporary variable that reads from the multiprocessing queue and sorts answer from time estimates
            while temp is None: # we basically just cycle through and await the answers from the queue
                temp = self.queue.get()
                if isinstance(temp, list) and len(temp) == 2: # this means that in the queue is a list of the 2 primes
                    self.p, self.q = temp
                    break # no need to continue, we got the answer
                if isinstance(temp, float): # in the queue is a time period per 1000 iterated numbers of one of the cores
                    self.timers_per_thousand.append(temp)
                    if len(self.timers_per_thousand) == self.cores: # if the list is full (every core provided an answer)
                        avg_time = sum(self.timers_per_thousand) / self.cores # average time from the list
                        avg_time = avg_time * ((self.biggest - self.smallest) // 1000) # how long would it take to go through the whole interval at this speed?
                        if not silent: # used in cli.py, if you don't want any output, you won't get it. Ez pz
                            print(f"Estimated time: {time_format(avg_time)}")
                temp = None # we delete the temporary variable and await another outputs from the queue
            self.private_key = number.inverse(self.key.public, (self.p - 1) * (self.q - 1)) # private key calculation
        finally: # here we kill all processes
            self.stop(processes)

    def save_key(self, path: str):
        """Save the RSA key to a JSON file. Returns True if the saving went through, False otherwise."""
        if not path.endswith(".json"):
            path += ".json"
        try:
            with open(path, 'w') as out:
                jstream = {"rsa_modulo": self.key.mod, "rsa_public_exponent": self.key.public, "rsa_private_key": self.private_key}
                out.write(json.dumps(jstream))
            return path
        except IOError:
            return False

if __name__ == "__main__": # testing purposes
    bitlength = abs(int(input("Enter bitlength of modulo:  ")))
    key = RSA_key().generate(bitlength)
    print(f"Modulo is: {key.mod}")
    print(f"Public exponent is: {key.public}")
    cracker = RSA_cracker(key)
    ref = perf_counter()
    print("Cracking, please wait...")
    cracker.start()
    print(f"Found primes: {cracker.p}, {cracker.q}")
    print(f"Found private exponent: {cracker.private_key}")
    print("Time in seconds: %.2f" % (perf_counter() - ref))
    input("Program finished, press enter.")
