# essa função tem como obj inserir um registro em games dat
arq1 = open("primario.ind","r")
arq = open("gam.dat","a")
import os 

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


