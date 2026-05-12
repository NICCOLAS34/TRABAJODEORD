arq = open('gam.dat', "rb")
from ignorarep import *



def gen(arq) -> list[tuple[int, str]]:

    registros = []

    tam = arq.read(2)

    while tam:

        contador = 0
        id = b""
        genero = b""

        tamint = int.from_bytes(tam, byteorder='little')
        ondecomeca = arq.tell()

        c = arq.read(1)
        while c != b"|":
            id += c
            c = arq.read(1)

        c = arq.read(1)
        while c:
            if c == b"|":
                contador += 1
                if contador == 3:
                    c = arq.read(1)
                    while c != b"|":
                        genero += c
                        c = arq.read(1)
                    break
            c = arq.read(1)

        
        id = id.decode()
        genero = genero.decode()
        registros.append((id, genero))
        arq.seek(ondecomeca + tamint)
        tam = arq.read(2)

        

        genignorados = ignorarep(registros)


