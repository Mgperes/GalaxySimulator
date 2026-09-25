import pygame
from config import *
from main import grade_aleatoria, proxima_geracao


def cor_da_celula(valor):
    if valor >= 3:
        return COR_ESTRELA
    return CORES.get(valor, CORES[0])


def desenhar_grade(tela, grade):
    for i, linha in enumerate(grade):
        for j, valor in enumerate(linha):
            rect = pygame.Rect(
                j * TAMANHO_CELULA, i * TAMANHO_CELULA,
                TAMANHO_CELULA, TAMANHO_CELULA
            )
            pygame.draw.rect(tela, cor_da_celula(valor), rect)


def desenhar_info(tela, fonte, altura, geracao, pausado):
    texto = fonte.render(
        f"geração {geracao}   [espaço] pausar   [r] reiniciar", 
        True, COR_TEXTO
    )
    tela.blit(texto, (6, altura - 24))


def main():
    pygame.init()

    grade = grade_aleatoria(tamanho=TAMANHO_GRADE, densidade_inicial=0.10, semente=7)
    largura = len(grade[0]) * TAMANHO_CELULA
    altura = len(grade) * TAMANHO_CELULA + 30

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Formação de galáxias — autômato celular")
    fonte = pygame.font.SysFont(FONTE_NOME, FONTE_TAMANHO)
    relogio = pygame.time.Clock()

    geracao = 0
    pausado = False
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                elif evento.key == pygame.K_r:
                    grade = grade_aleatoria(tamanho=TAMANHO_GRADE, densidade_inicial=0.10)
                    geracao = 0

        if not pausado:
            grade = proxima_geracao(grade, forca_rotacao=FORCA_ROTACAO)
            geracao += 1

        tela.fill(COR_FUNDO)
        desenhar_grade(tela, grade)
        desenhar_info(tela, fonte, altura, geracao, pausado)

        pygame.display.flip()
        relogio.tick(GERACOES_POR_SEGUNDO)

    pygame.quit()


if __name__ == "__main__":
    main()