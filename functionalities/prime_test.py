def fermat(num):
    """Runs a number through 1 simplified iteration of Fermat's test."""
    if ((2 ** num) - 2) % num == 0:
        return True
    else: return False

def gen_primes(maxnum):
    """Generates primes using fermat"""
    if maxnum % 2 == 0: # finds odd number
        maxnum -= 1
    num = maxnum
    while num > 1: # iterates from higher to smaller numbers
        if fermat(num):
            yield num
        num -= 2