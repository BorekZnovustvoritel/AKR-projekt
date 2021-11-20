def fermat(num):
    if ((2 ** num) - 2) % num == 0:
        return True
    else: return False

def gen_primes(maxnum):
    if maxnum % 2 == 0:
        maxnum -= 1
    num = maxnum
    while num > 1:
        if fermat(num):
            yield num
        num -= 2