"""
UFMT - Universidade Federal de Mato Grosso
Bacharelado em ciencia da computacao
Professor: Ivairton M. Santos
Alunos: Gabriel Pivetta Loss e João Paulo
"""
# Biblioteca PyGame
import pygame
# Modulo da biblioteca PyGame que permite o acesso as teclas utilizadas
from pygame.locals import *
# spacex.py

from bullets import bullet
from asteroides import Enemy
from jogador import Player






# Inicializa pygame
pygame.init()


screen_width = 800
screen_height = 600

# Cria a tela com resolução 800x600px
screen = pygame.display.set_mode((screen_width, screen_height))

# Cria um evento para adicao de inimigos
ADDENEMY = pygame.USEREVENT + 1
ADDMISSIL = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250) #Define um intervalo para a criacao de cada inimigo (milisegundos)

# Cria o jogador
player = Player()

# Cria missil 
missil = bullet(player) 
#bullet = bullets(player.rect.centerx, player.rect.centery)

# Define o plano de fundo, com a cor preta (RGB)
background = pygame.Surface(screen.get_size())
background.fill((255, 255, 255))

#grupo de misseis
missil = pygame.sprite.Group()

enemies = pygame.sprite.Group() #Cria o grupo de inimigos
all_sprites = pygame.sprite.Group() #Cria o grupo de todos os Sprites
all_sprites.add(player) #Adicionar o player no grupo de todos os Sprites

running = True #Flag para controle do jogo
clock = pygame.time.Clock() #Cria um relogio para controle do FPS
while running:
    #Laco para verificacao do evento que ocorreu
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: #Verifica se a tecla ESC foi pressionada
                running = False
        elif event.type == QUIT: #Verifica se a janela foi fechada
            running = False
        elif(event.type == ADDENEMY): #Verifica se e o evento de criar um inimigo
            new_enemy = Enemy() #Cria um novo inimigo
            enemies.add(new_enemy) #Adiciona o inimigo no grupo de inimigos
            all_sprites.add(new_enemy) #Adiciona o inimigo no grupo de todos os Sprites
        elif(event.type == ADDMISSIL): #Verifica se e o evento de criar um missil
            new_missil = bullet(player) #Cria um novo missil    
            missil.add(new_missil) #Adiciona o missil no grupo de misseis
            all_sprites.add(new_missil) #Adiciona o missil no grupo de todos os Sprites
    screen.blit(background, (0, 0)) #Atualiza a exibicao do plano de fundo do jogo (neste caso nao surte efeito)
    pressed_keys = pygame.key.get_pressed() #Captura as as teclas pressionadas
    player.update(pressed_keys, missil) #Atualiza a posicao do player conforme teclas usadas
    enemies.update() #Atualiza posicao dos inimigos
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect) #Atualiza a exibicao de todos os Sprites
    if missil.alive():
        enemy_hit = pygame.sprite.spritecollideany(missil, enemies)
        if enemy_hit:
            missil.kill()
            enemy_hit.kill()

    if pygame.sprite.spritecollideany(player, enemies): #Verifica se ocorreu a colisao do player com um dos inimigos
        player.kill() #Se ocorrer a colisao, encerra o player

    pygame.display.flip() #Atualiza a projecao do jogo

    #definir o FPS
    clock.tick(60)