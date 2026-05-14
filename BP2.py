#implementar busca por publicadora

from invertedkist import*
from absolutepupli import*
from invertedkist import*
arq = open('gam.dat', 'rb')

def BP2(publi: str) -> str:

    listaidspubli = []

    for i in range(len(publiignorados)):

        if publi == publiignorados[i][1]:       

            ponteiro = publiignorados[i][0 ]       

            while ponteiro != -1:

                id = invertida[ponteiro][0]
                ponteiro = invertida[ponteiro][1]
                listaidspubli.append(id)

    return listaidspubli
                        


def printaBP2(listaidspubli: list[str]) -> str:

    for i in range(len(listaidspubli)):

        for j in range(len(indprim)):

            if listaidspubli[i] == indprim[j][0]:      

                offset = indprim[j][1]    
                arq.seek(offset)

                tam = int.from_bytes(arq.read(2),byteorder= "little") 

                registro = arq.read(tam).decode()
                
                print(registro)