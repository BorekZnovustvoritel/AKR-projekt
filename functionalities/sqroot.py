def sqroot(num):
    """Natural square root (decimal points are ignored).
    Needed because math.sqrt breaks with numbers bigger than 2 to the power of 1024."""
    lenght = len(str(num))
    half = str(num)[0:(lenght//2)]
    #print(half)
    i = (int("1" + "0" * (lenght//2)))
    #print(i)
    root = int(half)
    while(True):
        if(i < 1):
            break
        if(((pow(root,2))>= (num-1)) and (pow(root,2)<= (num+1))):
            break
        elif((pow(root,2)) < (num)):
            while((pow(root,2)) < num):
                root = int(root) + int(i)

            i = i//10
        else:
            while((pow(root,2)) > num):
                root = int(root) - int(i)
    return root

if __name__ == "__main__":
    root = (sqroot(int(input())))
    print(str(root*root))
    print(str(root))