entrada = open('gam.dat', "rb")
saida = open("primario.ind", "w")

tam_bytes = entrada.read(2)

indprim = []

while tam_bytes != b"":

    ponteiro = entrada.tell() - 2

    tam = int.from_bytes(tam_bytes, "little")

    id = b""
    c = entrada.read(1)

    while c != b"|":
        id += c
        c = entrada.read(1)

    idstr = id.decode()

    indprim.append((idstr, ponteiro))

    entrada.seek(ponteiro + tam + 2)

    tam_bytes = entrada.read(2)
    
entrada.close()
saida.close()



    


    