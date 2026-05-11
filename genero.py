entrada = open('gam.dat', "rb")
saida = open("genero.ind", "w")

registros = []

tam = entrada.read(2) 

while tam and len(tam) == 2:
    genero = b''
    contador = 0

    tamint = int.from_bytes(tam, byteorder='little')
    ondecomeca = entrada.tell()

    c = entrada.read(1)
    while c:
        if c == b'|':
            contador += 1

            if contador == 3:
                c = entrada.read(1)
                while c != b'|':
                    genero += c
                    c = entrada.read(1)
                break

        c = entrada.read(1)

    genero = genero.decode()
    registros.append((genero, ondecomeca))
    

    entrada.seek(ondecomeca + tamint)
    tam = entrada.read(2)

registros.sort(key= lambda x: x[0])
saida.write(str(registros))
    
entrada.close()
saida.close()