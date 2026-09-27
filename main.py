"""
LÓGICA DO AUTÔMATO CELULAR
Contém as regras de evolução e geração inicial da grade.
"""

import random

LIMIAR_HALO = 2
LIMIAR_ESTRELA = 4 
FORCA_FEEDBACK = 0.4
DISPERSAO_FEEDBACK = 0.12

#Viés gravitacional: quanto mais longe do centro, mais difícil formar halo/estrela
BONUS_HALO_BORDA = 4
BONUS_ESTRELA_BORDA = 6


def grade_aleatoria(tamanho, densidade_inicial=0.10, semente=None):
    """
    Gera uma grade inicial aleatória.
    
    Args:
        tamanho: Dimensão da grade (tamanho x tamanho)
        densidade_inicial: Proporção de células vivas (0-1)
        semente: Seed para reproducibilidade
    """
    if semente is not None:
        random.seed(semente)
    
    grade = []
    for i in range(tamanho):
        linha = [1 if random.random() < densidade_inicial else 0
                 for _ in range(tamanho)]
    
        grade.append(linha)
    
    return grade

def carregar_grade_de_arquivo(caminho):
    """
    Carrega o estado inicial a partir de um arquivo de texto.
    """
    grade = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha_texto in arquivo:
            linha_texto = linha_texto.strip()
            if not linha_texto:
                continue
            valores = [int(v) for v in linha_texto.split()]
            grade.append(valores)
 
    if not grade:
        raise ValueError(f"Arquivo '{caminho}' está vazio ou em formato inválido.")
 
    tamanho_linha = len(grade[0])
    for linha in grade:
        if len(linha) != tamanho_linha:
            raise ValueError(f"Arquivo '{caminho}' tem linhas de tamanhos diferentes.")
 
    return grade

def salvar_grade_em_arquivo(grade, caminho):
    """Salva a grade atual num arquivo de texto, no mesmo formato de leitura."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for linha in grade:
            arquivo.write(" ".join(str(v) for v in linha) + "\n")

def eh_materia(valor):
    return valor >= 1


def contar_vizinhos(grade, linha, coluna):
    """Conta células vivas na vizinhança 3x3."""
    cont = 0
    for i in range(linha - 1, linha + 2):
        for j in range(coluna - 1, coluna + 2):
            if i == linha and j == coluna:
                continue
            
            if 0 <= i < len(grade) and 0 <= j < len(grade[0]):
                if eh_materia(grade[i][j]):
                    cont += 1
    
    return cont

def bias_distancia(i, j, tamanho_l, tamanho_c):
    """
    Retorna 0 no centro da grade e se aproxima de 1 nas bordas —
    usado para dificultar a formação de halo/estrela longe do centro
    (o "poço gravitacional" simplificado da simulação).
    """
    centro_i = (tamanho_l - 1) / 2
    centro_j = (tamanho_c - 1) / 2
    dist_max = (centro_i ** 2 + centro_j ** 2) ** 0.5
    if dist_max == 0:
        return 0
    dist = ((i - centro_i) ** 2 + (j - centro_j) ** 2) ** 0.5
    return dist / dist_max

def proximo_estado_por_densidade(valor, vizinhos, bias=0.0):
    """Decide o novo estado de uma célula a partir da densidade acumulada e da distância do centro."""
    # Estrela é estado terminal: uma vez atingido, não regride.
    if valor >= LIMIAR_ESTRELA:
        return valor
 
    densidade_total = valor + vizinhos
    limiar_halo_efetivo = LIMIAR_HALO + bias * BONUS_HALO_BORDA
    limiar_estrela_efetivo = LIMIAR_ESTRELA + bias * BONUS_ESTRELA_BORDA
 
    if densidade_total >= limiar_estrela_efetivo:
        return LIMIAR_ESTRELA
    elif densidade_total >= limiar_halo_efetivo:
        return 2
    elif valor >= 1 or vizinhos >= 3:
        return 1
    else:
        return 0

def centro_grade(grade):
    centro_linha = (len(grade) - 1) / 2
    centro_coluna = (len(grade[0]) - 1) / 2
    return centro_linha, centro_coluna


def calcular_novo_pos(i, j, grade, forca_rotacao):
    """
    Calcula a nova posição de uma célula com matéria: atração ao
    centro + rotação tangencial (mais rápida perto do centro, o que
    gera o efeito de "enrolar" em espiral em vez de girar em bloco
    rígido).
    """
    centro_i, centro_j = centro_grade(grade)
 
    di = i - centro_i
    dj = j - centro_j
    distancia = max(0.5, (di ** 2 + dj ** 2) ** 0.5)
 
    atracao_i = -di / distancia
    atracao_j = -dj / distancia
 
    velocidade_angular = forca_rotacao / distancia
    rotacao_i = -dj * velocidade_angular
    rotacao_j = di * velocidade_angular
 
    movimento_i = atracao_i * 0.5 + rotacao_i
    movimento_j = atracao_j * 0.5 + rotacao_j
 
    passo_i = 1 if movimento_i > 0.3 else (-1 if movimento_i < -0.3 else 0)
    passo_j = 1 if movimento_j > 0.3 else (-1 if movimento_j < -0.3 else 0)
 
    nova_i = max(0, min(i + passo_i, len(grade) - 1))
    nova_j = max(0, min(j + passo_j, len(grade[0]) - 1))
 
    return nova_i, nova_j


def mover_para_centro(grade, forca_rotacao):
    """
    Move células em direção ao centro. Quando duas ou mais células
    caem na mesma posição, seus valores se SOMAM (acúmulo real de
    massa) — estrelas (valor >= LIMIAR_ESTRELA) ficam ancoradas, já
    que representam matéria que colapsou definitivamente.
    """
    novo_grade = [[0 for _ in range(len(grade[0]))] for _ in range(len(grade))]
 
    for i in range(len(grade)):
        for j in range(len(grade[0])):
            valor = grade[i][j]
            if valor == 0:
                continue
 
            if valor >= LIMIAR_ESTRELA:
                novo_grade[i][j] += valor
                continue
 
            nova_i, nova_j = calcular_novo_pos(i, j, grade, forca_rotacao)
            novo_grade[nova_i][nova_j] += valor
    
    return novo_grade

def aplicar_feedback_estelar(grade, forca=FORCA_FEEDBACK):
    """
    Feedback estelar: células estrela dispersam parte da densidade das
    células vizinhas, simulando ventos estelares e radiação de
    supernovas — é isso que impede o colapso gravitacional de consumir
    a grade inteira, criando um equilíbrio entre crescimento e dispersão.
    """
    linhas = len(grade)
    colunas = len(grade[0])
    nova = [linha[:] for linha in grade]
 
    for i in range(linhas):
        for j in range(colunas):
            valor = grade[i][j]
            if valor < LIMIAR_ESTRELA:
                continue
 
            excesso = (valor - LIMIAR_ESTRELA + 1) * forca
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < linhas and 0 <= nj < colunas:
                        nova[ni][nj] = max(0, nova[ni][nj] - excesso * DISPERSAO_FEEDBACK)
 
    return nova


def proxima_geracao(grade, forca_rotacao=1.2):
    """
    Calcula a próxima geração:
      1) move e acumula matéria (gravidade + rotação diferencial),
      2) aplica feedback estelar (dispersão ao redor de estrelas),
      3) reclassifica cada célula por densidade.
    """
    grade_movida = mover_para_centro(grade, forca_rotacao)
    grade_com_feedback = aplicar_feedback_estelar(grade_movida)
 
    tamanho_l = len(grade_com_feedback)
    tamanho_c = len(grade_com_feedback[0])
 
    nova_grade = []
    for i in range(tamanho_l):
        nova_linha = []
        for j in range(tamanho_c):
            valor = grade_com_feedback[i][j]
            vizinhos = contar_vizinhos(grade_com_feedback, i, j)
            bias = bias_distancia(i, j, tamanho_l, tamanho_c)
            nova_linha.append(proximo_estado_por_densidade(valor, vizinhos, bias))
        nova_grade.append(nova_linha)
 
    return nova_grade