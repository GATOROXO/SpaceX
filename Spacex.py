"""
UFMT - Universidade Federal de Mato Grosso
Bacharelado em ciencia da computacao
Professor: Ivairton M. Santos
Alunos: Gabriel Pivetta Loss e João Paulo
"""

# Biblioteca PyGame
import pygame
from pygame.locals import *
from bullets import bullet
from asteroides import Enemy
from jogador import Player

# Inicializa pygame
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define os eventos para criação de inimigos e mísseis
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)  # Intervalo de criação de inimigos

# Cria o jogador
player = Player()

# Define o plano de fundo (cor branca)
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

# Grupos de sprites
missil = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                new_missil = bullet(player)
                missil.add(new_missil)
                all_sprites.add(new_missil)
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:  # Criação de um inimigo
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    screen.blit(background, (0, 0)) 

    # Atualiza o jogador e os inimigos 
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, bullet)
    enemies.update()

    # Atualiza mísseis e verifica colisões com inimigos
    missil.update()
    for missile in missil:
        enemy_hit = pygame.sprite.spritecollideany(missile, enemies, collided=lambda m, e: m.hitbox.colliderect(e.rect))
        if enemy_hit:
            missile.kill()  # Remove o míssil ao atingir um inimigo
            enemy_hit.kill()  # Remove o inimigo atingido

    # Verifica colisão do jogador com inimigos
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False  # Encerra o jogo se o jogador for atingido

    # Renderiza todos os sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
    clock.tick(60)
