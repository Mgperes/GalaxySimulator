"""
Efeitos visuais avançados: gradientes, sombras, glow, etc
"""

import pygame
import math
from config import *


class Efeitos:
    """Sistema de efeitos visuais"""
    
    @staticmethod
    def cor_da_celula(valor):
        """Retorna cor base da célula"""
        if valor >= 3:
            return COR_ESTRELA
        return CORES.get(valor, CORES[0])
    
    @staticmethod
    def criar_gradiente(largura, altura, cor_inicio, cor_fim, direcao="vertical"):
        """Cria uma superfície com gradiente"""
        surf = pygame.Surface((largura, altura))
        
        if direcao == "vertical":
            for y in range(altura):
                progresso = y / altura
                r = int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * progresso)
                g = int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * progresso)
                b = int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * progresso)
                pygame.draw.line(surf, (r, g, b), (0, y), (largura, y))
        else:  # horizontal
            for x in range(largura):
                progresso = x / largura
                r = int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * progresso)
                g = int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * progresso)
                b = int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * progresso)
                pygame.draw.line(surf, (r, g, b), (x, 0), (x, altura))
        
        return surf
    
    @staticmethod
    def aplicar_glow(tela, rect, cor, raio=RAIO_GLOW, intensidade=INTENSIDADE_GLOW):
        """Aplica efeito de glow suave ao redor da célula"""
        if not ATIVAR_GLOW:
            return
        
        tamanho = rect.width + raio * 4
        glow_surf = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        
        centro = tamanho // 2
        cor_clara = tuple(min(c + 100, 255) for c in cor)
        
        # Múltiplas camadas de glow com degradação
        for r in range(raio, 0, -1):
            alfa = int(255 * (1 - r / raio) * intensidade)
            cor_glow = (*cor_clara, alfa)
            pygame.draw.circle(glow_surf, cor_glow, (centro, centro), r)
        
        tela.blit(glow_surf, (rect.x - raio * 2, rect.y - raio * 2))
    
    @staticmethod
    def aplicar_sombra(tela, rect, offset_x=2, offset_y=2):
        """Aplica sombra suave embaixo da célula"""
        sombra_rect = rect.copy()
        sombra_rect.x += offset_x
        sombra_rect.y += offset_y
        
        sombra_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(sombra_surf, (0, 0, 0, 80), sombra_surf.get_rect(), border_radius=4)
        tela.blit(sombra_surf, sombra_rect)
    
    @staticmethod
    def desenhar_celula_gas(tela, rect, cor, escala=1.0):
        """Desenha célula de gás com padrão de partículas"""
        # Sombra
        Efeitos.aplicar_sombra(tela, rect)
        
        # Glow
        Efeitos.aplicar_glow(tela, rect, cor)
        
        # Célula principal com gradiente
        tamanho_escalado = int(rect.width * escala)
        offset = (rect.width - tamanho_escalado) // 2
        
        rect_escalado = pygame.Rect(
            rect.x + offset, rect.y + offset,
            tamanho_escalado, tamanho_escalado
        )
        
        pygame.draw.ellipse(tela, cor, rect_escalado)
        pygame.draw.ellipse(tela, tuple(min(c + 50, 255) for c in cor), 
                          rect_escalado, width=1)
        
        # Pontos de partículas
        cx, cy = rect.centerx, rect.centery
        for i in range(3):
            offset_x = 4 * math.cos(i * math.pi / 1.5)
            offset_y = 4 * math.sin(i * math.pi / 1.5)
            pygame.draw.circle(tela, tuple(min(c + 80, 255) for c in cor),
                             (int(cx + offset_x), int(cy + offset_y)), 1)
    
    @staticmethod
    def desenhar_celula_halo(tela, rect, cor, escala=1.0):
        """Desenha célula halo com efeito de anéis"""
        # Sombra
        Efeitos.aplicar_sombra(tela, rect)
        
        # Glow mais intenso
        Efeitos.aplicar_glow(tela, rect, cor, raio=4, intensidade=0.5)
        
        tamanho_escalado = int(rect.width * escala)
        offset = (rect.width - tamanho_escalado) // 2
        
        # Quadrado interno (núcleo)
        rect_interno = pygame.Rect(
            rect.x + offset + 2, rect.y + offset + 2,
            tamanho_escalado - 4, tamanho_escalado - 4
        )
        
        cor_clara = tuple(min(c + 60, 255) for c in cor)
        pygame.draw.rect(tela, cor_clara, rect_interno, border_radius=3)
        pygame.draw.rect(tela, cor, rect_interno, width=2, border_radius=3)
        
        # Anel externo
        rect_anel = pygame.Rect(
            rect.x + offset, rect.y + offset,
            tamanho_escalado, tamanho_escalado
        )
        pygame.draw.rect(tela, cor, rect_anel, width=1, border_radius=2)
    
    @staticmethod
    def desenhar_celula_estrela(tela, rect, cor, escala=1.0):
        """Desenha célula estrela com brilho central"""
        # Sombra mais pronunciada
        Efeitos.aplicar_sombra(tela, rect, offset_y=3)
        
        # Glow muito intenso
        Efeitos.aplicar_glow(tela, rect, cor, raio=5, intensidade=0.7)
        
        tamanho_escalado = int(rect.width * escala)
        offset = (rect.width - tamanho_escalado) // 2
        
        # Quadrado externo
        rect_principal = pygame.Rect(
            rect.x + offset, rect.y + offset,
            tamanho_escalado, tamanho_escalado
        )
        
        pygame.draw.rect(tela, cor, rect_principal, border_radius=2)
        
        # Brilho central
        raio_brilho = max(tamanho_escalado // 3, 2)
        cor_brilho = tuple(min(c + 100, 255) for c in cor)
        pygame.draw.circle(tela, cor_brilho, rect_principal.center, raio_brilho)
        
        # Pequenas "chamas" nos cantos
        tamanho_chama = max(tamanho_escalado // 5, 1)
        cantos = [
            (rect_principal.topleft, (-1, -1)),
            (rect_principal.topright, (1, -1)),
            (rect_principal.bottomleft, (-1, 1)),
            (rect_principal.bottomright, (1, 1))
        ]
        
        for canto, direcao in cantos:
            cx = canto[0] + direcao[0] * tamanho_chama
            cy = canto[1] + direcao[1] * tamanho_chama
            pygame.draw.circle(tela, (255, 200, 100), (cx, cy), tamanho_chama // 2)
    
    @staticmethod
    def desenhar_celula_detalhada(tela, rect, valor, escala=1.0, cor_customizada=None):
        """Desenha célula com tipo específico e efeitos"""
        
        cor = cor_customizada or Efeitos.cor_da_celula(valor)
        
        if valor == 0:  # Vazio
            return
        elif valor == 1:  # Gás
            Efeitos.desenhar_celula_gas(tela, rect, cor, escala)
        elif valor == 2:  # Halo
            Efeitos.desenhar_celula_halo(tela, rect, cor, escala)
        elif valor >= 3:  # Estrela
            Efeitos.desenhar_celula_estrela(tela, rect, cor, escala)
        
        # Bordas se ativado
        if ATIVAR_BORDAS:
            pygame.draw.rect(tela, COR_BORDA_CELULA, rect, ESPESSURA_BORDA, border_radius=2)


class RenderedorGradiente:
    """Pré-renderiza gradientes para melhor performance"""
    
    def __init__(self):
        self.cache = {}
    
    def obter_gradiente(self, largura, altura, cor_inicio, cor_fim, chave):
        """Retorna gradiente do cache ou cria novo"""
        if chave not in self.cache:
            self.cache[chave] = Efeitos.criar_gradiente(
                largura, altura, cor_inicio, cor_fim
            )
        return self.cache[chave]
    
    def limpar_cache(self):
        """Limpa cache de gradientes"""
        self.cache.clear()