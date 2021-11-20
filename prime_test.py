def fermat(num):
    a = False
    b = False
    if ((2 ** num) - 2) % num == 0:
        a = True
    if (2 ** (num - 1) % num) == 1:
        b = True
    if a & b is True:
        return True
    else:
        return False