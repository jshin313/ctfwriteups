""" Links Used """
""" General Reference of Instructions: https://docs.python.org/3/library/dis.html """
""" Basics of How Bytecodes Work: https://opensource.com/article/18/4/introduction-python-bytecode """
""" Basics of Reversing Bytecode: https://chriswarrick.com/blog/2017/08/03/gynvaels-mission-11-en-python-bytecode-reverse-engineering/ """
""" How List Comphrehension Works: https://stackoverflow.com/questions/38941643/how-does-list-comprehension-exactly-work-in-python """
""" What's yield: https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do """

def a(s):
    o = [0] * len(s)

    for i, char in enumerate(s):
        o[i] = (char * 2) - 60

    return o

def b(s, t):
    for x, y in zip(s, t):
        yield (x + y) - 50


def c(s):
    return [c + 5 for c in s]

def e(s):
    s = [ord(c) for c in s]

    o = [(c ^ 5) - 30 for c in b(a(s), c(s))]
    
    return bytes(o)
         

def main():
    s = input('Guess?')
    o = b'\xae\xc0\xa1\xab\xef\x15\xd8\xca\x18\xc6\xab\x17\x93\xa8\x11\xd7\x18\x15\xd7\x17\xbd\x9a\xc0\xe9\x93\x11\xa7\x04\xa1\x1c\x1c\xed'
    
    if e(s) == o:
        print('Correct!')
    else:
        print('Wrong...') 
    return None
        
main()
