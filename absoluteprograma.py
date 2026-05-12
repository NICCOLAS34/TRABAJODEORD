import os
from sys import argv


# ─────────────────────────────────────────────
#  ignorarep
# ─────────────────────────────────────────────

def ignorarep(lista: list[tuple[str, str]]) -> list[tuple[str, str]]:

    novoreg = []
    novoreg.append(lista[0])
    reganterior = lista[0]

    for i in range(1, len(lista)):
        if lista[i][1] == reganterior[1]:
            reganterior = lista[i]
        else:
            novoreg.append(lista[i])
            reganterior = lista[i]

    return novoreg


# ─────────────────────────────────────────────
#  gen
# ─────────────────────────────────────────────

def gen(arq) -> tuple[list, list]:

    registros = []
    tam = arq.read(2)

    while tam and len(tam) == 2:

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

    registros.sort(key=lambda x: x[1])
    genignorados = ignorarep(registros)

    return genignorados, registros


# ─────────────────────────────────────────────
#  publi
# ─────────────────────────────────────────────

def publi(arq) -> tuple[list, list]:

    registros = []
    tam = arq.read(2)

    while tam and len(tam) == 2:

        contador = 0
        id = b""
        publicadora = b""

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
                if contador == 4:
                    c = arq.read(1)
                    while c != b"|":
                        publicadora += c
                        c = arq.read(1)
                    break
            c = arq.read(1)

        id = id.decode()
        publicadora = publicadora.decode()
        registros.append((id, publicadora))
        arq.seek(ondecomeca + tamint)
        tam = arq.read(2)

    registros.sort(key=lambda x: x[1])
    publiignorados = ignorarep(registros)

    return publiignorados, registros


# ─────────────────────────────────────────────
#  geraid
# ─────────────────────────────────────────────

def geraid(arq) -> list[tuple[str, int]]:

    saida = open("primario.ind", "w")
    indprim = []

    tam_bytes = arq.read(2)

    while tam_bytes != b"":

        ponteiro = arq.tell() - 2
        tam = int.from_bytes(tam_bytes, "little")

        id = b""
        c = arq.read(1)
        while c != b"|":
            id += c
            c = arq.read(1)

        idstr = id.decode()
        indprim.append((idstr, ponteiro))
        saida.write(idstr + "|" + str(ponteiro) + "\n")

        arq.seek(ponteiro + tam + 2)
        tam_bytes = arq.read(2)

    saida.close()
    return indprim


# ─────────────────────────────────────────────
#  gerainvgen
# ─────────────────────────────────────────────

def gerainvgen(registros: list[tuple[str, str]]) -> list[tuple[str, int]]:

    invertida = []
    atual = registros[0][1]

    for i in range(len(registros) - 1):
        if atual == registros[i + 1][1]:
            invertida.append((registros[i][0], i + 1))
            atual = registros[i][1]
        else:
            invertida.append((registros[i][0], -1))
            atual = registros[i][1]

    invertida.append((registros[-1][0], -1))

    return invertida


# ─────────────────────────────────────────────
#  BP1
# ─────────────────────────────────────────────

def BP1(gen_busca: str, genignorados: list, invertida: list) -> list[str]:

    listaids = []

    for i in range(len(genignorados)):
        if gen_busca == genignorados[i][1]:
            ponteiro = genignorados[i][0]

            while ponteiro != -1:
                id = invertida[ponteiro][0]
                ponteiro = invertida[ponteiro][1]
                listaids.append(id)

    return listaids


# ─────────────────────────────────────────────
#  printaBP1
# ─────────────────────────────────────────────

def printaBP1(listaids: list[str], indprim: list, arq) -> None:

    for i in range(len(listaids)):
        for j in range(len(indprim)):
            if listaids[i] == indprim[j][0]:
                offset = indprim[j][1]
                arq.seek(offset)
                tam = int.from_bytes(arq.read(2), byteorder="little")
                registro = arq.read(tam).decode()
                print(registro)


# ─────────────────────────────────────────────
#  main
# ─────────────────────────────────────────────

def main() -> None:

    if len(argv) < 2:
        print("Uso:")
        print("  python programa.py -b")
        print("  python programa.py -e arquivo_operacoes")
        print("  python programa.py -c")
        return

    flag = argv[1]

    if flag == "-b":
        pass  # a implementar
    elif flag == "-e":
        if len(argv) < 3:
            print("Erro: informe o arquivo de operações.")
            return
        pass  # a implementar
    elif flag == "-c":
        pass  # a implementar
    else:
        print(f"Flag desconhecida: {flag}")


if __name__ == '__main__':
    main()