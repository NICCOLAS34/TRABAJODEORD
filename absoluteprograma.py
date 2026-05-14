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
            novoreg.append((lista[i][1], i))  
            reganterior = lista[i]

    return novoreg


# ─────────────────────────────────────────────
#  gen
# ─────────────────────────────────────────────

def gen(arq) -> list[tuple[str, str]]:

    registrosgen = []

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
        registrosgen.append((id, genero))
        arq.seek(ondecomeca + tamint)

        tam = arq.read(2)

    registrosgen.sort(key=lambda x: x[1])

    genignorados = [(registrosgen[0][1], 0)]

    for i in range(1, len(registrosgen)):

        if registrosgen[i][1] != registrosgen[i-1][1]:

            genignorados.append((registrosgen[i][1], i))

    return genignorados, registrosgen


# ─────────────────────────────────────────────
#  publi
# ─────────────────────────────────────────────

def publi(arq) -> tuple[list, list]:

    registrospubli = []

    tam = arq.read(2)

    while tam and len(tam) == 2:

        contador = 0
        id = b""
        pub = b""

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
                        pub += c
                        c = arq.read(1)
                    break
            c = arq.read(1)

        id = id.decode()
        pub = pub.decode()
        registrospubli.append((id, pub))
        arq.seek(ondecomeca + tamint)
        tam = arq.read(2)

    registrospubli.sort(key=lambda x: x[1])

    # publiignorados: (publicadora, posicao_na_lista_completa)
    publiignorados = [(registrospubli[0][1], 0)]
    for i in range(1, len(registrospubli)):
        if registrospubli[i][1] != registrospubli[i-1][1]:
            publiignorados.append((registrospubli[i][1], i))

    return registrospubli, publiignorados


# ────────────────────────────────────────── #
#                 geraid                     #
# ────────────────────────────────────────── #

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
        saida.write(str(indprim))

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
#  gerainvpubli
# ─────────────────────────────────────────────

def gerainvpubli(registrospubli: list[tuple[str, str]]) -> list[tuple[str, int]]:

    invertida = []
    atual = registrospubli[0][1]

    for i in range(len(registrospubli) - 1):
        if atual == registrospubli[i + 1][1]:
            invertida.append((registrospubli[i][0], i + 1))
            atual = registrospubli[i][1]
        else:
            invertida.append((registrospubli[i][0], -1))
            atual = registrospubli[i][1]

    invertida.append((registrospubli[-1][0], -1))

    return invertida


# ─────────────────────────────────────────────
#  BP1
# ─────────────────────────────────────────────

def BP1(gen_busca: str, genignorados: list, invertidagen: list) -> list[str]:

    listaids = []

    for i in range(len(genignorados)):
        if gen_busca == genignorados[i][0]:
            ponteiro = genignorados[i][1]

            while ponteiro != -1:
                id = invertidagen[ponteiro][0]
                ponteiro = invertidagen[ponteiro][1]
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
#  BP2
# ─────────────────────────────────────────────

def BP2(pub_busca: str, publiignorados: list, invertidapubli: list) -> list[str]:

    listaidspubli = []

    for i in range(len(publiignorados)):
        if pub_busca == publiignorados[i][0]:
            ponteiro = publiignorados[i][1]

            while ponteiro != -1:
                id = invertidapubli[ponteiro][0]
                ponteiro = invertidapubli[ponteiro][1]
                listaidspubli.append(id)

    return listaidspubli


# ───────────────────────────────────────────── #
#                 printaBP2                     #
# ───────────────────────────────────────────── #

def printaBP2(listaidspubli: list[str], indprim: list, arq) -> None:

    for i in range(len(listaidspubli)):
        for j in range(len(indprim)):
            if listaidspubli[i] == indprim[j][0]:
                offset = indprim[j][1]
                arq.seek(offset)
                tam = int.from_bytes(arq.read(2), byteorder="little")
                registro = arq.read(tam).decode()
                print(registro)


# ─────────────────────────────────────────────
#  buscaDiretaID
# ─────────────────────────────────────────────

def buscaDiretaID(id: str, indprim: list, arq) -> None:

    for i in range(len(indprim)):
        if id == indprim[i][0]:
            offset = indprim[i][1]
            arq.seek(offset)
            tam = int.from_bytes(arq.read(2), byteorder="little")
            registro = arq.read(tam).decode()
            print(registro)
            break
    else:
        print("Registro não encontrado!")

# --------------------------------------------- #
#                insererg                      #
# --------------------------------------------- #

def inserereg(id, nome, ano, genero, publicadora, plataforma, indprim, arq):
    
    buffer = f"{id}|{nome}|{ano}|{genero}|{publicadora}|{plataforma}|"
    
    for i in range(len(indprim)):

        if id == indprim[i][0]:
              
            print("ID duplicado!")
            return
    
    arq.seek(0, os.SEEK_END)
    antigofinal = arq.tell()
    
    tam = len(buffer)
    tamby = tam.to_bytes(2, byteorder="little")
    
    arq.write(tamby + buffer.encode())
    indprim.append((id, antigofinal))

# --------------------------------------------- #
#                removereg                      #
# --------------------------------------------- #

def removereg(indprim:list[tuple], id:str, arq):

    for i in range(len(indprim)):

        if id == indprim[i][0]:

            arq.seek(indprim[i][1])
            arq.read(2)  
            arq.write(b'*')
            
            indprim.remove(indprim[i])
            
        return

    print("Registro não encontrado.")
 

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

        arq = open("gam.dat", "rb")
        indprim = geraid(arq)
        arq.seek(0)
        genignorados, registrosgen = gen(arq)
        arq.seek(0)
        registrospubli, publiignorados = publi(arq)
        invertidagen = gerainvgen(registrosgen)
        invertidapubli = gerainvpubli(registrospubli)
        arq.close()

    elif flag == "-e":

        with open(argv[2], "r") as ops_file: 
            for linha in ops_file:             
                linha = linha.strip()
                partes = linha.split(" ", 1)
                comando = partes[0]
                argumento = partes[1]
                
                if comando == "i":
                    campos = argumento.split("|")
                    inserereg(campos[0], campos[1], int(campos[2]), 
                            campos[3], campos[4], campos[5], indprim, arq)
                    
                elif comando == "r":
                    removereg(indprim, argumento, arq)

    elif flag == "-c":

        pass  

    else:

        print(f"Flag desconhecida: {flag}")


if __name__ == '__main__':
    main()