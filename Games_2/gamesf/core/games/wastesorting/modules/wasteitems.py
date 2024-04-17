
import pygame
import random

class Waste(pygame.sprite.Sprite):
    def __init__(self, images_dict, selected_key, screensize):
        pygame.sprite.Sprite.__init__(self)
        self.selected_key=selected_key
        self.screensize = screensize
        self.image = images_dict[selected_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = random.randint(20, screensize[0]-20), -10
        self.speed = random.randrange(6, 10)
    def update(self):
        self.rect.bottom += self.speed
        if self.rect.top > self.screensize[1]:
            return True
        return False