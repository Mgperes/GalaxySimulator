"""
Sistema de botões e componentes de interface
"""

import pygame
from config import *


class Botao:
    """Botão interativo com efeitos visuais"""
    
    def __init__(self, x, y, largura, altura, texto, cor_fundo, cor_texto, cor_hover=None, callback=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.cor_hover = cor_hover or self._adicionar_luminosidade(cor_fundo, 40)
        self.callback = callback
        
        self.mouse_sobre = False
        self.pressionado = False
        self.fonte = pygame.font.SysFont(FONTE_NOME, 14, bold=True)
    
    def _adicionar_luminosidade(self, cor, valor):
        """Aumenta a luminosidade de uma cor"""
        return tuple(min(c + valor, 255) for c in cor)
    
    def desenhar(self, tela):
        """Desenha o botão com efeitos"""
        # Sombra
        sombra_rect = self.rect.copy()
        sombra_rect.y += 2
        pygame.draw.rect(tela, (0, 0, 0), sombra_rect, border_radius=6)
        
        # Cor do botão (depende do estado)
        cor = self.cor_hover if self.mouse_sobre else self.cor_fundo
        if self.pressionado:
            cor = self._adicionar_luminosidade(cor, -20)
        
        # Botão principal
        pygame.draw.rect(tela, cor, self.rect, border_radius=6)
        pygame.draw.rect(tela, self.cor_texto, self.rect, width=2, border_radius=6)
        
        # Texto
        texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        tela.blit(texto_surface, texto_rect)
    
    def atualizar(self, evento, mouse_pos):
        """Atualiza estado do botão"""
        self.mouse_sobre = self.rect.collidepoint(mouse_pos)
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.mouse_sobre:
                self.pressionado = True
                if self.callback:
                    self.callback()
        
        elif evento.type == pygame.MOUSEBUTTONUP:
            self.pressionado = False
    
    def está_clicado(self):
        """Verifica se foi clicado"""
        return self.pressionado


class ControleEscorregavel:
    """Slider para controlar valores"""
    
    def __init__(self, x, y, largura, valor_min, valor_max, valor_inicial, label=""):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = 20
        self.valor_min = valor_min
        self.valor_max = valor_max
        self.valor = valor_inicial
        self.label = label
        
        self.rect_barra = pygame.Rect(x, y, largura, self.altura)
        self.rect_botao = pygame.Rect(x, y, 15, self.altura)
        
        self.arrastando = False
        self.fonte = pygame.font.SysFont(FONTE_NOME, 12)
    
    def desenhar(self, tela):
        """Desenha o slider"""
        # Label
        if self.label:
            texto = self.fonte.render(self.label, True, COR_TEXTO)
            tela.blit(texto, (self.x, self.y - 20))
        
        # Barra de fundo
        pygame.draw.rect(tela, COR_BORDA_PAINEL, self.rect_barra, border_radius=5)
        
        # Barra preenchida
        progresso = (self.valor - self.valor_min) / (self.valor_max - self.valor_min)
        largura_preenchida = self.largura * progresso
        rect_preenchida = pygame.Rect(self.x, self.y, largura_preenchida, self.altura)
        pygame.draw.rect(tela, CORES[1], rect_preenchida, border_radius=5)
        
        # Botão
        self.rect_botao.x = self.x + (largura_preenchida - self.rect_botao.width / 2)
        pygame.draw.rect(tela, COR_TEXTO, self.rect_botao, border_radius=5)
        pygame.draw.circle(tela, COR_TEXTO, self.rect_botao.center, 8)
        
        # Valor atual
        texto_valor = self.fonte.render(f"{self.valor:.1f}", True, COR_TEXTO_SECUNDARIA)
        tela.blit(texto_valor, (self.x + self.largura + 10, self.y))
    
    def atualizar(self, evento, mouse_pos):
        """Atualiza o slider"""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_botao.collidepoint(mouse_pos):
                self.arrastando = True
        
        elif evento.type == pygame.MOUSEBUTTONUP:
            self.arrastando = False
        
        elif evento.type == pygame.MOUSEMOTION and self.arrastando:
            # Calcula novo valor baseado na posição do mouse
            mouse_x = mouse_pos[0]
            mouse_x = max(self.x, min(mouse_x, self.x + self.largura))
            
            progresso = (mouse_x - self.x) / self.largura
            self.valor = self.valor_min + (self.valor_max - self.valor_min) * progresso


class PainelConfiguracao:
    """Painel de configuração com botões e controles"""
    
    def __init__(self, tela):
        self.tela = tela
        self.visivel = False
        self.largura = 300
        self.altura = 400
        self.x = (tela.get_width() - self.largura) // 2
        self.y = (tela.get_height() - self.altura) // 2
        
        self.fonte_titulo = pygame.font.SysFont(FONTE_NOME, 18, bold=True)
        self.fonte_normal = pygame.font.SysFont(FONTE_NOME, 12)
        
        # Botões
        self.botao_fechar = Botao(
            self.x + self.largura - 35, self.y + 10, 30, 30, "X",
            (200, 100, 100), COR_TEXTO,
            callback=self.fechar
        )
        
        self.botao_reiniciar = Botao(
            self.x + 15, self.y + self.altura - 50, 130, 35, "Reiniciar",
            CORES[1], COR_TEXTO,
            callback=lambda: None
        )
        
        self.botao_exportar = Botao(
            self.x + 155, self.y + self.altura - 50, 130, 35, "Exportar",
            CORES[2], COR_TEXTO,
            callback=lambda: None
        )
        
        # Sliders
        self.slider_velocidade = ControleEscorregavel(
            self.x + 15, self.y + 80, 270, 1, 10, 4, "Velocidade"
        )
    
    def abrir(self):
        """Abre o painel"""
        self.visivel = True
    
    def fechar(self):
        """Fecha o painel"""
        self.visivel = False
    
    def alternar(self):
        """Alterna visibilidade"""
        self.visivel = not self.visivel
    
    def desenhar(self):
        """Desenha o painel"""
        if not self.visivel:
            return
        
        # Fundo semi-transparente
        overlay = pygame.Surface((self.tela.get_width(), self.tela.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.tela.blit(overlay, (0, 0))
        
        # Painel
        pygame.draw.rect(self.tela, COR_PAINEL, 
                        (self.x, self.y, self.largura, self.altura),
                        border_radius=10)
        pygame.draw.rect(self.tela, COR_BORDA_PAINEL,
                        (self.x, self.y, self.largura, self.altura),
                        width=2, border_radius=10)
        
        # Título
        titulo = self.fonte_titulo.render("Configurações", True, COR_TEXTO)
        titulo_rect = titulo.get_rect(center=(self.x + self.largura // 2, self.y + 20))
        self.tela.blit(titulo, titulo_rect)
        
        # Componentes
        self.botao_fechar.desenhar(self.tela)
        self.slider_velocidade.desenhar(self.tela)
        self.botao_reiniciar.desenhar(self.tela)
        self.botao_exportar.desenhar(self.tela)
    
    def atualizar(self, evento, mouse_pos):
        """Atualiza painel"""
        if not self.visivel:
            return
        
        self.botao_fechar.atualizar(evento, mouse_pos)
        self.botao_reiniciar.atualizar(evento, mouse_pos)
        self.botao_exportar.atualizar(evento, mouse_pos)
        self.slider_velocidade.atualizar(evento, mouse_pos)
    
    def obter_velocidade(self):
        """Retorna velocidade do slider"""
        return int(self.slider_velocidade.valor)


class BarraFerramenta:
    """Barra de ferramentas com botões no topo"""
    
    def __init__(self, tela):
        self.tela = tela
        self.altura = 50
        self.botoes = []
        
        # Botão Configurações
        self.botao_config = Botao(
            10, 10, 40, 30, "⚙",
            CORES[1], COR_TEXTO,
            callback=lambda: None
        )
        self.botoes.append(("config", self.botao_config))
        
        # Botão Info
        self.botao_info = Botao(
            60, 10, 40, 30, "ℹ",
            CORES[2], COR_TEXTO,
            callback=lambda: None
        )
        self.botoes.append(("info", self.botao_info))
        
        self.fonte = pygame.font.SysFont(FONTE_NOME, 14)
    
    def desenhar(self):
        """Desenha barra de ferramentas"""
        # Fundo
        pygame.draw.rect(self.tela, COR_PAINEL, (0, 0, self.tela.get_width(), self.altura))
        pygame.draw.line(self.tela, COR_BORDA_PAINEL,
                        (0, self.altura), (self.tela.get_width(), self.altura), 2)
        
        # Botões
        for nome, botao in self.botoes:
            botao.desenhar(self.tela)
        
        # Título
        titulo = self.fonte.render("Formação de Galáxias", True, COR_TEXTO)
        self.tela.blit(titulo, (120, 12))
    
    def atualizar(self, evento, mouse_pos):
        """Atualiza barra"""
        for nome, botao in self.botoes:
            botao.atualizar(evento, mouse_pos)
    
    def obter_botao_clicado(self):
        """Retorna qual botão foi clicado"""
        for nome, botao in self.botoes:
            if botao.está_clicado():
                return nome
        return None