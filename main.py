"""
LÓGICA DO AUTÔMATO CELULAR
Contém as regras de evolução e geração inicial da grade.
Não depende de pygame — código puro de simulação.
"""

import random


def grade_aleatoria(tamanho, densidade_inicial=0.10, semente=None):
    """
    Gera uma grade inicial aleatória.
    
    Args:
        tamanho: Dimensão da grade (tamanho x tamanho)
        densidade_inicial: Proporção de células vivas (0-1)
        semente: Seed para reproducibilidade
    
    Returns:
        Lista 2D representando a grade
    """
    if semente is not None:
        random.seed(semente)
    
    grade = []
    for i in range(tamanho):
        linha = []
        for j in range(tamanho):
            valor = 1 if random.random() < densidade_inicial else 0
            linha.append(valor)
        grade.append(linha)
    
    return grade


def contar_vizinhos(grade, linha, coluna):
    """Conta células vivas na vizinhança 3x3."""
    cont = 0
    for i in range(linha - 1, linha + 2):
        for j in range(coluna - 1, coluna + 2):
            if i == linha and j == coluna:
                continue
            
            if 0 <= i < len(grade) and 0 <= j < len(grade[0]):
                if grade[i][j] > 0:
                    cont += 1
    
    return cont


def aplicar_regras(grade, valor, vizinhos):
    """Aplica regras de evolução."""
    if valor == 0:  # Vazio
        if vizinhos >= 3:
            return 1  # Nasce gás
        return 0
    
    elif valor == 1:  # Gás
        if vizinhos >= 6:
            return 2  # Evolui para halo
        elif vizinhos >= 2:
            return 1  # Permanece gás
        else:
            return 0  # Morre
    
    elif valor >= 2:  # Halo ou Estrela
        return valor  # Permanece estável


def proxima_geracao(grade, forca_rotacao=1.2):
    """
    Calcula a próxima geração aplicando:
    1. Regras de evolução (nascimento, morte, evolução)
    2. Movimento em direção ao centro
    """
    # Passo 1: Aplicar regras
    nova_grade = []
    for i in range(len(grade)):
        nova_linha = []
        for j in range(len(grade[0])):
            vizinhos = contar_vizinhos(grade, i, j)
            novo_estado = aplicar_regras(grade, grade[i][j], vizinhos)
            nova_linha.append(novo_estado)
        nova_grade.append(nova_linha)
    
    # Passo 2: Aplicar movimento
    grade_movida = mover_para_centro(nova_grade, forca_rotacao)
    
    return grade_movida


def mover_para_centro(grade, forca_rotacao):
    """Move células em direção ao centro com efeito de rotação."""
    novo_grade = []
    for i in range(len(grade)):
        linha = []
        for j in range(len(grade[0])):
            linha.append(0)
        novo_grade.append(linha)
    
    centro_i = len(grade) // 2
    centro_j = len(grade[0]) // 2
    
    for i in range(len(grade)):
        for j in range(len(grade[0])):
            if grade[i][j] > 0:
                nova_i, nova_j = calcular_novo_pos(
                    i, j, centro_i, centro_j, len(grade), len(grade[0]), forca_rotacao
                )
                novo_grade[nova_i][nova_j] = grade[i][j]
    
    return novo_grade


def calcular_novo_pos(i, j, ci, cj, altura, largura, forca_rotacao):
    """Calcula nova posição com atração ao centro + rotação."""
    atracao_i = 2 * (1 if i < ci else (-1 if i > ci else 0))
    atracao_j = 2 * (1 if j < cj else (-1 if j > cj else 0))
    
    rotacao_i = 1 if j < cj else (-1 if j > cj else 0)
    rotacao_j = 1 if i > ci else (-1 if i < ci else 0)
    
    movimento_i = int(atracao_i + forca_rotacao * rotacao_i)
    movimento_j = int(atracao_j + forca_rotacao * rotacao_j)
    
    movimento_i = max(-1, min(1, movimento_i))
    movimento_j = max(-1, min(1, movimento_j))
    
    nova_i = i + movimento_i
    nova_j = j + movimento_j
    
    nova_i = max(0, min(nova_i, altura - 1))
    nova_j = max(0, min(nova_j, largura - 1))
    
    return nova_i, nova_j