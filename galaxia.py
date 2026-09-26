"""
Renderizador especializado para fazer parecer uma galáxia de verdade
Com movimento rotacional, núcleo brilhante e braços de galáxia
"""

import pygame
import math
import numpy as np
from config import *


class GaláxiaRenderizador:
    """Renderiza a simulação como uma galáxia real"""
    
    def __init__(self, tela, largura_grade, altura_grade):
        self.tela = tela
        self.largura_grade = largura_grade
        self.altura_grade = altura_grade
        
        # Centro da galáxia
        self.centro_x = largura_grade * TAMANHO_CELULA // 2
        self.centro_y = altura_grade * TAMANHO_CELULA // 2
        
        # Rotação
        self.angulo_rotacao = 0
        self.velocidade_rotacao = 0.02
        
        # Superfícies pré-renderizadas para performance
        self.cache_glow = {}
        
        # Cores da galáxia (gradiente)
        self.cor_nucleo = (255, 150, 0)      # Laranja quente
        self.cor_intermedio = (255, 200, 100)  # Amarelo
        self.cor_anel = (100, 150, 255)      # Azul
        self.cor_borda = (150, 100, 200)     # Roxo
    
    def calcular_distancia_centro(self, i, j):
        """Calcula distância de uma célula até o centro"""
        x = j * TAMANHO_CELULA + TAMANHO_CELULA // 2
        y = i * TAMANHO_CELULA + TAMANHO_CELULA // 2
        
        dist_x = x - self.centro_x
        dist_y = y - self.centro_y
        
        distancia = math.sqrt(dist_x**2 + dist_y**2)
        return distancia
    
    def calcular_angulo_centro(self, i, j):
        """Calcula ângulo de uma célula em relação ao centro"""
        x = j * TAMANHO_CELULA + TAMANHO_CELULA // 2
        y = i * TAMANHO_CELULA + TAMANHO_CELULA // 2
        
        dist_x = x - self.centro_x
        dist_y = y - self.centro_y
        
        angulo = math.atan2(dist_y, dist_x)
        return angulo
    
    def obter_cor_gradiente(self, distancia, valor):
        """Retorna cor baseada em distância do centro e tipo de célula"""
        max_dist = math.sqrt(self.centro_x**2 + self.centro_y**2)
        progresso = distancia / max_dist if max_dist > 0 else 0
        progresso = min(progresso, 1.0)
        
        # Cores diferentes por tipo
        if valor == 1:  # Gás
            # Gradiente de laranja (núcleo) → azul (borda)
            r = int(255 - progresso * 155)
            g = int(150 + progresso * 100)
            b = int(0 + progresso * 255)
        
        elif valor == 2:  # Halo
            # Roxo/Magenta
            r = int(200 - progresso * 100)
            g = int(100 + progresso * 50)
            b = int(200)
        
        else:  # Estrela
            # Branco/Amarelo muito brilhante
            r = 255
            g = 220
            b = 100
        
        return (r, g, b)
    
    def criar_brilho_galaxia(self, tela, pos_x, pos_y, cor, raio=15, intensidade=0.6):
        """Cria efeito de brilho tipo galáxia"""
        # Glow muito maior e mais suave
        tamanho = raio * 4
        if tamanho % 2 == 0:
            tamanho += 1
        
        surf = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        centro = tamanho // 2
        
        # Cria múltiplas camadas de glow
        for r in range(raio, 0, -1):
            alfa = int(255 * (1 - r / raio) ** 2 * intensidade)
            cor_glow = (*cor, alfa)
            pygame.draw.circle(surf, cor_glow, (centro, centro), r)
        
        # Blit na posição
        tela.blit(surf, (pos_x - centro, pos_y - centro))
    
    def desenhar_nucleo_galaxia(self, tela):
        """Desenha o núcleo brilhante no centro"""
        # Primeiro: glow imenso
        self.criar_brilho_galaxia(tela, self.centro_x, self.centro_y, 
                                  self.cor_nucleo, raio=80, intensidade=0.8)
        
        # Depois: núcleo sólido
        pygame.draw.circle(tela, self.cor_nucleo, 
                          (self.centro_x, self.centro_y), 30)
        
        # Brilho interno
        pygame.draw.circle(tela, (255, 255, 200), 
                          (self.centro_x, self.centro_y), 15)
    
    def desenhar_bracos_galaxia(self, tela, grade):
        """Desenha braços espirais da galáxia"""
        # Calcula posições e desenha linhas tipo braços
        for i in range(len(grade)):
            for j in range(len(grade[0])):
                if grade[i][j] > 0:
                    x = j * TAMANHO_CELULA + TAMANHO_CELULA // 2
                    y = i * TAMANHO_CELULA + TAMANHO_CELULA // 2
                    
                    distancia = self.calcular_distancia_centro(i, j)
                    
                    # Desenha linha do núcleo até a célula (tipo espiral)
                    if distancia > 50:  # Apenas fora do núcleo
                        alfa = int(50 * (1 - distancia / 300))
                        if alfa > 0:
                            cor_braco = (*self.cor_anel, alfa)
                            # Linha sutil conectando ao núcleo
                            pygame.draw.line(tela, self.cor_anel, 
                                           (self.centro_x, self.centro_y),
                                           (x, y), 1)
    
    def desenhar_celula_galaxia(self, tela, i, j, valor, distancia, 
                               cor_animada=None, escala=1.0):
        """Desenha célula no estilo de galáxia"""
        x = j * TAMANHO_CELULA + TAMANHO_CELULA // 2
        y = i * TAMANHO_CELULA + TAMANHO_CELULA // 2
        
        # Cor baseada em distância
        cor = cor_animada or self.obter_cor_gradiente(distancia, valor)
        
        # Glow maior no núcleo
        raio_glow = 15 if distancia < 100 else (8 if distancia < 200 else 4)
        intensidade_glow = 0.7 if valor >= 2 else 0.5
        
        self.criar_brilho_galaxia(tela, x, y, cor, 
                                raio=raio_glow, intensidade=intensidade_glow)
        
        # Célula principal (partículas pequenas)
        tamanho = int(3 * escala) if valor == 1 else int(5 * escala)
        pygame.draw.circle(tela, cor, (x, y), tamanho)
        
        # Brilho extra para estrelas
        if valor >= 3:
            pygame.draw.circle(tela, (255, 255, 200), (x, y), tamanho // 2)
    
    def desenhar_fundo_galaxia(self, tela):
        """Desenha fundo estrelado"""
        # Apenas uma vez, então cacheia seria melhor, mas para simplicidade:
        tela.fill(COR_FUNDO)
        
        # Algumas "estrelas de fundo" fixas (muito pequenas e fracas)
        np.random.seed(42)
        for _ in range(100):
            x = np.random.randint(0, tela.get_width())
            y = np.random.randint(0, tela.get_height())
            tamanho = np.random.randint(1, 2)
            cor_estrela_fundo = (50, 50, 100)
            pygame.draw.circle(tela, cor_estrela_fundo, (x, y), tamanho)
    
    def atualizar_rotacao(self):
        """Atualiza o ângulo de rotação (opcional)"""
        self.angulo_rotacao += self.velocidade_rotacao
        if self.angulo_rotacao >= 2 * math.pi:
            self.angulo_rotacao -= 2 * math.pi
    
    def desenhar_grade_galaxia(self, tela, grade, gerenciador_anim):
        """Desenha a grade como uma galáxia"""
        # Fundo estrelado
        self.desenhar_fundo_galaxia(tela)
        
        # Desenha braços (opcional, pode ser lento)
        # self.desenhar_bracos_galaxia(tela, grade)
        
        # Desenha cada célula
        for i, linha in enumerate(grade):
            for j, valor in enumerate(linha):
                if valor == 0:
                    continue
                
                distancia = self.calcular_distancia_centro(i, j)
                cor_animada = gerenciador_anim.obter_cor_animada(i, j, valor)
                escala_anim = gerenciador_anim.obter_escala_animada(i, j)
                
                self.desenhar_celula_galaxia(tela, i, j, valor, distancia, 
                                            cor_animada, escala_anim)
        
        # Desenha núcleo por cima de tudo
        self.desenhar_nucleo_galaxia(tela)


class Efeito3D:
    """Adiciona efeito de profundidade baseado em distância"""
    
    @staticmethod
    def obter_tamanho_por_profundidade(distancia, max_dist):
        """Quanto mais perto do centro, maior (efeito 3D)"""
        profundidade = 1 - (distancia / max_dist if max_dist > 0 else 0)
        tamanho_multiplier = 0.8 + profundidade * 0.4  # 0.8 a 1.2
        return tamanho_multiplier
    
    @staticmethod
    def obter_opacidade_por_profundidade(distancia, max_dist):
        """Células distantes são mais transparentes"""
        profundidade = 1 - (distancia / max_dist if max_dist > 0 else 0)
        opacidade = 0.7 + profundidade * 0.3  # 0.7 a 1.0
        return opacidade


class EfetoEspiral:
    """Movimento espiral das células (opcional)"""
    
    def __init__(self):
        self.tempo = 0
    
    def calcular_offset_espiral(self, distancia, angulo, velocidade=0.05):
        """Calcula deslocamento espiral"""
        # Quanto mais perto do centro, mais rápido gira
        rotacao = velocidade * self.tempo / (1 + distancia / 100)
        novo_angulo = angulo + rotacao
        
        return math.cos(novo_angulo), math.sin(novo_angulo)
    
    def atualizar(self):
        """Avança o tempo da espiral"""
        self.tempo += 1