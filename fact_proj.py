from rsa import RSA_key
from Crypto.Util import number
from sqroot import sqroot
import multiprocessing
from time import perf_counter

class RSA_cracker():
    def __init__(self, key: RSA_key):
        self.cores: int = multiprocessing.cpu_count()
        self.key: RSA_key = key
        self.queue: multiprocessing.Queue = multiprocessing.Queue()
        self.p: int = 0
        self.q: int = 0
        self.timers_per_thousand: list = []
        self.biggest: int = sqroot(self.key.mod)
        self.smallest: int = 2**((key.bitlength//2)-1)
        self.number_count_per_proces: int = (self.biggest - self.smallest) // self.cores
        self.starting_points: list = [int(self.biggest)]
        for core in range(self.cores - 1):
            self.starting_points.append(self.starting_points[-1] - self.number_count_per_proces)
        self.private_key: int = None


    def factorization(self, starting_point: int):
        max_fact = starting_point
        if max_fact % 2 == 0:
            max_fact -= 1
        res = max_fact % 1000
        ref = perf_counter()
        last_stop = 0
        for i in range(max_fact, 1, -2):
            if self.key.mod % i == 0:
                self.queue.put([i, self.key.mod//i])
            if i % 1000 == res:
                self.queue.put(perf_counter() - ref)
                last_stop = i
                break
        for i in range(last_stop, 1, -2):
            if self.key.mod % i == 0:
                self.queue.put([i, self.key.mod//i])

    def stop(self, processes):
        for process in processes:
            process.terminate()

    def start(self):
        print("Cracking, please wait...")
        processes = []
        for i in range(self.cores):
            pr = multiprocessing.Process(target=self.factorization, args=(self.starting_points[i],))
            processes.append(pr)
            pr.start()
        temp = None
        while temp is None:
            temp = self.queue.get()
            if isinstance(temp, list) and len(temp) == 2:
                self.p, self.q = temp
                break
            if isinstance(temp, float):
                self.timers_per_thousand.append(temp)
                if len(self.timers_per_thousand) == self.cores:
                    avg_time = sum(self.timers_per_thousand) / self.cores
                    print(f"Estimated time: {avg_time * ((self.biggest - self.smallest) // 1000) : .3f} s.")
            temp = None
        self.stop(processes)
        self.private_key = number.inverse(self.key.public, (self.p - 1) * (self.q - 1))


if __name__ == "__main__":
    bitlength = abs(int(input("Enter bitlength of modulo:  ")))
    key = RSA_key().generate(bitlength)
    print(f"Modulo is: {key.mod}")
    print(f"Public exponent is: {key.public}")
    cracker = RSA_cracker(key)
    ref = perf_counter()
    cracker.start()
    print(f"Found primes: {cracker.p}, {cracker.q}")
    print(f"Found private exponent: {cracker.private_key}")
    print("Time in seconds: %.2f" % (perf_counter() - ref))
    input("Program finished, press enter.")
