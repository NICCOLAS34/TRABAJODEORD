# esta função te como objetivo rmover um registro de gam.dat.

import os


arq = open("gam.dat", "r+b")

def removereg(indprim:list[tuple], id:str, arq):

    for i in range(len(indprim)):

        if id == indprim[i][0]:

            arq.seek(indprim[i][1])
            arq.read(2)  
            arq.write(b'*')
            
            indprim.remove(indprim[i])
            
        return

    print("Registro não encontrado.")


# esta praticamente feito. 
# mas esta função depende de outra que tera que ignorar o registro amrcado com "*"
# e pular pro proximo
# carregando apenas a lista sem as remoçoes para o  novo games dat

            


