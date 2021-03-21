import os
import lzma
import string
import sys
import time
from itertools import takewhile, dropwhile

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
                sha3_224, sha3_256, sha3_384, sha3_512
   --combo    write plain and hashed text with given separator(only works when --hash is used).
   --mask     Insted of Max and Min Length You Can Use Mask:
                ?l: Alphabet_lower
                ?u: Alphabet_upper
                ?s: Special_chars
                ?d: Digits
   --start    Start from given position
   --end      ِDetermine if script should stop early in given word
   -b         Specifie the size of the output file, (no unit)=bytes, kb, mb, gb
   -z         compres the output with lzma
   -h, --help  Print This Help Message

'''

TABLE = {'?l': string.ascii_uppercase,
         '?u': string.ascii_lowercase,
         '?s': string.punctuation,
         '?d': string.digits}

SIZE_TABLE = {'kb': 1000,
              'mb': 1000**2,
              'gb': 1000 ** 3,
              range(3, 6): 'kb',
              range(6, 9): 'mb',
              range(9, 12): 'gb'}

start_time = time.time()

n = 0  # we are using n to track the number of generated combinations
workingpath = os.getcwd()
WriteToFile = False
Filename = None
MemoryFriendly = False
Chunk = None
Split_File = False
split_bytes = 0  # max size of files before spliting
Part_num = 1  # variable for file name in splited files
current_length = 0
current_size = 0
algo = None
compression = False
Pre = ''
Suf = ''
start = None
end = None
mask = None
combo = False
separator = ''


def unit_convert(byte, to_byte=False, from_byte=False):
    byte = str(byte)
    if to_byte:
        return int(byte[:-2]) * SIZE_TABLE.get(byte[-2:], 0)
    elif from_byte:
        for unit in SIZE_TABLE:
            if isinstance(unit, range) and len(byte) in unit:
                byte = int(byte) // SIZE_TABLE[SIZE_TABLE[unit]]
                return f'{byte}{SIZE_TABLE[unit]}'


def Resume(pools, start=None, end=None, Pre='', Suf=''):  # works but like a turtle, make it better and use it and let me know
    # this function start right from where we determined but as I mentioned it is slow
    result = [[]]
    if start:
        temp_pools = [[start[0]]]
        for s in range(1, len(start)):
            temp_pools.append(pools[s][pools[s].index(start[s]):])
    for pool in temp_pools:
        result = [x+[y] for x in result for y in pool]
    for item in result:
        yield f"{Pre}{''.join(item)}{Suf}\n"
        if ''.join(item) == end:
            break


def Generator(*mystring, Length=1, start=None, end=None, chunk=None, Pre='', Suf=''):  # func for generating combinations
    global current_length
    current_length = Length
    pools = [tuple(pool) for pool in mystring] * Length
    if start:
        pools[0] = pools[0][pools[0].index(start[0]):]  # start generating from character start[0]
    result = [[]]
    if mask is not None:
        for pool in pools:
            result = [i+[j] for i in result for j in pool]
    else:
        for pool in pools:
            result = (i+[j] for i in result for j in pool)

    if start is not None and len(start) == Length:
        result = dropwhile(lambda x: ''.join(x) != start, result)
        # result = Resume(pools, start)
    if end is not None and len(end) == Length:
        result = takewhile(lambda x: ''.join(x) != end, result)

    if not MemoryFriendly:  # we will store 1% of combs every time before writing
        c = []
        for item in result:
            c.append(f"{Pre}{''.join(item)}{Suf}\n")
            if len(c) == chunk:
                yield c
                c.clear()
        if len(c):
            yield c
    else:
        yield from (f"{Pre}{''.join(item)}{Suf}\n" for item in result)


def Gen_mask(mask):  # func for generating mask passwords
    i = 0
    while i+1 < len(mask):
        key = mask[i] + mask[i+1]
        if key in TABLE:
            mask = list(mask.partition(key))
            mask[1] = TABLE[key]
            if mask[0] != '':
                mask[0] = [mask[0]]
            yield from [i for i in mask[:2] if i != '']
            yield from Gen_mask(mask[2])
            break
        elif not any(i in mask for i in TABLE) and mask != '':
            yield [mask]
            break
        i+=1


def Split(Password, Name, byte):
    global Part_num, current_size, n
    while True:
        # gotta be a better way that I can't think about right now
        processed_name = Name.split('.')
        processed_name[0] += str(Part_num)
        processed_name = '.'.join(processed_name)
        with open(processed_name, 'a') as out:
            for item in Password:
                if current_size > byte:
                    out.write(item)
                    n+=1
                    Part_num += 1
                    current_size %= byte
                    break
                current_size += current_length + 2  # +2 is newline character length
                out.write(item)
            else:
                break
            print(f'Writed {unit_convert(split_bytes, from_byte=True)} in {processed_name}')


def Output(Password, algo=None):  # func for wrapping outputs
    global n
    if algo is not None:
        Password = ((item.strip('\n'),
                     ha.new(algo, data=item.strip('\n').encode()).hexdigest())
                    for item in Password)
        if combo:
            Password = (f'{i[0]}{separator}{i[1]}\n' for i in Password)
        else:
            Password = (i[1]+'\n' for i in Password)
    if not WriteToFile:
        for item in Password:
            print(*item, sep='', end='')
    elif WriteToFile:
        if Split_File:
            print('Writing length: ', writing_lenght)
            Split(Password, Filename, split_bytes)
            return
        # else:
        if compression:
            file_obj = lzma.open(Filename+'.xz', 'at', filters=[{'id': lzma.FILTER_LZMA2, "mode": lzma.MODE_FAST}])
        else:
            file_obj = open(Filename, 'a')
        with file_obj as out:
            for item in Password:
                out.writelines(item)
                n += MemoryFriendly or Chunk  # if MemoryFriendly is off then we should increment by chunk length
                if n % (round(all_pos/100) or 1) == 0:
                    print('Working: ', round((n*100)/all_pos), '%', end='\r')


def parse(args):
    global WriteToFile, Filename, MemoryFriendly, algo, Pre, Suf, ha, Split_File, compression
    global mystring, minlength, maxlength, mask, separator, combo, start, end, split_bytes
    if '--help' in sys.argv or '-h' in sys.argv:
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
                import hashlib as ha  # what the hell !? it is a heavy library , import it when you need it
                MemoryFriendly = True  # hashes are too long, saving them in memory is not a good idea
                algo = args[arg+1]
                arg += 1
            elif args[arg] == '--combo':
                combo = True
                if args[arg+1] != '':
                    separator = args[arg+1]
                arg += 1
            elif args[arg] == '--start':
                if all(i in mystring for i in args[arg+1]) and minlength <= len(args[arg+1]) <= maxlength:
                    start = args[arg+1]
                    minlength = len(start)
                    arg+=1
                    continue
                print('Wrong place to start, generating from the beggening...')
            elif args[arg] == '--end':
                if all(i in mystring for i in args[arg+1]) and minlength <= len(args[arg+1]) <= maxlength:
                    end = args[arg+1]
                    maxlength = len(end)
                    arg+=1
                    continue
                print('Wrong place to end, generating from the beggening...')
            elif args[arg] == '-b':
                MemoryFriendly = True  # Trust me we need this
                split_bytes = args[arg+1].lower()
                if split_bytes.isdigit():
                    split_bytes = int(split_bytes)
                else:
                    split_bytes = unit_convert(split_bytes, to_byte=True)
                Split_File = split_bytes and True or False  # 0 bytes means no spliting :\
                arg += 1
            elif args[arg] == '-z':
                compression = True
                Split_File = False  # not a good idea with lzma

            arg += 1


def main():
    global start_time, all_pos, Chunk, writing_lenght

    start_time = time.time()
    if mask is not None:
        len_key = {'@': 26, ',': 26, '%': 10, '$': 36}
        all_pos = 1
        for char in mask:
            if char in len_key:
                all_pos *= len_key[char]
        Chunk = all_pos // 100 or all_pos
        processed_mask = Gen_mask(mask)
        Output(Generator(*processed_mask, start=start, end=end, chunk=Chunk, Pre=Pre, Suf=Suf), algo)
    elif maxlength == minlength:  # generating combinations with same length
        all_pos = len(mystring) ** minlength  # calculatinf all possible combs
        writing_lenght = minlength
        Chunk = all_pos // 100 or all_pos
        Output(Generator(mystring, Length=minlength, start=start, end=end, chunk=Chunk, Pre=Pre, Suf=Suf), algo)
    else:  # generating combinations with diffrent lengths
        if minlength > maxlength:
            print('Min Length Is Bigger Than Max!! Try Again.')
            sys.exit(0)
        all_pos = 0
        for pos in range(minlength, maxlength+1):
            all_pos = all_pos + len(mystring) ** pos
        Chunk = all_pos // 100 or all_pos
        for length in range(minlength, maxlength+1):
            writing_lenght = length
            Output(Generator(mystring, Length=length, start=start, end=end, chunk=Chunk, Pre=Pre, Suf=Suf), algo)


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
    end_time = time.time()
    print(f'\n Ended in: {round(end_time-start_time, 10)} sec')
