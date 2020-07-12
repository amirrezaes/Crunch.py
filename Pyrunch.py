import sys
import os
import time

intro = '''
Usage: pyrunch.py <min> <max> <characters> <options>

Options:
   -o         Set a name or directory for output file [defult: Script Path]
   -m         Memory Friendly mode(slightly slower) [default: off]
   -h         Show help command

'''

start = time.time()
n = 0  # we are using n to get number of generated combinations


def Generator(*mystring, Length):  # func for generating combinations
    result = [[]]
    recurser = [tuple(iter) for iter in mystring] * Length
    for iter in recurser:
        result = (i+[j] for i in result for j in iter)
    yield from result


def Output(Password):  # func for wrapping outps
    global n
    if not WriteToFile:  # just printing
        for item in Password:
            print(*item, sep='')
    elif WriteToFile:  # writing to file
        with open(Filename, 'a') as out:
            if MemoryFriendly:  # this will not store anything in memory
                for item in Password:
                    out.write(''.join(item)+'\n')
                    n+=1
                    if n % round(all_pos/100) == 0:
                        print('Working: ', round((n*100)/all_pos), '%', end='\r')
                return
            chunk = []  # we will store 1% of combs every time before writing
            for item in Password:
                chunk.append(''.join(item)+'\n')
                n += 1
                if n % round(all_pos/100) == 0:
                    out.writelines(chunk)
                    chunk.clear()
                    print('Working: ', round((n*100)/all_pos), '%', end='\r')
            if len(chunk) > 0:
                out.writelines(chunk)


try:
    if sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print(intro)
        sys.exit(0)
    # getting arguments
    mystring = str(sys.argv[3])
    minlength = int(sys.argv[1])
    maxlength = int(sys.argv[2])
    workingpath = os.path.dirname(sys.argv[0])
    WriteToFile = False
    Filename = None
    MemoryFriendly = False
    args = sys.argv[4:]
    if args != []:
        arg = 0
        while arg < len(args):
            if args[arg] == '-o' or args[arg] == '--output':
                WriteToFile = True
                if os.path.dirname(args[arg+1]) == '':
                    Filename = workingpath+'\\'+args[arg+1]
                else:
                    Filename = args[arg+1]
            elif args[arg] == '-m' or args[arg] == '--memory':
                MemoryFriendly = True
            arg += 1

    start = time.time()

    if maxlength == minlength:  # generating combinations with same length
        all_pos = len(mystring) ** minlength  # calculatinf all possible combs
        Output(Generator(mystring, Length=minlength))
    else:  # generating combinations with diffrent lengths
        if minlength > maxlength:
            print('Min Length Is Bigger Than Max!! Try Again.')
            sys.exit(0)
        all_pos = 0
        for pos in range(minlength, maxlength+1):
            all_pos = all_pos + len(mystring) ** pos
        for length in range(minlength, maxlength+1):
            Output(Generator(mystring, Length=length))
except (NameError, IndexError, ValueError):
    print("Incorrect Arguments use -h or --help for help.")
except KeyboardInterrupt:
    print("Stoped")
except MemoryError:
    print("Memory is Full, Use Memory Friendly Mode")
finally:
    end = time.time()
    print('\n', 'Ended in: ', round(end-start, 10), 'sec')
