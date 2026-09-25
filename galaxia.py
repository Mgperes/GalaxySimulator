import pygame

#Grade inicial
grade = [
    [1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1]
]

def mostrar_grade(grade):
    for linha in grade:
        for celula in linha:
            if celula == 0:
                print(".", end=" ")
            elif celula == 1:
                print("•", end=" ")
            elif celula == 2:
                print("★", end=" ")
        print()

def contar_materia(grade, linha, coluna):
    cont = 0

    for i in range(linha - 1, linha + 2):
        for j in range(coluna - 1, coluna + 2):
            #Não conta a própria celula
            if i == linha and j == coluna:
                continue 

            if 0 <= i < len(grade) and 0 <= j < len(grade[0]):
                if grade[i][j] == 1:
                    cont += 1

    return cont

def proximo_estado(grade, linha, coluna):
    estado_atual = grade[linha][coluna]
    vizinhos = contar_materia(grade, linha, coluna)

    #Se vazia
    if estado_atual == 0:
        if vizinhos >= 3:
            return 1
        else:
            return 0

    #Se matéria
    elif estado_atual == 1:
        if vizinhos >= 6:
            return 2
        elif vizinhos >= 2:
            return 1
        else:
            return 0

    #Celula estrela
    elif estado_atual == 2:
        return 2

def proxima_geracao(grade):
    nova_grade = []

    for i in range(len(grade)):
        nova_linha = []

        for j in range(len(grade[0])):
            estado = proximo_estado(grade, i, j)
            nova_linha.append(estado)

        nova_grade.append(nova_linha)

    return nova_grade

#=============================TESTE===============================
#print("Geração Atual:")
#mostrar_grade(grade)

#nova_grade = proxima_geracao(grade)

#print("\nPróxima Geração:")
#mostrar_grade(nova_grade)
#=================================================================

def simular(grade, geracoes):
    for geracao in range(geracoes):
        print("\nGeração", geracao)
        mostrar_grade(grade)

        grade = proxima_geracao(grade)

def centro_grade(grade):
    centro_linha = len(grade) // 2
    centro_coluna = len(grade[0]) // 2

    return centro_linha, centro_coluna

def direcao_centro(grade, linha, coluna):
    centro_linha, centro_coluna = centro_grade(grade)

    nova_linha = linha 
    nova_coluna = coluna 

    if linha < centro_linha:
        nova_linha += 1
    elif linha > centro_linha:
        nova_linha -= 1

    if coluna < centro_coluna:
        nova_coluna += 1
    elif coluna > centro_coluna:
        nova_coluna -= 1

    return nova_linha, nova_coluna

def mover_materia(grade):
    nova_grade = []

    for i in range(len(grade)):
        linha = []

        for j in range(len(grade[0])):
            linha.append(0)

        nova_grade.append(linha)

    #Procura celulas de matéria
    for i in range(len(grade)):
        for j in range(len(grade[0])):
            if grade[i][j] == 1:

                nova_linha, nova_coluna = direcao_movimento(grade, i, j)
                nova_grade[nova_linha][nova_coluna] = 1

    return nova_grade

def direcao_rotacao(grade, linha, coluna):
    centro_linha, centro_coluna = centro_grade(grade)

    nova_linha = linha 
    nova_coluna = coluna 

    #Se acima do centro, move para direita
    if linha < centro_linha:
        if coluna < len(grade[0]) - 1:
            nova_coluna += 1

    #Se abaixo do centro, move para esquerda
    elif linha > centro_linha:
        if coluna > 0:
            nova_coluna -= 1

    #Se a esquerda do centro, move para cima
    if coluna < centro_coluna:
        if linha > 0:
            nova_linha -= 1

    #Se a direita do centro, move para baixo
    elif coluna > centro_coluna:
        if linha < len(grade) - 1:
            nova_linha += 1

    return nova_linha, nova_coluna

def direcao_movimento(grade, linha, coluna):
    #Movimento em direção ao centro
    centro_linha, centro_coluna = centro_grade(grade)

    if linha < centro_linha:
        atracao_linha = 1
    elif linha > centro_linha:
        atracao_linha = -1
    else:
        atracao_linha = 0

    if coluna < centro_coluna:
        atracao_coluna = 1
    elif coluna > centro_coluna:
        atracao_coluna = -1
    else:
        atracao_coluna = 0

    #Rotação
    rotacao_linha = 0
    rotacao_coluna = 0

    if linha < centro_linha:
        rotacao_coluna = 1
    elif linha > centro_linha:
        rotacao_coluna = -1

    if coluna < centro_coluna:
        rotacao_linha = -1
    elif coluna > centro_coluna:
        rotacao_linha = 1

    #Combinar movimentos
    movimento_linha = (2 * atracao_linha) + rotacao_linha
    movimento_coluna = (2 * atracao_coluna) + rotacao_coluna

    #Transforma o resultado em um passo de no máximo 1 célula
    if movimento_linha > 0:
        movimento_linha = 1
    elif movimento_linha < 0:
        movimento_linha = -1

    if movimento_coluna > 0:
        movimento_coluna = 1
    elif movimento_coluna < 0:
        movimento_coluna = -1

    nova_linha = linha + movimento_linha
    nova_coluna = coluna + movimento_coluna

    #Impede que saia da grade
    nova_linha = max(0, min(nova_linha, len(grade) - 1))
    nova_coluna = max(0, min(nova_coluna, len(grade[0]) - 1))

    return nova_linha, nova_coluna

class vizualizadorgrade


#=============================TESTE===============================
#mostrar_grade(grade)

#nova = mover_materia(grade)

#print("\nDepois do movimento:")

#mostrar_grade(nova)

grade_teste = [
    [0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

for geracao in range(5):

    print("\nGeração", geracao)
    mostrar_grade(grade_teste)

    grade_teste = mover_materia(grade_teste)
#=================================================================

#teste