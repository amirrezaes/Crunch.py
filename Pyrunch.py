import sys
import os
import time
from itertools import product as p

intro = '''
Usage: pyrunch.py <min> <max> <characters> <options>
       or
       pyrunch.py --mask <mask> <options>
Options:
   -o         Set a Name or Directory for Output File (use -o - for piping the output to aircrack-ng, etc...)
   -m         Memory Friendly mode(slightly slower) [default: off]
   -s suffix  Add a Suffix to Passwords
   -p prefix  Add a Prefix to Passwords
   --hash     Hash Passwords With Given Algorithm:
                md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s,
                sha3_224, sha3_256, sha3_384, sha3_512.
   --combo    write plain and hashed text with given separator(only works when --hash is used).
   --mask     Insted of Max and Min Length You Can Use Mask:
                ?l: Alphabet_lower
                ?u: Alphabet_upper
                ?s: Special_chars
                ?d: Digits
   -h         Print This Help Message

'''

alpha_u = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha_l = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'
symbol = """!@#$%^&*()_+-=,.`~[]\{}|;':"/<>?"""
table = {'?l': alpha_l, '?u': alpha_u, '?s': symbol, '?d': numbers}
start = time.time()

n = 0  # we are using n to track the number of generated combinations
workingpath = os.getcwd()
WriteToFile = False
Filename = None
MemoryFriendly = False
algo = None
Pre = ''
Suf = ''
mask = None
combo = False
separator = ''


def Generator(*mystring, Length=1, algo=None):  # func for generating combinations
    result = [[]]
    recurser = [tuple(iter) for iter in mystring] * Length
    for iter in recurser:
        result = (i+[j] for i in result for j in iter)
    if algo is not None:
        hashed = ((''.join(i), ha.new(algo, data=''.join(i).encode()).hexdigest()) for i in result)
        yield from hashed
    yield from result


def Gen_mask(mask):  # func for generating mask passwords
    i = 0
    while i+1 < len(mask):
        key = mask[i] + mask[i+1]
        if key in table:
            mask = list(mask.partition(key))
            mask[1] = table[key]
            if mask[0] != '': mask[0] = [mask[0]]
            yield from [i for i in mask[:2] if i != '']
            yield from Gen_mask(mask[2])
            break
        elif not any(i in mask for i in table) and mask != '':
            yield [mask]
            break
        i+=1


def Output(Password, Pre='', Suf=''):  # func for wrapping outputs
    global n
    if combo:
        Password = (i[0]+separator+i[1] for i in Password)
    elif algo is not None:
        Password = (i[1] for i in Password)
    else:
        Password = (''.join(i) for i in Password)

    if not WriteToFile:  # just printing
        for item in Password:
            print(f'{Pre}{item}{Suf}')
    elif WriteToFile:  # writing to file
        with open(Filename, 'a') as out:
            if MemoryFriendly:  # this will not store anything in memory
                for item in Password:
                    out.write(Pre+item+Suf+'\n')
                    n+=1
                    if n % round(all_pos/100) == 0:
                        print('Working: ', round((n*100)/all_pos), '%', end='\r')
                return
            chunk = []  # we will store 1% of combs every time before writing
            for item in Password:
                chunk.append(Pre+item+Suf+'\n')
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
    global mystring, minlength, maxlength, mask, separator, combo
    if '-h' in args or '--help' in args or '-h' in sys.argv[1:2]:
        print(intro)
        sys.exit(0)
    if '--mask' in sys.argv:
        mask = sys.argv[sys.argv.index('--mask') + 1]
        args = sys.argv[2:]
    else:
        mystring = str(sys.argv[3])
        minlength = int(sys.argv[1])
        maxlength = int(sys.argv[2])
    if args != []:
        arg = 0
        while arg < len(args):
            if args[arg] == '-o' or args[arg] == '--output':
                if args[arg+1] == '-':
                    pass
                else:
                    WriteToFile = True
                    Filename = args[arg+1]
                arg += 1
            elif args[arg] == '-m' or args[arg] == '--memory':
                MemoryFriendly = True
            elif args[arg] == '-p' or args[arg] == '--prefix':
                Pre = args[arg+1]
                arg += 1
            elif args[arg] == '-s' or args[arg] == '--sufix':
                Suf = args[arg+1]
                arg += 1
            elif args[arg] == '--hash':
                import hashlib as ha
                algo = args[arg+1]
                arg += 1
            elif args[arg] == '--combo':
                combo = True
                if args[arg+1] != '':
                    separator = args[arg+1]
            arg += 1


def main():
    global start, all_pos

    start = time.time()
    if mask is not None:
        len_key = {'@': 26, ',': 26, '%': 10, '$': 36}
        all_pos = 1
        for char in mask:
            if char in len_key:
                all_pos *= len_key[char]
        processed_mask = Gen_mask(mask)
        Output(p(*processed_mask))
    elif maxlength == minlength:  # generating combinations with same length
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
    except (NameError, IndexError, ValueError):
        print("Incorrect Arguments use -h or --help for help.")
    except KeyboardInterrupt:
        print("\nStoped")
    except MemoryError:
        print("Memory is Full, Use Memory Friendly Mode")
    finally:
        end = time.time()
        print(f'\n Ended in: {round(end-start, 10)} sec')
