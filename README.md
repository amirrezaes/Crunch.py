# Pyrunch
Python script for crunch

It is not as fast as the orginal crunch which is written in C but it is definitely faster than https://github.com/derv82/werdy/blob/master/crunch.py .
I will add multiprocessing in future.

    Usage: pyrunch.py <min> <max> <characters> <options>

    Options:
       -o         Set a name or directory for output file
       -m         Memory Friendly mode(slightly slower) [default: off]
       -s suffix  Add a Suffix to Passwords
       -p prefix  Add a Prefix to Passwords
       --hash     Hash Passwords With Given algo:
                    md5(), sha1(), sha224(), sha256(), sha384(), sha512(), blake2b(), blake2s(),
                    sha3_224, sha3_256, sha3_384, sha3_512, shake_128, and shake_256.
       -h         Show help command

![](gif.gif)
