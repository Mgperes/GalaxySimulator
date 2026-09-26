import pygame
import math
from config import *
from main import grade_aleatoria, proxima_geracao
from animacoes import GerenciadorAnimacoes, SistemaParticulas
from botoes import Botao, ControleEscorregavel, PainelConfiguracao, BarraFerramenta
from galaxia import GaláxiaRenderizador


class Estatisticas:
    """Calcula e armazena estatísticas da grade"""
    
    def __init__(self, grade):
        self.atualizar(grade)
    
    def atualizar(self, grade):
        """Calcula estatísticas da grade atual"""
        self.total_vazio = 0
        self.total_gas = 0
        self.total_halo = 0
        self.total_estrela = 0
        
        for linha in grade:
            for valor in linha:
                if valor == 0:
                    self.total_vazio += 1
                elif valor == 1:
                    self.total_gas += 1
                elif valor == 2:
                    self.total_halo += 1
                elif valor >= 3:
                    self.total_estrela += 1
        
        total = self.total_vazio + self.total_gas + self.total_halo + self.total_estrela
        self.percentual_gas = (self.total_gas / total * 100) if total > 0 else 0
        self.percentual_halo = (self.total_halo / total * 100) if total > 0 else 0
        self.percentual_estrela = (self.total_estrela / total * 100) if total > 0 else 0
    
    def __str__(self):
        return (f"Gás: {self.percentual_gas:.1f}% | "
                f"Halo: {self.percentual_halo:.1f}% | "
                f"Estrela: {self.percentual_estrela:.1f}%")


class PainelInformacoes:
    """Interface do HUD (informações, controles)"""
    
    def __init__(self, tela, altura_painel=ALTURA_HUD):
        self.tela = tela
        self.altura = altura_painel
        self.y = tela.get_height() - altura_painel
        self.fonte_principal = pygame.font.SysFont(FONTE_NOME, FONTE_PRINCIPAL)
        self.fonte_titulo = pygame.font.SysFont(FONTE_NOME, FONTE_TITULO, bold=True)
        self.fonte_pequena = pygame.font.SysFont(FONTE_NOME, FONTE_PEQUENA)
    
    def desenhar(self, geracao, pausado, estatisticas, velocidade):
        """Desenha o painel com informações e controles"""
        # Fundo do painel com gradiente sutil
        rect_painel = pygame.Rect(0, self.y, self.tela.get_width(), self.altura)
        pygame.draw.rect(self.tela, COR_PAINEL, rect_painel)
        pygame.draw.line(self.tela, COR_BORDA_PAINEL, 
                        (0, self.y), (self.tela.get_width(), self.y), 2)
        
        # Lado esquerdo - Informações
        texto_geracao = self.fonte_titulo.render(
            f"Geração {geracao}", True, COR_TEXTO
        )
        self.tela.blit(texto_geracao, (15, self.y + 10))
        
        # Status de pausa com indicador
        status = "⏸ PAUSADO" if pausado else "▶ SIMULANDO"
        cor_status = (200, 100, 100) if pausado else (100, 200, 100)
        texto_status = self.fonte_principal.render(status, True, cor_status)
        self.tela.blit(texto_status, (self.tela.get_width() - 200, self.y + 10))
        
        # Velocidade
        texto_vel = self.fonte_pequena.render(
            f"Velocidade: {velocidade}x", True, COR_TEXTO_SECUNDARIA
        )
        self.tela.blit(texto_vel, (self.tela.get_width() - 200, self.y + 35))
        
        # Estatísticas
        if ATIVAR_ESTATISTICAS:
            texto_stats = self.fonte_pequena.render(
                str(estatisticas), True, COR_TEXTO_SECUNDARIA
            )
            self.tela.blit(texto_stats, (15, self.y + 40))
        
        # Controles
        controles = "[ ESPAÇO ] pausar   [ R ] reiniciar   [ ↑↓ ] velocidade   [ C ] configurações"
        texto_controles = self.fonte_pequena.render(
            controles, True, COR_TEXTO_SECUNDARIA
        )
        self.tela.blit(texto_controles, 
                      (15, self.y + 60) if ATIVAR_ESTATISTICAS else (15, self.y + 40))


def main():
    """Loop principal da simulação com renderização de galáxia"""
    pygame.init()

    # Inicialização
    grade = grade_aleatoria(tamanho=TAMANHO_GRADE, densidade_inicial=0.10, semente=7)
    largura = len(grade[0]) * TAMANHO_CELULA
    altura = len(grade) * TAMANHO_CELULA + ALTURA_HUD

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Formação de galáxias — autômato celular")
    relogio = pygame.time.Clock()

    # Componentes
    painel_info = PainelInformacoes(tela)
    painel_config = PainelConfiguracao(tela)
    barra_ferramentas = BarraFerramenta(tela)
    gerenciador_anim = GerenciadorAnimacoes(grade)
    sistema_particulas = SistemaParticulas()
    renderizador_galaxia = GaláxiaRenderizador(tela, TAMANHO_GRADE, TAMANHO_GRADE)
    estatisticas = Estatisticas(grade)

    # Estados
    geracao = 0
    pausado = False
    rodando = True
    velocidade = GERACOES_POR_SEGUNDO

    # Loop principal
    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                elif evento.key == pygame.K_r:
                    grade = grade_aleatoria(tamanho=TAMANHO_GRADE, densidade_inicial=0.10)
                    geracao = 0
                    gerenciador_anim = GerenciadorAnimacoes(grade)
                    estatisticas.atualizar(grade)
                elif evento.key == pygame.K_UP:
                    velocidade = min(velocidade + 1, 20)
                elif evento.key == pygame.K_DOWN:
                    velocidade = max(velocidade - 1, 1)
                elif evento.key == pygame.K_c:
                    painel_config.alternar()
            
            # Atualizar componentes
            painel_config.atualizar(evento, mouse_pos)
            barra_ferramentas.atualizar(evento, mouse_pos)
            
            # Verificar botões da barra
            botao_clicado = barra_ferramentas.obter_botao_clicado()
            if botao_clicado == "config":
                painel_config.alternar()

        # Atualização da simulação
        if not pausado:
            grade_nova = proxima_geracao(grade, forca_rotacao=FORCA_ROTACAO)
            gerenciador_anim.atualizar_grade(grade_nova)
            grade = grade_nova
            estatisticas.atualizar(grade)
            geracao += 1
        
        # Atualizar animações e partículas
        gerenciador_anim.atualizar()
        sistema_particulas.atualizar()
        renderizador_galaxia.atualizar_rotacao()
        
        # Velocidade do painel config
        velocidade = painel_config.obter_velocidade()

        # Renderização com estilo de galáxia
        renderizador_galaxia.desenhar_grade_galaxia(tela, grade, gerenciador_anim)
        
        # Desenhar partículas
        sistema_particulas.desenhar(tela)
        
        # Desenhar painéis
        painel_info.desenhar(geracao, pausado, estatisticas, velocidade)
        painel_config.desenhar()

        pygame.display.flip()
        relogio.tick(velocidade)

    pygame.quit()


if __name__ == "__main__":
    main()