nomearq = input("digite o nome do arquivo: ")
entrada = open(nomearq, "rb")
saida = open("publi.ind", "w")

registros = []

tam = entrada.read(2)  # começa direto no primeiro registro

while tam and len(tam) == 2:
    publicadora = b''
    contador = 0

    tamint = int.from_bytes(tam, byteorder='little')
    ondecomeca = entrada.tell()

    c = entrada.read(1)
    while c:
        if c == b'|':
            contador += 1

            if contador == 4:
                c = entrada.read(1)
                while c != b'|':
                    publicadora += c
                    c = entrada.read(1)
                break

        c = entrada.read(1)

    publicadora = publicadora.decode()
    registros.append((publicadora, ondecomeca))

    entrada.seek(ondecomeca + tamint)
    tam = entrada.read(2)

registros.sort(key = lambda x:x[0])



