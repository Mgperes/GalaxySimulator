# Galaxy Simulator

Simulador de formação de galáxias baseado em um autômato celular. A matéria se move em direção ao centro da grade, recebe um componente de rotação e muda de estado conforme a densidade acumulada ao redor.

## Requisitos

- Python 3.10 ou superior
- `pygame`

Instale a dependência com:

```bash
python -m pip install pygame
```

## Como executar

### Visualizador gráfico

```bash
python vizualizador.py
```

Controles:

- `Espaço`: pausar ou continuar a simulação
- `R`: gerar uma nova grade e reiniciar a contagem de gerações
- Fechar a janela: encerrar o programa

### Modo de terminal

```bash
python main.py
```

Esse modo imprime a grade no terminal durante 10 gerações.

## Estados da matéria

| Estado | Valor | Representação |
| --- | ---: | --- |
| Vazio | `0` | `.` |
| Gás | `1` | `•` |
| Halo | `2` | `○` |
| Estrela | `3` ou mais | `★` |

Estrelas são estados terminais: depois de formadas, permanecem na posição e continuam acumulando matéria.

## Configuração

Os principais parâmetros estão em `config.py`:

- `TAMANHO_GRADE`: quantidade de células da grade
- `TAMANHO_CELULA`: tamanho visual de cada célula em pixels
- `GERACOES_POR_SEGUNDO`: velocidade da simulação
- `FORCA_ROTACAO`: intensidade do movimento orbital

As regras do autômato e as funções de geração de estados ficam em `main.py`; o desenho da janela fica em `vizualizador.py`.

Esse é um trabalho feito para a disciplina de Computação Científica, para cunho científico e acadêmico