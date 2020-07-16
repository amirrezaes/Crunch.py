import sys
import os
import time

intro = '''
Usage: pyrunch.py <min> <max> <characters> <options>

Options:
   -o         Set a Name or Directory for Output File (use -o - for piping the output to aircrack-ng, etc...)
   -m         Memory Friendly mode(slightly slower) [default: off]
   -s suffix  Add a Suffix to Passwords
   -p prefix  Add a Prefix to Passwords
   --hash     Hash Passwords With Given Algorithm:
                md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s,
                sha3_224, sha3_256, sha3_384, sha3_512.
   -h         Print This Help Message

'''
if sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print(intro)
    sys.exit(0)

start = time.time()
n = 0  # we are using n to get number of generated combinations

# getting arguments
mystring = str(sys.argv[3])
minlength = int(sys.argv[1])
maxlength = int(sys.argv[2])
workingpath = os.getcwd()
WriteToFile = False
Filename = None
MemoryFriendly = False
algo = None
Pre = ''
Suf = ''


def Generator(*mystring, Length, algo = None):  # func for generating combinations
    result = [[]]
    recurser = [tuple(iter) for iter in mystring] * Length
    for iter in recurser:
        result = (i+[j] for i in result for j in iter)
    if algo == None:
        yield from result
    else:
        hashed = (ha.new(algo, data=''.join(i).encode()).hexdigest() for i in result)
        yield from hashed


def Output(Password, Pre, Suf):  # func for wrapping outputs
    global n
    if not WriteToFile:  # just printing
        for item in Password:
            print(Pre, *item, Suf, sep='')
    elif WriteToFile:  # writing to file
        with open(Filename, 'a') as out:
            if MemoryFriendly:  # this will not store anything in memory
                for item in Password:
                    out.write(Pre+''.join(item)+Suf+'\n')
                    n+=1
                    if n % round(all_pos/100) == 0:
                        print('Working: ', round((n*100)/all_pos), '%', end='\r')
                return
            chunk = []  # we will store 1% of combs every time before writing
            for item in Password:
                chunk.append(Pre+''.join(item)+Suf+'\n')
                n += 1
                try:
                    if n % round(all_pos/100) == 0:
                        out.writelines(chunk)
                        chunk.clear()
                        print('Working: ', round((n*100)/all_pos), '%', end='\r')
                except ZeroDivisionError:  # if all_pos is less than 50 the round() will turn it to 0 and we will get this error
                    pass
            if len(chunk) > 0:
                out.writelines(chunk)


def parse(args):
    global WriteToFile, Filename, MemoryFriendly, algo, Pre, Suf, ha
    if args != []:
        arg = 0
        while arg < len(args):
            if args[arg] == '-o' or args[arg] == '--output':
                if args[arg+1] == '-':
                    pass
                else:
                    WriteToFile = True
                    if os.path.dirname(args[arg+1]) == '':
                        Filename = workingpath+'\\'+args[arg+1]
                    else:
                        Filename = args[arg+1]
            elif args[arg] == '-m' or args[arg] == '--memory':
                MemoryFriendly = True
            elif args[arg] == '-p' or args[arg] == '--prefix':
                Pre = args[arg+1]
            elif args[arg] == '-s' or args[arg] == '--sufix':
                Suf = args[arg+1]
            elif args[arg] == '--hash':
                import hashlib as ha
                algo = args[arg+1]
            arg += 1
def main():
    global start, all_pos

    start = time.time()
    if maxlength == minlength:  # generating combinations with same length
        all_pos = len(mystring) ** minlength  # calculatinf all possible combs
        Output(Generator(mystring, Length=minlength, algo=algo), Pre, Suf)
    else:  # generating combinations with diffrent lengths
        if minlength > maxlength:
            print('Min Length Is Bigger Than Max!! Try Again.')
            sys.exit(0)
        all_pos = 0
        for pos in range(minlength, maxlength+1):
            all_pos = all_pos + len(mystring) ** pos
        for length in range(minlength, maxlength+1):
            Output(Generator(mystring, Length=length, algo=algo), Pre, Suf)


if __name__ == '__main__':
    try:
        parse(sys.argv[4:])
        main()
    except (NameError, IndexError, ValueError) as er:
        print(er)
        print("Incorrect Arguments use -h or --help for help.")
    except KeyboardInterrupt:
        print("Stoped")
    except MemoryError:
        print("Memory is Full, Use Memory Friendly Mode")
    finally:
        end = time.time()
        print('\n', 'Ended in: ', round(end-start, 10), 'sec')
