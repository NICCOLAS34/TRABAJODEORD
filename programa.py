import os
from sys import argv
arq = open('gam.dat', "wb")





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


arq = open('gam.dat', "rb")


def gen(arq) -> list[tuple[int, str]]:

    registros = []

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
        registros.append((id, publi))
        arq.seek(ondecomeca + tamint)
        tam = arq.read(2)




def geraid(arq: str) -> list[tuple[int, bytes]]:

    entrada = open('gam.dat', "rb")
    saida = open("primario.ind", "wb")

    tam_bytes = entrada.read(2)


    while tam_bytes != b"":

        ponteiro = entrada.tell() - 2

        tam = int.from_bytes(tam_bytes, "little")

        id = b""
        c = entrada.read(1)

        while c != b"|":
            id += c
            c = entrada.read(1)

        ponteirotexto = str(ponteiro).encode()

        saida.write(id)
        saida.write(b"|")
        saida.write(ponteirotexto)
        saida.write(b"\n")

        entrada.seek(ponteiro + tam + 2)

        tam_bytes = entrada.read(2)

    entrada.close()
    saida.close()






def main() -> None:

    if len(argv) < 3:
        raise ValueError ('Número incorreto de argumentosa\n Modo de uso:')
    
    '''supostafunção (arg[1], arg[2])'''

if __name__ == '__main__':
    main()



