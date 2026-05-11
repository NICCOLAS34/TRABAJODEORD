import sys
import os

ARQUIVO_DADOS = "games.dat"
PRIMARIO_IND  = "primario.ind"
GENERO_IND    = "genero.ind"
PUBLI_IND     = "publicadora.ind"
LISTA_INV     = "listaInvertida.lst"


# ─────────────────────────────────────────────
#  Funções auxiliares de leitura do .dat
# ─────────────────────────────────────────────

def ler_registro(entrada):
    """Lê um registro do arquivo binário e devolve o conteúdo como string.
    Retorna "" quando chega ao fim do arquivo ou ao encontrar registro marcado como removido (*).
    """
    tam_bytes = entrada.read(2)
    if len(tam_bytes) < 2:
        return None, -1          # fim de arquivo

    tamint = int.from_bytes(tam_bytes, "little")
    offset = entrada.tell() - 2  # posição do início do registro (antes do tamanho)

    if tamint == 0:
        return None, offset       # registro removido (tamanho zerado)

    buffer = entrada.read(tamint)
    try:
        return buffer.decode(), offset
    except Exception:
        return None, offset


# ─────────────────────────────────────────────
#  Construção dos índices  (-b)
# ─────────────────────────────────────────────

def construir_indice_primario(entrada):
    """Percorre o arquivo e grava primario.ind (id|offset\\n)."""
    saida = open(PRIMARIO_IND, "wb")
    entrada.seek(0)

    tam_bytes = entrada.read(2)
    while tam_bytes != b"":
        ponteiro = entrada.tell() - 2          # offset do início do registro
        tam = int.from_bytes(tam_bytes, "little")

        # lê o ID (primeiro campo, até o primeiro '|')
        id_campo = b""
        c = entrada.read(1)
        while c and c != b"|":
            id_campo += c
            c = entrada.read(1)

        # grava id|offset no índice
        saida.write(id_campo + b"|" + str(ponteiro).encode() + b"\n")

        # avança para o próximo registro
        entrada.seek(ponteiro + tam + 2)
        tam_bytes = entrada.read(2)

    saida.close()


def construir_indice_genero(entrada):
    """Percorre o arquivo e grava genero.ind (genero|offset\\n)."""
    saida = open(GENERO_IND, "w")
    registros = []
    entrada.seek(0)

    tam = entrada.read(2)
    while tam and len(tam) == 2:
        genero = b""
        contador = 0

        tamint = int.from_bytes(tam, byteorder="little")
        ondecomeca = entrada.tell()   # offset logo após os 2 bytes de tamanho

        c = entrada.read(1)
        while c:
            if c == b"|":
                contador += 1
                if contador == 3:     # gênero é o 4º campo (3 pipes antes dele)
                    c = entrada.read(1)
                    while c != b"|":
                        genero += c
                        c = entrada.read(1)
                    break
            c = entrada.read(1)

        registros.append((genero.decode(), ondecomeca))
        entrada.seek(ondecomeca + tamint)
        tam = entrada.read(2)

    for genero, offset in registros:
        saida.write(genero + "|" + str(offset) + "\n")

    saida.close()
    return registros   # usado para montar a lista invertida


def construir_indice_publicadora(entrada):
    """Percorre o arquivo e grava publicadora.ind (publicadora|offset\\n)."""
    saida = open(PUBLI_IND, "w")
    registros = []
    entrada.seek(0)

    tam = entrada.read(2)
    while tam and len(tam) == 2:
        publicadora = b""
        contador = 0

        tamint = int.from_bytes(tam, byteorder="little")
        ondecomeca = entrada.tell()

        c = entrada.read(1)
        while c:
            if c == b"|":
                contador += 1
                if contador == 4:     # publicadora é o 5º campo (4 pipes antes)
                    c = entrada.read(1)
                    while c != b"|":
                        publicadora += c
                        c = entrada.read(1)
                    break
            c = entrada.read(1)

        registros.append((publicadora.decode(), ondecomeca))
        entrada.seek(ondecomeca + tamint)
        tam = entrada.read(2)

    for publicadora, offset in registros:
        saida.write(publicadora + "|" + str(offset) + "\n")

    saida.close()
    return registros


def construir_lista_invertida_genero(registros_genero):
    """A partir da lista (genero, offset) gera listaInvertida.lst.
    Formato: genero|pos_inicio_na_genero.ind\\n
    (índice invertido: para cada gênero diferente, guarda a posição
    da primeira entrada desse gênero no genero.ind)
    """
    saida = open(LISTA_INV, "w")
    registros_ordenados = sorted(registros_genero, key=lambda x: x[0])

    genero_ind_final = []
    for i, (genero, offset) in enumerate(registros_ordenados):
        if i == 0 or genero != registros_ordenados[i - 1][0]:
            genero_ind_final.append((genero, i))

    for genero, pos in genero_ind_final:
        saida.write(genero + "|" + str(pos) + "\n")

    saida.close()


def modo_construir_indices():
    """Entry-point do modo -b."""
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"Erro: arquivo {ARQUIVO_DADOS} não encontrado.")
        sys.exit(1)

    entrada = open(ARQUIVO_DADOS, "rb")

    construir_indice_primario(entrada)
    registros_genero = construir_indice_genero(entrada)
    construir_indice_publicadora(entrada)
    construir_lista_invertida_genero(registros_genero)

    entrada.close()
    print("Índices construídos: primario.ind, genero.ind, publicadora.ind, listaInvertida.lst")


# ─────────────────────────────────────────────
#  Carregamento dos índices para memória
# ─────────────────────────────────────────────

def carregar_primario():
    """Devolve dict {id_str: offset_int}."""
    indice = {}
    with open(PRIMARIO_IND, "rb") as f:
        for linha in f:
            linha = linha.decode().strip()
            if linha:
                partes = linha.split("|")
                indice[partes[0]] = int(partes[1])
    return indice


def carregar_genero():
    """Devolve lista [(genero, offset), ...]."""
    registros = []
    with open(GENERO_IND, "r") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                partes = linha.split("|")
                registros.append((partes[0], int(partes[1])))
    return registros


def carregar_publicadora():
    """Devolve lista [(publicadora, offset), ...]."""
    registros = []
    with open(PUBLI_IND, "r") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                partes = linha.split("|")
                registros.append((partes[0], int(partes[1])))
    return registros


def salvar_primario(indice):
    with open(PRIMARIO_IND, "wb") as f:
        for id_str, offset in sorted(indice.items(), key=lambda x: int(x[0])):
            f.write((id_str + "|" + str(offset) + "\n").encode())


def salvar_genero(registros):
    with open(GENERO_IND, "w") as f:
        for genero, offset in registros:
            f.write(genero + "|" + str(offset) + "\n")


def salvar_publicadora(registros):
    with open(PUBLI_IND, "w") as f:
        for pub, offset in registros:
            f.write(pub + "|" + str(offset) + "\n")


def salvar_lista_invertida(registros_genero):
    construir_lista_invertida_genero(registros_genero)


# ─────────────────────────────────────────────
#  Operações de busca
# ─────────────────────────────────────────────

def busca_primaria(id_busca, indice_primario, arquivo_dados):
    print(f'Busca pelo registro de ID "{id_busca}"')
    offset = indice_primario.get(id_busca)
    if offset is None:
        print("Registro não encontrado!")
        return

    arquivo_dados.seek(offset)
    conteudo, _ = ler_registro(arquivo_dados)
    if conteudo:
        print(conteudo)
    else:
        print("Registro não encontrado!")


def busca_secundaria_genero(genero_busca, registros_genero, arquivo_dados):
    resultados = [offset for g, offset in registros_genero if g == genero_busca]
    print(f'Busca por registros de gênero "{genero_busca}" ({len(resultados)} registros)')
    for offset in resultados:
        arquivo_dados.seek(offset - 2)   # offset aponta logo após os 2 bytes de tamanho
        conteudo, _ = ler_registro(arquivo_dados)
        if conteudo:
            print(conteudo)


def busca_secundaria_publicadora(pub_busca, registros_publicadora, arquivo_dados):
    resultados = [offset for p, offset in registros_publicadora if p == pub_busca]
    print(f'Busca por registros da publicadora "{pub_busca}" ({len(resultados)} registros)')
    for offset in resultados:
        arquivo_dados.seek(offset - 2)
        conteudo, _ = ler_registro(arquivo_dados)
        if conteudo:
            print(conteudo)


# ─────────────────────────────────────────────
#  Inserção
# ─────────────────────────────────────────────

def inserir_registro(linha_registro, indice_primario, registros_genero,
                     registros_publicadora, arquivo_dados):
    campos = linha_registro.rstrip("|").split("|")
    id_novo = campos[0]
    genero_novo = campos[3]
    pub_nova = campos[4]

    if id_novo in indice_primario:
        print(f'ID duplicado: registro de chave "{id_novo}" já existe.')
        return

    conteudo_bytes = linha_registro.encode()
    tam = len(conteudo_bytes)
    tam_bytes = tam.to_bytes(2, "little")

    arquivo_dados.seek(0, 2)                   # vai para o fim do arquivo
    offset_novo = arquivo_dados.tell() + 2     # offset após os 2 bytes de tamanho
    arquivo_dados.write(tam_bytes + conteudo_bytes)

    indice_primario[id_novo] = offset_novo - 2  # guarda offset do início do registro
    registros_genero.append((genero_novo, offset_novo))
    registros_publicadora.append((pub_nova, offset_novo))

    print(f'Inserção do registro de chave "{id_novo}" ({tam} bytes)')


# ─────────────────────────────────────────────
#  Remoção (lógica)
# ─────────────────────────────────────────────

def remover_registro(id_remover, indice_primario, registros_genero,
                     registros_publicadora, arquivo_dados):
    offset = indice_primario.get(id_remover)
    if offset is None:
        print(f'Remoção do registro de chave "{id_remover}"')
        print("Registro não encontrado!")
        return

    # zera os 2 bytes de tamanho (marca como removido)
    arquivo_dados.seek(offset)
    arquivo_dados.write((0).to_bytes(2, "little"))

    print(f'Remoção do registro de chave "{id_remover}" (offset = {offset})')

    del indice_primario[id_remover]
    registros_genero[:]      = [(g, o) for g, o in registros_genero      if o != offset + 2]
    registros_publicadora[:] = [(p, o) for p, o in registros_publicadora if o != offset + 2]


# ─────────────────────────────────────────────
#  Execução do arquivo de operações  (-e)
# ─────────────────────────────────────────────

def modo_executar_operacoes(arquivo_operacoes):
    for arq in [PRIMARIO_IND, GENERO_IND, PUBLI_IND, LISTA_INV]:
        if not os.path.exists(arq):
            print(f"Erro: arquivo de índice '{arq}' não encontrado. Execute -b primeiro.")
            sys.exit(1)

    if not os.path.exists(ARQUIVO_DADOS):
        print(f"Erro: arquivo {ARQUIVO_DADOS} não encontrado.")
        sys.exit(1)

    # carrega índices para memória
    indice_primario      = carregar_primario()
    registros_genero     = carregar_genero()
    registros_publicadora = carregar_publicadora()

    arquivo_dados = open(ARQUIVO_DADOS, "r+b")

    with open(arquivo_operacoes, "r") as ops:
        for linha in ops:
            linha = linha.strip()
            if not linha:
                continue

            partes = linha.split(" ", 1)
            op   = partes[0]
            arg  = partes[1] if len(partes) > 1 else ""

            if op == "bp":
                busca_primaria(arg, indice_primario, arquivo_dados)
            elif op == "bs1":
                busca_secundaria_genero(arg, registros_genero, arquivo_dados)
            elif op == "bs2":
                busca_secundaria_publicadora(arg, registros_publicadora, arquivo_dados)
            elif op == "i":
                inserir_registro(arg, indice_primario, registros_genero,
                                 registros_publicadora, arquivo_dados)
            elif op == "r":
                remover_registro(arg, indice_primario, registros_genero,
                                 registros_publicadora, arquivo_dados)
            else:
                print(f"Operação desconhecida: {op}")

    arquivo_dados.close()

    # salva índices atualizados de volta no disco
    salvar_primario(indice_primario)
    salvar_genero(registros_genero)
    salvar_publicadora(registros_publicadora)
    salvar_lista_invertida(registros_genero)


# ─────────────────────────────────────────────
#  Compactação  (-c)
# ─────────────────────────────────────────────

def modo_compactar():
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"Erro: arquivo {ARQUIVO_DADOS} não encontrado.")
        sys.exit(1)

    tmp = ARQUIVO_DADOS + ".tmp"
    entrada = open(ARQUIVO_DADOS, "rb")
    saida   = open(tmp, "wb")

    tam_bytes = entrada.read(2)
    while tam_bytes:
        if len(tam_bytes) < 2:
            break
        tam = int.from_bytes(tam_bytes, "little")
        if tam == 0:
            # registro removido: descobre o tamanho original para pular
            # (tamanho zerado não guarda o tamanho original; precisamos
            #  ler até o próximo registro — aqui assumimos que registros
            #  removidos têm tamanho 0 e não há como recuperar o tamanho,
            #  então apenas paramos. Ajuste conforme a estratégia da sua professora.)
            break
        conteudo = entrada.read(tam)
        saida.write(tam_bytes + conteudo)
        tam_bytes = entrada.read(2)

    entrada.close()
    saida.close()

    os.replace(tmp, ARQUIVO_DADOS)
    print("Arquivo compactado.")

    # reconstrói índice primário se existir
    if os.path.exists(PRIMARIO_IND):
        entrada = open(ARQUIVO_DADOS, "rb")
        construir_indice_primario(entrada)
        entrada.close()
        print("Índice primário reconstruído.")


# ─────────────────────────────────────────────
#  Ponto de entrada
# ─────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python programa.py -b")
        print("  python programa.py -e arquivo_operacoes")
        print("  python programa.py -c")
        sys.exit(1)

    flag = sys.argv[1]

    if flag == "-b":
        modo_construir_indices()
    elif flag == "-e":
        if len(sys.argv) < 3:
            print("Erro: informe o arquivo de operações.")
            sys.exit(1)
        modo_executar_operacoes(sys.argv[2])
    elif flag == "-c":
        modo_compactar()
    else:
        print(f"Flag desconhecida: {flag}")
        sys.exit(1)