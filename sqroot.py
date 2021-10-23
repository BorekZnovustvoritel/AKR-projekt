
def sqroot(num):
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

            i = i/10
        else:
            while((pow(root,2)) > num):
                root = int(root) - int(i)
    return root

root = (sqroot(int(input())))
print(str(root*root))
print(str(root))