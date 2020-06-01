import sys
import os
intro = '''
Usage: pylist.py <min> <max> <characters> <options>
Options:
   -o         Set a name or directory for output file (defult is script directory)
   -h         Show help command
   
'''


def Generator(*mystring, Length):
    result = [[]]
    recurser = [tuple(iter) for iter in mystring] * Length
    for iter in recurser:
        result = (i+[j] for i in result for j in iter)
    for output in result:
        yield tuple(output)


def Output(Password, WriteToFile, Filename):
    if not WriteToFile:
        for item in Password:
            print(*item, sep='')
    elif WriteToFile:
        with open(Filename, 'w') as out:
            for item in Password:
                out.write(''.join(item)+'\n')

try:
    if '-h' in sys.argv[0:]:
        print(intro)
        sys.exit(0)
    mystring = str(sys.argv[3])
    minlength = int(sys.argv[1])
    maxlength = int(sys.argv[2])
    workingpath = os.path.dirname(sys.argv[0])
    WriteToFile = False
    Filename = False
    if '-o' in sys.argv[0:]:
        WriteToFile = True
        if os.path.dirname(sys.argv[5]) == '':
            Filename = workingpath+'\\'+sys.argv[5]
        else:
            Filename = sys.argv[5]
    if maxlength == minlength:
        Output(Generator(mystring, Length=minlength), WriteToFile=WriteToFile, Filename=Filename)
    else:
        if minlength > maxlength:
            raise Exception('Min Length Is Bigger Than Max Try Again')
        else:
            for length in range(minlength, maxlength+1):
                Output(Generator(mystring, Length=length), WriteToFile=WriteToFile, Filename=Filename)
except (NameError, IndexError):
    print("Incorrect Arguments use -h for help")
except KeyboardInterrupt:
    print("Stoped")
finally:
    print("Closing...")
