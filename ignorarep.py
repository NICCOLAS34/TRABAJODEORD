def ignorarep(lista: list[tuple[int, str]]) -> list[tuple[int, str]]:

    novoreg = []

    novoreg.append(lista[0])

    reganterior = lista[0]

    for i in range(1, len(lista)):

        if lista[i][1] == reganterior[1]:
            reganterior = lista[i]

        else:
            novoreg.append(lista[i])
            reganterior = lista[i]

    return novoreg

