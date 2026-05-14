# busca direta por indice.

from menosb import*

arq = open('gam.dat', 'rb')

def buscaDiretaID(id: str) -> str:

    for i in range(len(indprim)):

        if id == indprim[i][0]:      

            offset = indprim[i][1]       

            arq.seek(offset)

            tam = int.from_bytes(arq.read(2),byteorder= "little") 

            registro = arq.read(tam).decode()
            
            print(registro)   

    else:

        print("Registro não encontrado")
