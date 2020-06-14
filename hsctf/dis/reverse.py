""" Links Used """
""" General Reference of Instructions: https://docs.python.org/3/library/dis.html """
""" Basics of How Bytecodes Work: https://opensource.com/article/18/4/introduction-python-bytecode """
""" Basics of Reversing Bytecode: https://chriswarrick.com/blog/2017/08/03/gynvaels-mission-11-en-python-bytecode-reverse-engineering/ """
""" How List Comphrehension Works: https://stackoverflow.com/questions/38941643/how-does-list-comprehension-exactly-work-in-python """
""" What's yield: https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do """

def e(s):
    s2 = []
    for char in s:
        s2.append(char)
    
    o = []
    for char in s2:
        o.append((char + 30) ^ 5)

    string = ""
    for char in o:
        string += (chr(int((char + 50 + 60 - 5)/3)))
    
    print(string)

    #return bytes(o)
         

def main():
    o = b'\xae\xc0\xa1\xab\xef\x15\xd8\xca\x18\xc6\xab\x17\x93\xa8\x11\xd7\x18\x15\xd7\x17\xbd\x9a\xc0\xe9\x93\x11\xa7\x04\xa1\x1c\x1c\xed'
    
    #o = b'\xa1\x9a\xa7\xa8\xa5\xae'
    e(o)
        
main()
