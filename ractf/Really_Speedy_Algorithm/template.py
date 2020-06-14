import socket
import math

IP = '88.198.219.20'
PORT = 35831 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
s.setblocking(0)

buffer = b''

values = {}

def getModInverse(a, m):
    if math.gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

while True:
    # Read until a prompt or line break
    try:
        chunk = s.recv(4096)
        buffer += chunk
        print(chunk.decode(), end='')
    except BlockingIOError:
        pass

    if b'\n' not in buffer and not buffer.endswith(b': '):
        continue

    # Grab the oldest line
    buffer = buffer.split(b'\n', 1)
    if len(buffer) == 1:
        line, buffer = buffer[0], b''
    else:
        line, buffer = buffer

    # Llines start with [<code>]
    if line[:1] != b'[':
        continue

    # Use slicing not indexing because indexing bytes returns ints
    mode = line[1:2]
    #print(mode)
    if mode == b'*':
        pass 
    elif mode == b'c':
        pass 
    elif mode == b':':
        data = line.split(b"] ")[1].decode().split(": ")
        values[data[0]] = int(data[1])
        print(values)
        
    elif mode == b'!':
        print("YOU FAILED!!! :(") 
    elif mode == b'?':
        question = line.split(b"] ")[1][:-2]
        if question == b"n":
            n = values['p'] * values['q']
            print("     N: " + str(n))
            s.send(str(n).encode('latin-1') + b"\n")
        elif question == b"d":
            phi = (values['p'] - 1) * (values['q'] - 1)
            d = getModInverse(values['e'], phi)
            print("     D: " + str(d))
            s.send(str(d).encode('latin-1') + b"\n")
        elif question == b"pt":
            phi = values['phi']
            p = values['p']
            q = (phi // (p - 1)) + 1
            n = p * q
            d = getModInverse(values['e'], phi)
            pt = pow(values['ct'], d, n)
            print("     Pt: " + str(pt))
            s.send(str(pt).encode('latin-1') + b"\n")
        elif question == b"ct":
            n = values['p'] * values['q']
            ct = pow(values['pt'], values['e'], n)
            print("     Ct: " + str(ct))
            s.send(str(ct).encode('latin-1') + b"\n")
        elif question == b"q":
            q = values['n'] // values['p']
            print("     Q: " + str(q))
            s.send(str(q).encode('latin-1') + b"\n")

        else:
            print("         OTHER: " + str(question))

    else:
        pass
