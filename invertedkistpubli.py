
def gerainvpubli(registrospubli: list[tuple[str, str]]) -> list[tuple[str, int]]:

   invertida = []

   atual = registrospubli[0][1]

   for i in range(len(registrospubli)-1):

      if atual == registrospubli[i + 1][1]:

         invertida.append((registrospubli[i][0], i + 1))
         atual = registrospubli[i][1]

      else:
         invertida.append((registrospubli[i][0], -1))
         atual = registrospubli[i][1]

   invertida.append((registrospubli[-1][0], -1))

   return invertida