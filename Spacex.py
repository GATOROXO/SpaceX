# Biblioteca PyGame
import pygame
from pygame.locals import *
from bullets import bullet
from asteroides import Enemy
from jogador import Player
import os
# Inicializa pygame
pygame.init()

screen_width = 800 # Largura da tela ou eixo x
screen_height = 600 # Altura da tela ou eixo y
screen = pygame.display.set_mode((screen_width, screen_height)) # Cria a tela com o tamanho definido
pygame.display.set_caption("SpaceX Alpha") # Define o nome da janela "SpaceX Alpha"
background = pygame.image.load(os.path.join(os.path.dirname(__file__), 'packground.png')).convert() #define a imagem de plano de fundo
screen.blit(background, (0, 0)) #coloca a imagem de plano de fundo na tela e define sua posiçao

pygame.display.flip()


# Define os eventos para criação de inimigos e mísseis
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)  # Intervalo de criação de inimigos

# Cria o jogador
player = Player()

# Define o plano de fundo (cor branca)
#background = pygame.Surface(screen.get_size())
#background.fill((0, 0, 0))

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
    if pygame.sprite.spritecollideany(player, enemies , collided=lambda p, e: p.hitbox.colliderect(e.rect)):
        player.kill()
        


    # Renderiza todos os sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)   

    pygame.display.flip()
    clock.tick(60)
