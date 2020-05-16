import sys, os


auto = False

List = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|', '!', '@', '#', '$', '', '^', '%', '&', '*', '(', ')', '_', '`', '~', '+'," "]


try:
    path = sys.argv[1]
    #path = "Test.tst"
    newPath = ""
    encrypt = sys.argv[3]
    auto = True



    for x in range(len(path)-1,0,-1):
        if path[x] == ".":
            newPath = path[:x]

    if encrypt == "enc":
        newPath += ".enc"
    if encrypt == "dec":
        newPath += ".tst"

except:
    pass
    

def Encrypt(string, key):
    encryption = ""
    for i,c in enumerate(string):
        keyB = List.index(key[i % len(key)])
        stringB = List.index(c)
        char = List[(stringB + keyB) % len(List)]
        encryption += char
    return encryption

def Decrypt(encrypt, key):
    string = ""
    for i,c in enumerate(encrypt):
        keyB = List.index(key[i % len(key)])
        encryptB = List.index(c)
        char = List[(encryptB - keyB) % len(List)]
        string += char
    return string


if __name__ == "__main__":
    while True:
        print(Encrypt(input("Message: "),"my_key"))
        print(Decrypt(input("Decrypt: "),"my_key"))
        a = input("press any key to continue...")
elif auto:
    
    file = open(path,"r")
    lines = file.readlines()
    file.close()
    
    newLines = []

    for line in lines:
        if encrypt == "enc":
            a = Encrypt(line,sys.argv[2])
        else:
            a = Decrypt(line,sys.argv[2])
        #a = Encrypt(line,"this_is_my_key")
        newLines.append(str(a))
    
    file = open(path,"w")
    
    for x in newLines:
        file.write(x)
    
    file.close()
    
    os.rename(path,newPath)