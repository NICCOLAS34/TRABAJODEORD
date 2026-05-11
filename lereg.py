entrada = open('gam.dat', "rb")


def leiareg(entrada):
    tam = entrada.read(2)

    if  len(tam) < 2:
        return ""

    tamint = int.from_bytes(tam, "little")

    if tamint > 0:
        buffer = entrada.read(tamint)
        buffer = buffer.decode()
        return buffer
    else:
        return ""


buffer = leiareg(entrada)

while buffer != "":
    lista = buffer.split(sep='|')

    for campo in lista:
        print(campo)

    buffer = leiareg(entrada)

entrada.close()