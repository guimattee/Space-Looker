# Space Looker ☄️🚀
Sobre o Projeto
O Space Looker é um projeto acadêmico desenvolvido por Guilherme Matte Embarach (RA: 1137953). O jogo foi criado como requisito para uma disciplina, utilizando a biblioteca pygame para construir uma experiência de tiro espacial (space shooter).

Neste jogo, o jogador assume o papel do último piloto com a missão de salvar a galáxia de invasores cósmicos.

Funcionalidades
O jogo incorpora várias bibliotecas modernas para aprimorar a experiência do usuário:

* Reconhecimento de Voz: Os jogadores podem dizer seus nomes no microfone para configurar o perfil de jogador, usando a biblioteca SpeechRecognition.
* Texto para Fala (TTS): O jogo oferece feedback auditivo, como dar as boas-vindas ao jogador e anunciar a pontuação, com a tecnologia da biblioteca pyttsx3.
* Persistência de Pontuação: O jogo salva as últimas cinco sessões, incluindo nome do jogador, pontuação e data/hora da partida. Essas informações são exibidas na tela de "Game Over".
* Jogabilidade Dinâmica: A velocidade dos asteroides aumenta progressivamente à medida que o jogo avança, oferecendo um desafio crescente.
* Funcionalidade de Pausa: Os jogadores podem pausar e retomar o jogo a qualquer momento.

  
Como Jogar: 
Controles
Mover: Use as setas PARA CIMA e PARA BAIXO para navegar sua nave espacial.
Atirar: Pressione a tecla S para disparar projéteis nos asteroides.
Pausar: Pressione a barra de ESPAÇO para pausar ou retomar o jogo.
Jogabilidade
Tela Inicial: Ao iniciar o jogo, você será solicitado a inserir seu nome. Você pode digitá-lo ou pressionar o botão "Falar nome" para usar o reconhecimento de voz.
Introdução: Após definir seu nome, uma breve introdução à história e aos controles é exibida, juntamente com uma contagem regressiva de 10 segundos para o início do jogo.
Objetivo: O objetivo principal é destruir o maior número possível de asteroides para acumular pontos. Cada asteroide destruído concede um ponto.
Game Over: O jogo termina se sua nave colidir com um asteroide. A tela final exibirá sua pontuação e as pontuações das últimas cinco partidas. A partir desta tela, você pode optar por sair do jogo ou retornar à tela inicial para jogar novamente.
Dependências
Para rodar este jogo, você precisará do Python e das seguintes bibliotecas:

* pygame
* pyttsx3
* SpeechRecognition
* pickle
* datetime
* time
* threading
Elas podem ser instaladas via pip:

Bash

pip install pygame pyttsx3 SpeechRecognition
