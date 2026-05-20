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
        if c == b'*':

            arq.seek(ondecomeca + tamint)
            tam = arq.read(2)
            continue
        
        while c != b"|":

            id += c
            c = arq.read(1)

        c = arq.read(1)
        while c:
            if c == b"|":

                contador += 1
                if contador == 2:

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

        if c == b'*':
            arq.seek(ondecomeca + tamint)
            tam = arq.read(2)
            continue
        
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

    publiignorados = [(registrospubli[0][1], 0)]
    for i in range(1, len(registrospubli)):
        if registrospubli[i][1] != registrospubli[i-1][1]:
            publiignorados.append((registrospubli[i][1], i))

    return registrospubli, publiignorados


# ────────────────────────────────────────── #
#                 geraid                     #
# ────────────────────────────────────────── #

def geraid(arq) -> list[tuple[str, int]]:

    indprim = []

    tam_bytes = arq.read(2)

    while tam_bytes != b"":

        ponteiro = arq.tell() - 2
        tam = int.from_bytes(tam_bytes, "little")

        id = b""
        c = arq.read(1)
        
        if c == b'*':
            arq.seek(ponteiro + tam + 2)
            tam_bytes = arq.read(2)
            continue
        
        while c != b"|":
            id += c
            c = arq.read(1)

        idstr = id.decode()
        indprim.append((idstr, ponteiro))

        arq.seek(ponteiro + tam + 2)
        tam_bytes = arq.read(2)

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
            atual = registros[i + 1][1]
        else:
            invertida.append((registros[i][0], -1))
            atual = registros[i + 1][1]

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
            atual = registrospubli[i + 1][1]
        else:

            invertida.append((registrospubli[i][0], -1))
            atual = registrospubli[i + 1][1]

    invertida.append((registrospubli[-1][0], -1))

    return invertida


# ─────────────────────────────────────────────
#  buscaPrimaria (busca por ID)
# ─────────────────────────────────────────────

def buscaPrimaria(id: str, indprim: list, arq) -> None:

    encontrou = False
    
    for i in range(len(indprim)):

        if id == indprim[i][0]:
            encontrou = True
            
            offset = indprim[i][1]
            arq.seek(offset)
            tam = int.from_bytes(arq.read(2), byteorder="little")
            registro = arq.read(tam).decode()
            
            print(registro)
            break
    
    if encontrou == False:
        print("Registro não encontrado!")


# ─────────────────────────────────────────────
#  buscaGenero (BS1)
# ─────────────────────────────────────────────

def buscaGenero(genero_busca: str, genignorados: list, invertidagen: list, indprim: list, arq) -> None:

    listaids = []
    
    for i in range(len(genignorados)):
        if genero_busca == genignorados[i][0]:
            ponteiro = genignorados[i][1]
            
            while ponteiro != -1:
                id = invertidagen[ponteiro][0]
                ponteiro = invertidagen[ponteiro][1]
                listaids.append(id)
            
            break
    
    if len(listaids) == 0:
        print("Nenhum registro encontrado!")
        return
    
    for i in range(len(listaids)):
        for j in range(len(indprim)):
            if listaids[i] == indprim[j][0]:
                offset = indprim[j][1]
                arq.seek(offset)
                tam = int.from_bytes(arq.read(2), byteorder="little")
                registro = arq.read(tam).decode()
                print(registro)


# ─────────────────────────────────────────────
#  buscaPublicadora (BS2)
# ─────────────────────────────────────────────

def buscaPublicadora(pub_busca: str, publiignorados: list, invertidapubli: list, indprim: list, arq) -> None:

    listaidspubli = []
    
    for i in range(len(publiignorados)):
        if pub_busca == publiignorados[i][0]:
            ponteiro = publiignorados[i][1]
            
            while ponteiro != -1:
                id = invertidapubli[ponteiro][0]
                ponteiro = invertidapubli[ponteiro][1]
                listaidspubli.append(id)
            
            break
    
    if len(listaidspubli) == 0:
        print("Nenhum registro encontrado!")
        return
    
    for i in range(len(listaidspubli)):
        for j in range(len(indprim)):
            if listaidspubli[i] == indprim[j][0]:
                offset = indprim[j][1]
                arq.seek(offset)
                tam = int.from_bytes(arq.read(2), byteorder="little")
                registro = arq.read(tam).decode()
                print(registro)


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
#               printaBP2                     #
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

# ───────────────────────────────────────────── #
#                buscaDiretaID                #
# ───────────────────────────────────────────── #

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

def inserereg(registro, indprim, arq):
    
    tam = len(registro)
    tamby = tam.to_bytes(2, byteorder="little")
    
    idstr = b""
    i = 0
    while i < len(registro):
        if registro[i:i+1] == b"|":
            break
        idstr += registro[i:i+1]
        i = i + 1
    
    idstr = idstr.decode()
    
    ja_existe = False
    j = 0
    while j < len(indprim):
        if idstr == indprim[j][0]:
            ja_existe = True
        j = j + 1
    
    if ja_existe:
        print("ID duplicado!")
        return
    
    arq.seek(0, os.SEEK_END)
    pos_final = arq.tell()
    
    arq.write(tamby)
    arq.write(registro)
    
    indprim.append((idstr, pos_final))

# --------------------------------------------- #
#                removereg                      #
# --------------------------------------------- #

def removereg(indprim:list[tuple], id:str, arq):

    encontrou = False
    
    for i in range(len(indprim)):

        if id == indprim[i][0]:
            encontrou = True
            ponteiro = indprim[i][1]
            
            arq.seek(ponteiro)
            tam_bytes = arq.read(2)
            tam = int.from_bytes(tam_bytes, byteorder="little")
            
            arq.seek(ponteiro)
            arq.write(b'*')
            
            indprim.pop(i)
            break
    
    if not encontrou:
        print("Registro não encontrado!")
    
    return


# ───────────────────────────────────────────── #
#                    lereg                      #
# ───────────────────────────────────────────── #



def leiareg(entrada, saida):  
    tam = entrada.read(2)
    
    if len(tam) < 2:
        return ""
    
    tamint = int.from_bytes(tam, "little")
    primbyte = entrada.read(1)
    
    if primbyte != b'*':
        saida.write(tam)
        saida.write(primbyte)
        resto = entrada.read(tamint - 1)
        saida.write(resto)
        
        buffer = (primbyte + resto).decode()
        return buffer
    else:

        entrada.seek(entrada.tell() + tamint - 1)
        return ""
 

 

# ───────────────────────────────────────────── #
#            salvarIndices                       #
# ───────────────────────────────────────────── #

def salvarIndices(indprim, genignorados, invertidagen, publiignorados, invertidapubli):
    
    primarq = open("primario.ind","w")
    genarq = open("genero.ind", "w")
    pubarq = open("publicadora.ind","w")
    arqinv = open("listaInvertida.lst","w")
        
    primarq.write(str(indprim))
    genarq.write(str(genignorados))
    pubarq.write(str(publiignorados))

    arqinv.write(str(invertidagen))
    arqinv.write("\n")
    arqinv.write(str(invertidapubli))
    
    primarq.close()
    genarq.close()
    pubarq.close()
    arqinv.close()


# ───────────────────────────────────────────── #
#            carregarIndices                     #
# ───────────────────────────────────────────── #

def carregarIndices():
    
    indprim = []
    genignorados = []
    publiignorados = []
    invertidagen = []
    invertidapubli = []
    
    try:
        primarq = open("primario.ind", "r")
        conteudo = primarq.read()
        primarq.close()
        indprim = eval(conteudo)
    except FileNotFoundError:
        print("Arquivo primario.ind não encontrado!")
        return None
    except:
        print("Erro ao carregar primario.ind!")
        return None
    
    try:
        genarq = open("genero.ind", "r")
        conteudo = genarq.read()
        genarq.close()
        genignorados = eval(conteudo)
    except FileNotFoundError:
        print("Arquivo genero.ind não encontrado!")
        return None
    except:
        print("Erro ao carregar genero.ind!")
        return None
    
    try:
        pubarq = open("publicadora.ind", "r")
        conteudo = pubarq.read()
        pubarq.close()
        publiignorados = eval(conteudo)
    except FileNotFoundError:
        print("Arquivo publicadora.ind não encontrado!")
        return None
    except:
        print("Erro ao carregar publicadora.ind!")
        return None
    
    try:
        arqinv = open("listaInvertida.lst", "r")
        conteudo = arqinv.read()
        arqinv.close()
        
        linhas = conteudo.split("\n")
        invertidagen = eval(linhas[0])
        invertidapubli = eval(linhas[1])
        
    except FileNotFoundError:
        print("Arquivo listaInvertida.lst não encontrado!")
        return None
    except:
        print("Erro ao carregar listaInvertida.lst!")
        return None
    
    return indprim, genignorados, invertidagen, publiignorados, invertidapubli


# ───────────────────────────────────────────── #
#                    main                       #
# ───────────────────────────────────────────── #

def main() -> None:

    if len(argv) < 2:
        print("Uso:")
        print("  python programa.py -b")
        print("  python programa.py -e arquivo_operacoes")
        print("  python programa.py -c")
        return

    flag = argv[1]

    if flag == "-b":

        try:
            arq = open("gam.dat", "rb")
        except FileNotFoundError:
            print("Arquivo gam.dat não encontrado!")
            return
        
        indprim = geraid(arq)
        arq.seek(0)
        genignorados, registrosgen = gen(arq)
        arq.seek(0)
        registrospubli, publiignorados = publi(arq)
        invertidagen = gerainvgen(registrosgen)
        invertidapubli = gerainvpubli(registrospubli)
        arq.close()
        
        salvarIndices(indprim, genignorados, invertidagen, publiignorados, invertidapubli)
        print("Índices criados com sucesso!")

    elif flag == "-e":

        indices = carregarIndices()
        
        if indices == None:
            print("Erro ao carregar índices!")
            return
        
        indprim, genignorados, invertidagen, publiignorados, invertidapubli = indices
        
        try:
            arq = open("gam.dat", "r+b")
        except FileNotFoundError:
            print("Arquivo gam.dat não encontrado!")
            return
        
        try:
            with open(argv[2], "r") as arqdeop: 
                for linha in arqdeop:             
                    linha = linha.strip()
                    
                    if not linha:
                        continue
                    
                    partes = linha.split(" ", 1)
                    flag = partes[0]
                    
                    if len(partes) < 2:
                        continue
                    
                    argumento = partes[1]
                    
                    if flag == "bp":
                        print(f"Busca pelo registro de ID \"{argumento}\"")
                        buscaPrimaria(argumento, indprim, arq)
                    
                    elif flag == "bs1":
                        print(f"Busca por registros de gênero \"{argumento}\"")
                        buscaGenero(argumento, genignorados, invertidagen, indprim, arq)
                    
                    elif flag == "bs2":
                        print(f"Busca por registros da publicadora \"{argumento}\"")
                        buscaPublicadora(argumento, publiignorados, invertidapubli, indprim, arq)
                    
                    elif flag == "i":
                        registro_bytes = argumento.encode()
                        
                        idstr = b""
                        k = 0
                        while k < len(registro_bytes):
                            if registro_bytes[k:k+1] == b"|":
                                break
                            idstr += registro_bytes[k:k+1]
                            k = k + 1
                        
                        idstr = idstr.decode()
                        print(f"Inserção do registro de chave \"{idstr}\" ({len(argumento)} bytes)")
                        inserereg(registro_bytes, indprim, arq)
                    
                    elif flag == "r":
                        encontrou = False
                        for i in range(len(indprim)):
                            if argumento == indprim[i][0]:
                                print(f"Remoção do registro de chave \"{argumento}\" (offset = {indprim[i][1]})")
                                encontrou = True
                                break
                        if encontrou == False:
                            print(f"Remoção do registro de chave \"{argumento}\"")
                        removereg(indprim, argumento, arq)
        
        except FileNotFoundError:
            print(f"Arquivo {argv[2]} não encontrado!")
            arq.close()
            return
        
        arq.close()
        salvarIndices(indprim, genignorados, invertidagen, publiignorados, invertidapubli)

    elif flag == "-c":

        try:
            entrada = open('gam.dat', "rb")
        except FileNotFoundError:
            print("Arquivo gam.dat não encontrado!")
            return
        
        saida = open('gam_novo.dat', "wb")

        buffer = leiareg(entrada, saida)

        while buffer != "":
            buffer = leiareg(entrada, saida)

        entrada.close()
        saida.close()

        os.replace('gam_novo.dat', 'gam.dat')
        
        arq = open('gam.dat', "rb")
        indprim = geraid(arq)
        arq.close()
        
        arq_ind = open("primario.ind", "w")
        for i in range(len(indprim)):
            arq_ind.write(indprim[i][0] + "|" + str(indprim[i][1]) + "\n")
        arq_ind.close()
        
        print("Arquivo compactado com sucesso!")

    else:

        print(f"Flag desconhecida: {flag}")


if __name__ == '__main__':
    main()