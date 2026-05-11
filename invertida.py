newgen = open('newgen.ind', "w")

arquivo = open("genero.ind", "r")
registros = []

for linha in arquivo:
    partes = linha.split("|")
    genero = partes[0]
    offset = int(partes[1])
    registros.append((genero, offset))  

i = 0
genero_ind_final = []

while i < len(registros):
    if i == 0 or registros[i][0] != registros[i-1][0]:
        genero_ind_final.append((registros[i][0], i))
    i += 1

for genero, pos in genero_ind_final:
    newgen.write(genero + "|" + str(pos) + "\n")

newgen.close()