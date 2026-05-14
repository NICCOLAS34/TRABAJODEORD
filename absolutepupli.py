arq = open('gam.dat', "rb")
from ignorarep import *


def publi(arq) -> tuple[list, list]:

    registrospubli = []

    tam = arq.read(2)

    while tam:

        contador = 0
        id = b""
        publi = b""

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
                        publi += c
                        c = arq.read(1)
                    break
            c = arq.read(1)

        id = id.decode()
        publi = publi.decode()
        registrospubli.append((id, publi))
        arq.seek(ondecomeca + tamint)
        tam = arq.read(2)

    registrospubli.sort(key=lambda x: x[1])

    publiignorados = ignorarep(registrospubli)

    return registrospubli, publiignorados