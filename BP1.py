#implementar busca por gênero
arq = open('gam.dat', 'rb')

def BP1(gen: str) -> str:


    listaidgen = []

    for i in range(len(genignorados)):

        if gen == genignorados[i][0]:       

            ponteiro = genignorados[i][1]       

            while ponteiro != -1:

                id = invertida[ponteiro][0]
                ponteiro = invertida[ponteiro][1]
                listaidgen.append(id)

    return listaidgen
                        


def printaBP1(listaidgen: list[str]) -> str:

    for i in range(len(listaidgen)):

        for j in range(len(indprim)):

            if listaidgen[i] == indprim[j][0]:      

                offset = indprim[j][1]       

                arq.seek(offset)

                tam = int.from_bytes(arq.read(2),byteorder= "little") 

                registro = arq.read(tam).decode()
                
                print(registro)      