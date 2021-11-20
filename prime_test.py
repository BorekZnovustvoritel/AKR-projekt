def fermat(num):
    if ((2 ** num) - 2) % num == 0:
        return True
    else: return False