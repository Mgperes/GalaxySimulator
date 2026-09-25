import random

def grade_aleatoria(tamanho=15, densidade_inicial=0.12, semente=None):
    if semente is not None:
        random.seed(semente)

    grade = []
    for i in range(tamanho):
        linha = []
        for j in range(tamanho):
            if random.random() < densidade_inicial:
                linha.append(1)
            else:
                linha.append(0)
        grade.append(linha)
    return grade


def mostrar_grade(grade):
    for linha in grade:
        for celula in linha:
            if celula == 0:
                print(".", end=" ")
            elif celula == 1:
                print("•", end=" ")
            elif celula == 2:
                print("○", end=" ")
            elif celula >= 3:
                print("★", end=" ")
        print()


def eh_materia(valor):
    return valor >= 1


def contar_materia(grade, linha, coluna):
    cont = 0
    for i in range(linha - 1, linha + 2):
        for j in range(coluna - 1, coluna + 2):
            if i == linha and j == coluna:
                continue
            if 0 <= i < len(grade) and 0 <= j < len(grade[0]):
                if eh_materia(grade[i][j]):
                    cont += 1
    return cont


def centro_grade(grade):
    centro_linha = (len(grade) - 1) / 2
    centro_coluna = (len(grade[0]) - 1) / 2
    return centro_linha, centro_coluna


def direcao_movimento(grade, linha, coluna, forca_rotacao=1.0):
    centro_linha, centro_coluna = centro_grade(grade)

    dl = linha - centro_linha
    dc = coluna - centro_coluna
    distancia = max(0.5, (dl ** 2 + dc ** 2) ** 0.5)

    # vetor de atração: aponta para o centro
    atracao_linha = -dl / distancia
    atracao_coluna = -dc / distancia

    # vetor tangencial (rotação de 90° do vetor radial),
    # com velocidade angular maior perto do centro
    velocidade_angular = forca_rotacao / distancia
    rotacao_linha = -dc * velocidade_angular
    rotacao_coluna = dl * velocidade_angular

    movimento_linha = atracao_linha * 0.5 + rotacao_linha
    movimento_coluna = atracao_coluna * 0.5 + rotacao_coluna

    # reduz a um passo de no máximo 1 célula em cada eixo
    passo_linha = 1 if movimento_linha > 0.3 else (-1 if movimento_linha < -0.3 else 0)
    passo_coluna = 1 if movimento_coluna > 0.3 else (-1 if movimento_coluna < -0.3 else 0)

    nova_linha = linha + passo_linha
    nova_coluna = coluna + passo_coluna

    nova_linha = max(0, min(nova_linha, len(grade) - 1))
    nova_coluna = max(0, min(nova_coluna, len(grade[0]) - 1))

    return nova_linha, nova_coluna


LIMIAR_HALO = 2     # densidade acumulada mínima para virar halo (2)
LIMIAR_ESTRELA = 4  # densidade acumulada mínima para virar estrela (3+)


def mover_materia(grade, forca_rotacao=1.0):
    tamanho_l = len(grade)
    tamanho_c = len(grade[0])
    nova_grade = [[0 for _ in range(tamanho_c)] for _ in range(tamanho_l)]

    for i in range(tamanho_l):
        for j in range(tamanho_c):
            valor = grade[i][j]
            if valor == 0:
                continue

            if valor >= LIMIAR_ESTRELA:
                # estrela já colapsou: fica parada, mas acumula o que cair nela
                nova_grade[i][j] += valor
                continue

            nova_linha, nova_coluna = direcao_movimento(grade, i, j, forca_rotacao)
            nova_grade[nova_linha][nova_coluna] += valor

    return nova_grade


def proximo_estado_por_densidade(valor, vizinhos):
    # já é estrela: estado terminal, não regride
    if valor >= LIMIAR_ESTRELA:
        return valor

    densidade_total = valor + vizinhos

    if densidade_total >= LIMIAR_ESTRELA + 2:
        return LIMIAR_ESTRELA
    elif densidade_total >= LIMIAR_HALO:
        return 2
    elif valor >= 1 or vizinhos >= 3:
        return 1
    else:
        return 0


def proxima_geracao(grade, forca_rotacao=1.0):
    grade_movida = mover_materia(grade, forca_rotacao)

    nova_grade = []
    for i in range(len(grade_movida)):
        nova_linha = []
        for j in range(len(grade_movida[0])):
            valor = grade_movida[i][j]
            vizinhos = contar_materia(grade_movida, i, j)
            nova_linha.append(proximo_estado_por_densidade(valor, vizinhos))
        nova_grade.append(nova_linha)

    return nova_grade


#==================================================================
# SIMULAÇÃO
#==================================================================

def simular(grade, geracoes, forca_rotacao=1.0):
    for geracao in range(geracoes):
        print("\nGeração", geracao)
        mostrar_grade(grade)
        grade = proxima_geracao(grade, forca_rotacao)
    return grade


#=============================TESTE===============================
if __name__ == "__main__":
    grade_inicial = grade_aleatoria(tamanho=15, densidade_inicial=0.12, semente=7)
    simular(grade_inicial, geracoes=10, forca_rotacao=1.2)
#===================================================================