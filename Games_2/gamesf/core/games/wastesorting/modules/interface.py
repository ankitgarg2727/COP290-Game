
import pygame
from ....utils import QuitGame


class MainInterface(pygame.sprite.Sprite):
    def __init__(self, cfg, resource_loader):
        pygame.sprite.Sprite.__init__(self)
        self.image = resource_loader.images['start']['start_interface'].convert()
        self.rect = self.image.get_rect()
        self.rect.center = cfg.SCREENSIZE[0] / 2, cfg.SCREENSIZE[1] / 2
    def update(self):
        pass
class PlayButton(pygame.sprite.Sprite):
    def __init__(self, cfg, resource_loader, position=(220, 415)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = resource_loader.images['start']['play_black'].convert()
        self.image_2 = resource_loader.images['start']['play_red'].convert()
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.center = position
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.image_2
        else:
            self.image = self.image_1
class QuitButton(pygame.sprite.Sprite):
    def __init__(self, cfg, resource_loader, position=(580, 415)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = resource_loader.images['start']['quit_black'].convert()
        self.image_2 = resource_loader.images['start']['quit_red'].convert()
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.center = position
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.image_2
        else:
            self.image = self.image_1

class StartInterface():
    def __init__(self, cfg, resource_loader):
        self.cfg = cfg
        self.main_interface = MainInterface(cfg, resource_loader)
        self.play_btn = PlayButton(cfg, resource_loader)
        self.quit_btn = QuitButton(cfg, resource_loader)
        self.components = pygame.sprite.LayeredUpdates(self.main_interface, self.play_btn, self.quit_btn)
    def update(self, screen):
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.cfg.FPS)
            self.components.update()
            self.components.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.play_btn.rect.collidepoint(mouse_pos):
                            return True
                        elif self.quit_btn.rect.collidepoint(mouse_pos):
                            return False

def ShowEndGameInterface(screen, cfg, score, highest_score, resource_loader):
    
    font_big = resource_loader.fonts['default_l']
    font_small = resource_loader.fonts['default_s']
    text_title = font_big.render(f"Time is up!", True, (255, 0, 0))
    text_title_rect = text_title.get_rect()
    text_title_rect.centerx = screen.get_rect().centerx
    text_title_rect.centery = screen.get_rect().centery - 100
    text_score = font_small.render(f"Score: {score}, Highest Score: {highest_score}", True, (255, 0, 0))
    text_score_rect = text_score.get_rect()
    text_score_rect.centerx = screen.get_rect().centerx
    text_score_rect.centery = screen.get_rect().centery - 10
    text_tip = font_small.render(f"Enter Q to quit game or Enter R to restart game", True, (255, 0, 0))
    text_tip_rect = text_tip.get_rect()
    text_tip_rect.centerx = screen.get_rect().centerx
    text_tip_rect.centery = screen.get_rect().centery + 60
    text_tip_count = 0
    text_tip_freq = 10
    text_tip_show_flag = True
  
    clock = pygame.time.Clock()
    while True:
        screen.fill(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_r:
                    return True
        screen.blit(text_title, text_title_rect)
        screen.blit(text_score, text_score_rect)
        if text_tip_show_flag:
            screen.blit(text_tip, text_tip_rect)
        text_tip_count += 1
        if text_tip_count % text_tip_freq == 0:
            text_tip_count = 0
            text_tip_show_flag = not text_tip_show_flag
        pygame.display.flip()
        clock.tick(cfg.FPS)
        
def ShowEndGameInterface_two(screen, cfg, score, highest_score, resource_loader):
    
    font_big = resource_loader.fonts['default_l']
    font_small = resource_loader.fonts['default_s']
    text_title = font_big.render(f"You have already used Five lifes", True, (255, 0, 0))
    text_title_rect = text_title.get_rect()
    text_title_rect.centerx = screen.get_rect().centerx
    text_title_rect.centery = screen.get_rect().centery - 100
    text_score = font_small.render(f"Score: {score}, Highest Score: {highest_score}", True, (255, 0, 0))
    text_score_rect = text_score.get_rect()
    text_score_rect.centerx = screen.get_rect().centerx
    text_score_rect.centery = screen.get_rect().centery - 10
    text_tip = font_small.render(f"Enter Q to quit game or Enter R to restart game", True, (255, 0, 0))
    text_tip_rect = text_tip.get_rect()
    text_tip_rect.centerx = screen.get_rect().centerx
    text_tip_rect.centery = screen.get_rect().centery + 60
    text_tip_count = 0
    text_tip_freq = 10
    text_tip_show_flag = True
  
    clock = pygame.time.Clock()
    while True:
        screen.fill(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_r:
                    return True
        screen.blit(text_title, text_title_rect)
        screen.blit(text_score, text_score_rect)
        if text_tip_show_flag:
            screen.blit(text_tip, text_tip_rect)
        text_tip_count += 1
        if text_tip_count % text_tip_freq == 0:
            text_tip_count = 0
            text_tip_show_flag = not text_tip_show_flag
        pygame.display.flip()
        clock.tick(cfg.FPS)        