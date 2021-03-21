# Pyrunch
Python script for crunch

It is not as fast as the orginal crunch which is written in C but it is definitely fast among other worldlist generators.
I'm not using the itertools.product, just to keep things pure.

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
       -z         compress the output with lzma
       -h, --help  Print This Help Message

![](gif.gif)
