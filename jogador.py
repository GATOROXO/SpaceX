import pygame
from pygame.locals import *
from bullets import bullet
import os  # Manipulador de arquivos

# Classe que representa o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Verifique o caminho correto para a imagem
        image_path = os.path.join(os.path.dirname(__file__), 'spacecraft.png')
        self.surf = pygame.image.load(image_path).convert_alpha()  # Carrega a imagem da nave
        self.surf = pygame.transform.scale(self.surf, (15, 50))  # Redimensiona a imagem da nave
        self.surf = pygame.transform.rotate(self.surf, -90)  # Rotaciona a imagem 90 graus à direita
        self.rect = self.surf.get_rect(center=(400, 300))  # Inicializa no centro da tela
        self.speed = 5

    # Atualiza a posição do jogador conforme as teclas pressionadas
    def update(self, pressed_keys, bullets):
        if pressed_keys[K_LSHIFT]:  # Aumenta a velocidade ao pressionar Shift
            self.speed = 10
        else:
            self.speed = 5

        if pressed_keys[K_SPACE]:  # Cria um novo missil quando pressionada a barra espaço
            bullets.add(bullet(self))
        
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        
        # Limites laterais (sem wrap-around)
        if self.rect.left < 0:  # Não permitir sair pela esquerda
            self.rect.left = 0
        elif self.rect.right > 800:  # Não permitir sair pela direita
            self.rect.right = 800
        
        # Permitir wrap-around nas bordas superior e inferior
        if self.rect.top > 600:  # Sai pela parte inferior
            self.rect.bottom = 0  # Coloca na parte superior
        elif self.rect.bottom < 0:  # Sai pela parte superior
            self.rect.top = 600  # Coloca na parte inferior
