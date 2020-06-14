def xor(s1,s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def encrypt(a):
    some_text = a[::2]

    randnum = 14
    text_length = len(some_text)
    endtext = ""
    for i in range(1, text_length + 1):
      weirdtext = some_text[i - 1]
      if weirdtext >= "a" and weirdtext <= "z":
          weirdtext = chr(ord(weirdtext) + randnum)
          if weirdtext > "z":
              weirdtext = chr(ord(weirdtext) - 26)
      endtext += weirdtext
    randtext = a[1::2]

    xored = xor("aaaaaaaaaaaaaaa", randtext)
    hex_xored = xored.encode("utf-8").hex()

    return endtext + hex_xored

def decrypt():
    a="fqtbjfub4uj_0_d00151a52523e510f3e50521814141c"

    #some_text = a[::2]
    some_text = a[:15]
    print(some_text)
    randnum = 14
    text_length = len(some_text)
    endtext = ""
    for i in range(1, text_length + 1):
      weirdtext = some_text[i - 1]
      if weirdtext >= "a" and weirdtext <= "z":
          weirdtext = chr(ord(weirdtext) - randnum)
          if weirdtext < "a" or weirdtext > "z":
              weirdtext = chr(ord(weirdtext) +  26)
      endtext += weirdtext
    #randtext = a[1::2]
    randtext = a[15:]
    print(randtext)

    randtext = bytearray.fromhex(randtext).decode()

    xored = xor("aaaaaaaaaaaaaaa", randtext)
    hex_xored = xored

    flag = ""
    print(endtext)
    print(hex_xored)

    endtext_i = 0
    hex_xored_i = 0
    for i in range(30):
        if i % 2 == 0:
            flag += endtext[endtext_i]
            endtext_i += 1
        else:
            flag += hex_xored[hex_xored_i]
            hex_xored_i += 1
    print(flag)

def main():
    decrypt()
if __name__ == "__main__":
    main()
