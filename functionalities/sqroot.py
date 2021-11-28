def sqroot(num):
    """Natural square root (decimal points are ignored).
    Needed because math.sqrt breaks with numbers bigger than 2 to the power of 1024."""
    lenght = len(str(num))#convert number to string
    half = str(num)[0:(lenght//2)]#create a substring that is roughly a half of the number
    i = (int("1" + "0" * (lenght//2)))
    root = int(half)#convert the substring into number
    while(True):#infinite loop that adds and substracts until the root equals the root of number (without decimals)
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
