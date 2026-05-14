
def gerainvgen(registrosgen: list[tuple[str, str]]) -> list[tuple[str, int]]:

   invertida = []

   atual = registrosgen[0][1]

   for i in range(len(registrosgen)-1):   

      if atual == registrosgen[i + 1][1]:

         invertida.append((registrosgen[i][0], i + 1))
         atual = registrosgen[i][1]

      else:
         invertida.append((registrosgen[i][0], -1))
         atual = registrosgen[i][1]

   invertida.append((registrosgen[-1][0], -1))

   return invertida


  


         





