import pygame
import datetime
import random

pygame.init()

pygame.display.set_caption("Space Looker")
fundoJogo = pygame.image.load("imagens/fundoJogo.jpg")
nave = pygame.image.load("imagens/nave.png")
icone = pygame.image.load("imagens/icone.png")
tiro = pygame.image.load("imagens/tiro.png")
pygame.display.set_icon(icone)
asteroide = pygame.image.load("imagens/asteroide.png")
escalaAsteroide = pygame.transform.scale(asteroide, (55, 55))
velocidadeAsteroide = random.randint(3, 8)
relogio = pygame.time.Clock()
tela = (1000, 700)
tamanhoTela = pygame.display.set_mode(tela)
preto = (0, 0, 0)
branco = (255, 255, 255)

# Posição e movimento da nave
posicaoXNave = 20
posicaoYNave = 350
movimentoXNave = 0
movimentoYNave = 0

tiro = 0
ultimoTiro = 200

# Múltiplos asteroides
NUM_ASTEROIDES = 10
asteroides = []
for _ in range(NUM_ASTEROIDES):
    x = 1000 + random.randint(0, 500)
    y = random.randint(0, 645)
    asteroides.append({'x': x, 'y': y})

# Variáveis do jogo
pausado = False
pontuacao = 0
fonteHora = pygame.font.Font(None, 20)
fontePontuacao = pygame.font.Font(None, 35)

while True:
    # --- Seção de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Evento de pausar o jogo
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            pausado = not pausado
            movimentoYNave = 0

        # Eventos de movimento (apenas se não estiver pausado)
        if not pausado:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    movimentoYNave = -8
                elif evento.key == pygame.K_DOWN:
                    movimentoYNave = 8

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    movimentoYNave = 0

    # --- Seção de Lógica do Jogo ---
    if not pausado:
        # Atualiza a posição da nave
        posicaoXNave += movimentoXNave
        posicaoYNave += movimentoYNave

        # Limita o movimento da nave na tela
        if posicaoXNave <= 20:
            posicaoXNave = 20
        elif posicaoXNave >= 855:
            posicaoXNave = 855

        if posicaoYNave <= 0:
            posicaoYNave = 0
        elif posicaoYNave >= 580:
            posicaoYNave = 580

        if tiro < ultimoTiro:
            tiro += 1

        # Move e reposiciona asteroides
        for ast in asteroides:
            ast['x'] -= velocidadeAsteroide
            if ast['x'] < -55:
                ast['x'] = 1000
                ast['y'] = random.randint(0, 645)

    # --- Seção de Colisão ---
    # Crie a hitbox da nave ANTES do loop de colisão
    nave_rect = pygame.Rect(
        posicaoXNave + 8,           # desloca para a direita
        posicaoYNave + 12,          # desloca para baixo
        nave.get_width() - 16,      # diminui largura
        nave.get_height() - 20      # diminui altura
    )

    for ast in asteroides:
        asteroide_rect = pygame.Rect(
            ast['x'] + 8,
            ast['y'] + 8,
            escalaAsteroide.get_width() - 16,
            escalaAsteroide.get_height() - 16
        )
        if nave_rect.colliderect(asteroide_rect):
            print("Você foi atingido por um asteroide!") #mostrar na tela de morte
            pygame.quit()
            exit()

    # --- Seção de Desenho na Tela ---
    tamanhoTela.blit(fundoJogo, (-120, 10))
    tamanhoTela.blit(nave, (posicaoXNave, posicaoYNave))
    for ast in asteroides:
        tamanhoTela.blit(escalaAsteroide, (ast['x'], ast['y']))

    # Se quiser visualizar as hitboxes, descomente abaixo:
    # pygame.draw.rect(tamanhoTela, (0,255,0), nave_rect, 2)
    # for ast in asteroides:
    #     asteroide_rect = pygame.Rect(
    #         ast['x'] + 8,
    #         ast['y'] + 8,
    #         escalaAsteroide.get_width() - 16,
    #         escalaAsteroide.get_height() - 16
    #     )
    #     pygame.draw.rect(tamanhoTela, (255,0,0), asteroide_rect, 2)

    # Atualiza e desenha a hora a cada quadro
    hora_atual = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    texto_hora = fonteHora.render(hora_atual, True, branco)
    tamanhoTela.blit(texto_hora, (10, 10))

    # Desenha a tela de Pause se o jogo estiver pausado
    if pausado:
        s = pygame.Surface(tela, pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        tamanhoTela.blit(s, (0, 0))

        fonte = pygame.font.Font(None, 74)
        fonte2 = pygame.font.Font(None, 40)

        texto = fonte.render("PAUSE", True, (255, 0, 0))
        texto2 = fonte2.render("Pressione espaço para retomar", True, branco)

        texto_rect = texto.get_rect(center=(tela[0] // 2, tela[1] // 2 - 30))
        texto2_rect = texto2.get_rect(center=(tela[0] // 2, tela[1] // 2 + 30))

        tamanhoTela.blit(texto, texto_rect)
        tamanhoTela.blit(texto2, texto2_rect)

    pygame.display.update()
    relogio.tick(60)