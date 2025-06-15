import os, pygame, datetime, random, time, threading
from recursos.funcoes import speak, salvar_partida, ler_ultimas_partidas, reconhecer_nome

#Git push origin main
#global dá pra puxar em qualquer lugar do código

pygame.init()
pygame.display.set_caption("Space Looker")
fundoJogo = pygame.image.load("imagens/fundoJogo.jpg")
nave = pygame.image.load("imagens/nave.png")
icone = pygame.image.load("imagens/icone.png")
tiro = pygame.image.load("imagens/tiro.png")
pygame.display.set_icon(icone)
asteroide = pygame.image.load("imagens/asteroide.png")
escalaAsteroide = pygame.transform.scale(asteroide, (55, 55))
velocidadeAsteroide = random.randint(3, 6)
relogio = pygame.time.Clock()
tela = (1000, 700)
telaPrincipal = pygame.display.set_mode(tela)
preto = (0, 0, 0)
branco = (255, 255, 255)
roxo = (200, 0, 128)
cinza = (192, 192, 192)
vermelho = (255, 0, 0)
pygame.mixer.music.load("imagens/fundoCerto.mp3")
pygame.mixer.music.play(-1, 0, 1000000)  

LOG_PATH = "log.dat"

def tela_inicio():
    fonte = pygame.font.Font(None, 110)  
    fonte2 = pygame.font.Font(None, 36)
    input_box = pygame.Rect(tela[0]//2 - 150, tela[1]//2, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active
    active = False
    text = ''
    botao_rect = pygame.Rect(tela[0]//2 - 75, tela[1]//2 + 80, 150, 50)
    botao_color = (128, 0, 180)
    botao_hover = (255, 255, 255)
    botao_fala_rect = pygame.Rect(tela[0]//2 - 75, tela[1]//2 + 150, 150, 50)
    rodando = True
    nome = ''
    blink = True
    blink_timer = 0
    blink_interval = 1000  # ms

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if botao_rect.collidepoint(event.pos):
                    nome = text.strip() if text.strip() else "Jogador"
                    rodando = False
                if botao_fala_rect.collidepoint(event.pos):
                    nome_falado = reconhecer_nome()
                    if nome_falado:
                        text = nome_falado
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        nome = text.strip() if text.strip() else "Jogador"
                        rodando = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 15:
                            text += event.unicode

        telaPrincipal.blit(fundoJogo, (0, 0))

        fade = pygame.Surface(tela, pygame.SRCALPHA)
        fade.fill((0, 0, 0, 180))
        telaPrincipal.blit(fade, (0, 0))

        blink_timer += relogio.get_time()
        if blink_timer > blink_interval:
            blink = not blink
            blink_timer = 0

        if blink:
            titulo = fonte.render("Space Looker", True, (255, 0, 255))
        else:
            titulo = fonte.render("Space Looker", True, (60, 0, 60))

        telaPrincipal.blit(titulo, (tela[0]//2 - titulo.get_width()//2, tela[1]//2 - 180))
        instr = fonte2.render("Digite seu nome ou use o microfone:", True, branco)
        telaPrincipal.blit(instr, (tela[0]//2 - instr.get_width()//2, tela[1]//2 - 40))
        pygame.draw.rect(telaPrincipal, branco, input_box, 2)
        txt_surface = fonte2.render(text, True, branco)
        telaPrincipal.blit(txt_surface, (input_box.x+5, input_box.y+10))
        input_box.w = max(300, txt_surface.get_width()+10)
        mouse = pygame.mouse.get_pos()
        cor_botao = botao_hover if botao_rect.collidepoint(mouse) else botao_color
        pygame.draw.rect(telaPrincipal, cor_botao, botao_rect)
        botao_txt = fonte2.render("Iniciar Jogo", True, preto)
        telaPrincipal.blit(botao_txt, (botao_rect.x + (150-botao_txt.get_width())//2, botao_rect.y + 10))
        cor_botao_fala = botao_hover if botao_fala_rect.collidepoint(mouse) else botao_color
        pygame.draw.rect(telaPrincipal, cor_botao_fala, botao_fala_rect)
        botao_fala_txt = fonte2.render("Falar nome", True, preto)
        telaPrincipal.blit(botao_fala_txt, (botao_fala_rect.x + (150-botao_fala_txt.get_width())//2, botao_fala_rect.y + 10))
        pygame.display.flip()
        relogio.tick(60)
    return nome

def tela_intro(nome):
    fonte = pygame.font.Font(None, 48)
    fonte2 = pygame.font.Font(None, 32)
    historia = [
        "Em um universo distante, você é o último piloto",
        "capaz de salvar a galáxia dos invasores cósmicos.",
        "",
        "Controles: Use as setas para mover e S para atirar.",
        "",
        "Prepare-se!"
    ]
    timer = 10
    last_tick = time.time()
    speak(f"Bem vindo {nome}")

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        telaPrincipal.blit(fundoJogo, (-120, 10))

        fade = pygame.Surface(tela, pygame.SRCALPHA)
        fade.fill((0, 0, 0, 180))  
        telaPrincipal.blit(fade, (0, 0))

        titulo = fonte.render(f"Bem-vindo ao Space Looker, {nome}!", True, roxo)
        telaPrincipal.blit(titulo, (tela[0]//2 - titulo.get_width()//2, 80))
        for i, linha in enumerate(historia):
            texto = fonte2.render(linha, True, branco)
            telaPrincipal.blit(texto, (tela[0]//2 - texto.get_width()//2, 200 + i*40))
        timer_txt = fonte2.render(f"O jogo começa em {timer} segundos...", True, vermelho)
        telaPrincipal.blit(timer_txt, (tela[0]//2 - timer_txt.get_width()//2, tela[1] - 100))
        pygame.display.flip()
        if time.time() - last_tick >= 1:
            timer -= 1
            last_tick = time.time()
        if timer <= 0:
            rodando = False
        relogio.tick(60)

def tela_morte(pontuacao, nome_jogador):
    salvar_partida(pontuacao, nome_jogador)
    ultimas = ler_ultimas_partidas()
    fonte = pygame.font.Font(None, 60)
    fonte2 = pygame.font.Font(None, 36)
    rodando = True
    voltar_inicio = False
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    rodando = False
                if event.key == pygame.K_SPACE:
                    voltar_inicio = True
                    rodando = False

        telaPrincipal.blit(fundoJogo, (0, 0))
        fade = pygame.Surface(tela, pygame.SRCALPHA)
        fade.fill((0, 0, 0, 200))
        telaPrincipal.blit(fade, (0, 0))

        texto = fonte.render("VOCÊ MORREU!", True, (255, 0, 0))
        telaPrincipal.blit(texto, (tela[0]//2 - texto.get_width()//2, 80))
        texto2 = fonte2.render(f"{nome_jogador} - Sua pontuação: {pontuacao}", True, branco)
        telaPrincipal.blit(texto2, (tela[0]//2 - texto2.get_width()//2, 180))

        texto3 = fonte2.render("Últimas 5 partidas:", True, branco)
        telaPrincipal.blit(texto3, (tela[0]//2 - texto3.get_width()//2, 250))

        for i, partida in enumerate(ultimas):
            linha = fonte2.render(
                f"{i+1}. {partida.get('nome','?')} - {partida['pontuacao']} pontos - {partida['datahora']}",
                True, branco
            )
            telaPrincipal.blit(linha, (tela[0]//2 - linha.get_width()//2, 300 + i*40))

        texto4 = fonte2.render("Pressione ENTER para sair", True, branco)
        telaPrincipal.blit(texto4, (tela[0]//2 - texto4.get_width()//2, tela[1] - 80))

        texto5 = fonte2.render("Ou pressione ESPAÇO para voltar ao início", True, branco)
        telaPrincipal.blit(texto5, (tela[0]//2 - texto5.get_width()//2, tela[1] - 40))

        pygame.display.flip()
        relogio.tick(60)
    return voltar_inicio

decorativo_pos = [random.randint(100, 900), random.randint(100, 600)]
decorativo_vel = [random.choice([-1, 1]) * random.uniform(0.5, 1.5), random.choice([-1, 1]) * random.uniform(0.5, 1.5)]
decorativo_raio = 18
decorativo_cor = (roxo)  


sol_pos = (80, 80)  
sol_raio_base = 40
sol_raio = sol_raio_base
sol_pulse_direcao = 1  
sol_pulse_vel = 0.3   

while True:
    global nome_jogador
    nome_jogador = tela_inicio()
    tela_intro(nome_jogador)

    posicaoXNave = 20
    posicaoYNave = 350
    movimentoXNave = 0
    movimentoYNave = 0

    velocidadeTiro = 20
    tiros = [] 

    NUM_ASTEROIDES = 10
    asteroides = []
    for _ in range(NUM_ASTEROIDES):
        x = 1000 + random.randint(0, 500)
        y = random.randint(0, 645)
        asteroides.append({'x': x, 'y': y})

    pausado = False
    pontuacao = 0
    fonteHora = pygame.font.Font(None, 20)
    fontePontuacao = pygame.font.Font(None, 35)

    jogando = True
    while jogando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
                movimentoYNave = 0

            if not pausado:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        movimentoYNave = -10
                    elif evento.key == pygame.K_DOWN:
                        movimentoYNave = 10

                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                        movimentoYNave = 0

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_s:
                        tiros.append({
                            'x': posicaoXNave + nave.get_width() // 2.3,
                            'y': posicaoYNave + nave.get_height() // 2 - tiro.get_height() // 2
                        })

        if not pausado:
            posicaoXNave += movimentoXNave
            posicaoYNave += movimentoYNave

            if posicaoXNave <= 20:
                posicaoXNave = 20
            elif posicaoXNave >= 855:
                posicaoXNave = 855

            if posicaoYNave <= 0:
                posicaoYNave = 0
            elif posicaoYNave >= 580:
                posicaoYNave = 580

            for ast in asteroides:
                ast['x'] -= velocidadeAsteroide
                if ast['x'] < -55:
                    ast['x'] = 1000
                    ast['y'] = random.randint(0, 645)
                    velocidadeAsteroide += 0.1

            for t in tiros[:]:
                t['x'] += velocidadeTiro
                if t['x'] > tela[0]:
                    tiros.remove(t)

            decorativo_pos[0] += decorativo_vel[0]
            decorativo_pos[1] += decorativo_vel[1]

            if decorativo_pos[0] < decorativo_raio or decorativo_pos[0] > tela[0] - decorativo_raio:
                decorativo_vel[0] *= -1
                decorativo_pos[0] = max(decorativo_raio, min(tela[0] - decorativo_raio, decorativo_pos[0]))
            if decorativo_pos[1] < decorativo_raio or decorativo_pos[1] > tela[1] - decorativo_raio:
                decorativo_vel[1] *= -1
                decorativo_pos[1] = max(decorativo_raio, min(tela[1] - decorativo_raio, decorativo_pos[1]))

        nave_rect = pygame.Rect(
            posicaoXNave + 8,
            posicaoYNave + 12,
            nave.get_width() - 16,
            nave.get_height() - 20
        )

        for ast in asteroides:
            asteroide_rect = pygame.Rect(
                ast['x'] + 8,
                ast['y'] + 8,
                escalaAsteroide.get_width() - 16,
                escalaAsteroide.get_height() - 16
            )
            if nave_rect.colliderect(asteroide_rect):
                voltar_inicio = tela_morte(pontuacao, nome_jogador)
                if voltar_inicio:
                    jogando = False  
                else:
                    pygame.quit()
                    exit()
                break 

        for t in tiros[:]:
            tiro_rect = pygame.Rect(
                t['x'],
                t['y'],
                tiro.get_width(),
                tiro.get_height()
            )
            for ast in asteroides:
                asteroide_rect = pygame.Rect(
                    ast['x'] + 8,
                    ast['y'] + 8,
                    escalaAsteroide.get_width() - 16,
                    escalaAsteroide.get_height() - 16
                )
                if tiro_rect.colliderect(asteroide_rect):
                    tiros.remove(t)
                    ast['x'] = 1000
                    ast['y'] = random.randint(0, 675)
                    pontuacao += 1
                    threading.Thread(target=speak, args=(f"{pontuacao} pontos",)).start()
                    break 

        telaPrincipal.blit(fundoJogo, (-120, 10))
        telaPrincipal.blit(nave, (posicaoXNave, posicaoYNave))

        pygame.draw.circle(
            telaPrincipal,
            (255, 255, 0),
            sol_pos,
            int(sol_raio)
        )
        sol_raio += sol_pulse_direcao * sol_pulse_vel
        if sol_raio > sol_raio_base + 10:
            sol_pulse_direcao = -1
        elif sol_raio < sol_raio_base - 10:
            sol_pulse_direcao = 1

        pygame.draw.circle(
            telaPrincipal,
            decorativo_cor,
            (int(decorativo_pos[0]), int(decorativo_pos[1])),
            decorativo_raio
        )

        for t in tiros:
            telaPrincipal.blit(tiro, (t['x'], t['y']))

        pontuacao_texto = fontePontuacao.render(f"{nome_jogador} - Pontos: {pontuacao}", True, branco)
        telaPrincipal.blit(pontuacao_texto, (10, 40))

        for ast in asteroides:
            telaPrincipal.blit(escalaAsteroide, (ast['x'], ast['y']))

        hora_atual = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        texto_hora = fonteHora.render(hora_atual, True, branco)
        telaPrincipal.blit(texto_hora, (10, 10))

        fontePause = pygame.font.Font(None, 18)
        texto_pause = fontePause.render("Press Space to Pause Game.", True, branco)
        telaPrincipal.blit(texto_pause, (10 + texto_hora.get_width() + 10, 12))

        if pausado:
            s = pygame.Surface(tela, pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            telaPrincipal.blit(s, (0, 0))

            fonte = pygame.font.Font(None, 74)
            fonte2 = pygame.font.Font(None, 40)

            texto = fonte.render("PAUSE", True, (255, 0, 0))
            texto2 = fonte2.render("Pressione espaço para retomar", True, branco)

            texto_rect = texto.get_rect(center=(tela[0] // 2, tela[1] // 2 - 30))
            texto2_rect = texto2.get_rect(center=(tela[0] // 2, tela[1] // 2 + 30))

            telaPrincipal.blit(texto, texto_rect)
            telaPrincipal.blit(texto2, texto2_rect)

        pygame.display.update()
        relogio.tick(60)
