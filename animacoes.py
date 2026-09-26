"""
Sistema de animações e transições para células
"""

import math
from config import *


class TransicaoCelula:
    """Gerencia transição suave entre estados de uma célula"""
    
    def __init__(self, estado_inicial, estado_final, duracao_frames=10):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.duracao = duracao_frames
        self.tempo_decorrido = 0
        self.concluida = False
    
    def atualizar(self):
        """Avança a animação"""
        if not self.concluida:
            self.tempo_decorrido += 1
            if self.tempo_decorrido >= self.duracao:
                self.concluida = True
                self.tempo_decorrido = self.duracao
    
    def progresso(self):
        """Retorna valor 0-1 do progresso da animação"""
        return min(self.tempo_decorrido / self.duracao, 1.0)
    
    def cor_intermediaria(self, cor_inicio, cor_fim):
        """Interpola entre duas cores"""
        prog = self.progresso()
        r = int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * prog)
        g = int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * prog)
        b = int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * prog)
        return (r, g, b)


class GerenciadorAnimacoes:
    """Gerencia animações de todas as células"""
    
    def __init__(self, grade):
        self.animacoes = {}
        self.grade_anterior = [linha[:] for linha in grade]
    
    def atualizar_grade(self, grade_nova):
        """Detecta mudanças e cria animações"""
        for i in range(len(grade_nova)):
            for j in range(len(grade_nova[0])):
                if grade_nova[i][j] != self.grade_anterior[i][j]:
                    chave = (i, j)
                    self.animacoes[chave] = TransicaoCelula(
                        self.grade_anterior[i][j],
                        grade_nova[i][j],
                        duracao_frames=8
                    )
        
        self.grade_anterior = [linha[:] for linha in grade_nova]
    
    def atualizar(self):
        """Atualiza todas as animações"""
        chaves_removidas = []
        for chave, anim in self.animacoes.items():
            anim.atualizar()
            if anim.concluida:
                chaves_removidas.append(chave)
        
        for chave in chaves_removidas:
            del self.animacoes[chave]
    
    def obter_cor_animada(self, i, j, valor_atual):
        """Retorna cor interpolada se há animação, senão cor normal"""
        from efeitos import Efeitos
        
        chave = (i, j)
        if chave not in self.animacoes:
            return Efeitos.cor_da_celula(valor_atual)
        
        anim = self.animacoes[chave]
        cor_inicio = Efeitos.cor_da_celula(anim.estado_inicial)
        cor_fim = Efeitos.cor_da_celula(anim.estado_final)
        
        return anim.cor_intermediaria(cor_inicio, cor_fim)
    
    def obter_escala_animada(self, i, j):
        """Retorna escala para efeito de "pop" na animação"""
        chave = (i, j)
        if chave not in self.animacoes:
            return 1.0
        
        anim = self.animacoes[chave]
        prog = anim.progresso()
        
        # Efeito elástico: cresce e depois volta
        if prog < 0.5:
            return 1.0 + (prog * 2) * 0.1  # Cresce até 1.1
        else:
            return 1.1 - ((prog - 0.5) * 2) * 0.1  # Volta a 1.0


class Particula:
    """Pequenas partículas para efeitos visuais"""
    
    def __init__(self, x, y, vx, vy, duracao=20, cor=(255, 255, 255)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.duracao = duracao
        self.tempo = 0
        self.cor = cor
        self.viva = True
    
    def atualizar(self):
        """Atualiza posição e duração"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravidade
        self.tempo += 1
        
        if self.tempo >= self.duracao:
            self.viva = False
    
    def opacidade(self):
        """Retorna opacidade baseada no progresso"""
        prog = self.tempo / self.duracao
        return 1.0 - prog  # Desaparece gradualmente


class SistemaParticulas:
    """Gerencia sistema de partículas para efeitos"""
    
    def __init__(self):
        self.particulas = []
    
    def criar_explosao(self, x, y, quantidade=8, cor=(200, 100, 100)):
        """Cria efeito de explosão"""
        import math
        for i in range(quantidade):
            angulo = (2 * math.pi * i) / quantidade
            vx = math.cos(angulo) * 2
            vy = math.sin(angulo) * 2
            self.particulas.append(
                Particula(x, y, vx, vy, duracao=15, cor=cor)
            )
    
    def criar_brilho(self, x, y, quantidade=4, cor=(246, 194, 94)):
        """Cria efeito de brilho ascendente"""
        for i in range(quantidade):
            vx = (i - quantidade/2) * 0.3
            vy = -1.5
            self.particulas.append(
                Particula(x, y, vx, vy, duracao=20, cor=cor)
            )
    
    def atualizar(self):
        """Atualiza todas as partículas"""
        for p in self.particulas[:]:
            p.atualizar()
            if not p.viva:
                self.particulas.remove(p)
    
    def desenhar(self, tela):
        """Desenha todas as partículas"""
        import pygame
        for p in self.particulas:
            alfa = int(255 * p.opacidade())
            cor_com_alfa = (*p.cor, alfa)
            
            # Cria superfície com transparência
            surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(surf, cor_com_alfa, (2, 2), 2)
            tela.blit(surf, (int(p.x), int(p.y)))