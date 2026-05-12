''' 

   O arquivo de operações possuirá uma operação por linha, codificada com o identificador da 
operação seguido pelo seu argumento. Os identificadores de operações possíveis são: bp = 
busca no índice primário, bs1 = busca no índice
secundário por gênero, bs2 = busca no índice secundário por publicadora, i 
= inserção ou r = remoção. A seguir é
exemplificado o formato de um arquivo de operações.

'''

def gerainvgen(registros: list[tuple[str, str]]) -> list[tuple[str, int]]:

   invertida = []

   atual = registros[0][1]

   for i in range(len(registros)-1):

      if atual == registros[i + 1][1]:

         invertida.append((registros[i][0], i + 1))
         atual = registros[i][1]

      else:
         invertida.append((registros[i][0], -1))
         atual = registros[i][1]

   invertida.append((registros[-1][0], -1))

   return invertida


  


         





