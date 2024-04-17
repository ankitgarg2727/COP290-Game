import os
import pygame
import random
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import Dustbin, Waste, ShowEndGameInterface,StartInterface,ShowEndGameInterface_two



class Config():
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    TITLE = 'Waste sorting game'
    FPS = 30
    SCREENSIZE = (800, 600)
    BACKGROUND_COLOR = (0, 160, 233)
    HIGHEST_SCORE_RECORD_FILEPATH = os.path.join(rootdir, 'highest.rec')
    IMAGE_PATHS_DICT = {
        '31': os.path.join(rootdir, 'resources/images/31.png'),
        '32': os.path.join(rootdir, 'resources/images/32.png'),
        '33': os.path.join(rootdir, 'resources/images/33.png'),
        '34': os.path.join(rootdir, 'resources/images/34.png'),
        '35': os.path.join(rootdir, 'resources/images/35.png'),
        '36': os.path.join(rootdir, 'resources/images/36.png'),
        '37': os.path.join(rootdir, 'resources/images/37.png'),
        '38': os.path.join(rootdir, 'resources/images/38.png'),
        '39': os.path.join(rootdir, 'resources/images/39.png'),
        'start': {
            'play_black': os.path.join(rootdir, 'resources/images/start/play_black.png'), 
            'play_red': os.path.join(rootdir, 'resources/images/start/play_red.png'), 
            'quit_black': os.path.join(rootdir, 'resources/images/start/quit_black.png'), 
            'quit_red': os.path.join(rootdir, 'resources/images/start/quit_red.png'), 
            'start_interface': os.path.join(rootdir, 'resources/images/start/start_interface.png'), 
        },
        'background': os.path.join(rootdir, 'resources/images/background.jpg'),
        'hazardous': [],
        'dry':[],
        'wet':[]
    }
    for i in range(1, 11):
        IMAGE_PATHS_DICT['wet'].append(os.path.join(rootdir, 'resources/images/%d.png' % i))
    for i in range(11, 21):
        IMAGE_PATHS_DICT['hazardous'].append(os.path.join(rootdir, 'resources/images/%d.png' % i))
    for i  in range(21,31):
        IMAGE_PATHS_DICT['dry'].append(os.path.join(rootdir, 'resources/images/%d.png' % i))    
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    SOUND_PATHS_DICT = {
        'get': os.path.join(rootdir, 'resources/audios/get.wav'),
    }
    FONT_PATHS_DICT = {
        'default_s': {'name': os.path.join(rootdir.replace('wastesorting', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 40},
        'default_l': {'name': os.path.join(rootdir.replace('wastesorting', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 60},
    }

class WasteSortinggame(PygameBaseGame):
    game_type = 'catchcoins'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(WasteSortinggame, self).__init__(config=self.cfg, **kwargs)
    def run(self):
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        game_images, game_sounds = resource_loader.images, resource_loader.sounds
        start_interface = StartInterface(cfg, resource_loader)
        is_play = start_interface.update(screen)
        if not is_play:
            return
        flag = True
        while flag:
            gameended=False
            start_time = pygame.time.get_ticks()
            resource_loader.playbgm()
            font = resource_loader.fonts['default_s']
            dustbin = Dustbin(game_images['wet'], position=(375, 520))
            waste_sprites_group = pygame.sprite.Group()
            generate_waste_freq = random.randint(10, 20)
            generate_waste_count = 0
            score = 0
            lives=5
            highest_score = 0 if not os.path.exists(cfg.HIGHEST_SCORE_RECORD_FILEPATH) else int(open(cfg.HIGHEST_SCORE_RECORD_FILEPATH).read())
            clock = pygame.time.Clock()
            current_left=0
            current_top=0
            while True: 
                if pygame.time.get_ticks() - start_time >= 90000:
                    break
                while True:            
                    screen.fill(0)
                    screen.blit(game_images['background'], (0, 0))
                    countdown_text = 'Count down: ' + str((90000 - (pygame.time.get_ticks()-start_time)) // 60000) + ":" + str((90000 - (pygame.time.get_ticks()-start_time)) // 1000 % 60).zfill(2)
                    countdown_text = font.render(countdown_text, True, (0, 0, 0))
                    countdown_rect = countdown_text.get_rect()
                    countdown_rect.topright = [cfg.SCREENSIZE[0]-30, 5]
                    screen.blit(countdown_text, countdown_rect)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            QuitGame()
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                        dustbin.move(cfg.SCREENSIZE, 'left')
                    if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                        dustbin.move(cfg.SCREENSIZE, 'right')
                    generate_waste_count += 1
                    if generate_waste_count > generate_waste_freq:
                        generate_waste_freq = random.randint(10, 20)
                        generate_waste_count = 0
                        waste = Waste(game_images, random.choice(['31',]*2  + ['32',]*2  + ['33',]*2 + ['34',]*10 + ['35',]*10 + ['36',]*10 + ['37',]*2 + ['38',]*2 + ['39']*2), cfg.SCREENSIZE)
                        waste_sprites_group.add(waste)
                    for waste in waste_sprites_group:
                        if waste.update(): waste_sprites_group.remove(waste)
                    for waste in waste_sprites_group:
                        if pygame.sprite.collide_mask(waste, dustbin):
                            game_sounds['get'].play()
                            waste_sprites_group.remove(waste)
                            touched=waste.selected_key
                            if touched=='34' or touched=='35' or touched=='36':
                                score+=10
                            else:
                                lives-=1
                                score-=5 
                            if score > highest_score: highest_score = score        
                    dustbin.draw(screen)
                    waste_sprites_group.draw(screen)
                    score_text = f'Score: {score}, Highest: {highest_score}, Lifesleft: {lives}'
                    score_text = font.render(score_text, True, (0, 0, 0))
                    score_rect = score_text.get_rect()
                    score_rect.topleft = [5, 5]
                    screen.blit(score_text, score_rect)
                    if(lives==0):
                        gameended=True
                        break
                    if (pygame.time.get_ticks()-start_time) % 30000 >= 10000:
                        current_left=dustbin.rect.left
                        current_top=dustbin.rect.top
                        break
                    pygame.display.flip()
                    clock.tick(cfg.FPS)
                if(gameended==True):
                    break  
                dustbin = Dustbin(game_images['dry'], position=(current_left, current_top))    
                while True:
                    screen.fill(0)
                    screen.blit(game_images['background'], (0, 0))
                    countdown_text = 'Count down: ' + str((90000 - (pygame.time.get_ticks()-start_time)) // 60000) + ":" + str((90000 - (pygame.time.get_ticks()-start_time)) // 1000 % 60).zfill(2)
                    countdown_text = font.render(countdown_text, True, (0, 0, 0))
                    countdown_rect = countdown_text.get_rect()
                    countdown_rect.topright = [cfg.SCREENSIZE[0]-30, 5]
                    screen.blit(countdown_text, countdown_rect)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            QuitGame()
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                        dustbin.move(cfg.SCREENSIZE, 'left')
                    if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                        dustbin.move(cfg.SCREENSIZE, 'right')
                    generate_waste_count += 1
                    if generate_waste_count > generate_waste_freq:
                        generate_waste_freq = random.randint(10, 20)
                        generate_waste_count = 0
                        waste = Waste(game_images, random.choice(['31',]*10 + ['32',]*10 + ['33',]*10 + ['34',]*2  + ['35',]*2  + ['36',]*2  + ['37',]*2 + ['38',]*2 + ['39']*2), cfg.SCREENSIZE)
                        waste_sprites_group.add(waste)
                    for waste in waste_sprites_group:
                        if waste.update(): waste_sprites_group.remove(waste)
                    for waste in waste_sprites_group:
                        if pygame.sprite.collide_mask(waste, dustbin):
                            game_sounds['get'].play()
                            waste_sprites_group.remove(waste)
                            touched=waste.selected_key
                            if touched=='31' or touched=='32' or touched=='33':
                                score+=10
                            else:
                                lives-=1
                                score-=5
                            if score > highest_score: highest_score = score
                    dustbin.draw(screen)
                    waste_sprites_group.draw(screen)
                    score_text = f'Score: {score}, Highest: {highest_score}, Lifesleft: {lives}'
                    score_text = font.render(score_text, True, (0, 0, 0))
                    score_rect = score_text.get_rect()
                    score_rect.topleft = [5, 5]
                    screen.blit(score_text, score_rect)
                    if(lives==0):
                        gameended=True
                        break
                    if (pygame.time.get_ticks()-start_time) % 30000 >= 20000  :
                        current_left=dustbin.rect.left
                        current_top=dustbin.rect.top
                        break
                    pygame.display.flip()
                    clock.tick(cfg.FPS) 
                if(gameended==True):
                    break       
                dustbin = Dustbin(game_images['hazardous'], position=(current_left, current_top))
                while True:
                    screen.fill(0)
                    screen.blit(game_images['background'], (0, 0))
                    countdown_text = 'Count down: ' + str((90000 - (pygame.time.get_ticks()-start_time)) // 60000) + ":" + str((90000 - (pygame.time.get_ticks()-start_time)) // 1000 % 60).zfill(2)
                    countdown_text = font.render(countdown_text, True, (0, 0, 0))
                    countdown_rect = countdown_text.get_rect()
                    countdown_rect.topright = [cfg.SCREENSIZE[0]-30, 5]
                    screen.blit(countdown_text, countdown_rect)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            QuitGame()
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                        dustbin.move(cfg.SCREENSIZE, 'left')
                    if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                        dustbin.move(cfg.SCREENSIZE, 'right')
                    generate_waste_count += 1
                    if generate_waste_count > generate_waste_freq:
                        generate_waste_freq = random.randint(10, 20)
                        generate_waste_count = 0
                        waste = Waste(game_images, random.choice(['31',]*2 + ['32',]*2 + ['33',]*2 + ['34',]*2 + ['35',]*2 + ['36',]*2 + ['37',] * 10 + ['38',] * 10+ ['39'] * 10), cfg.SCREENSIZE)
                        waste_sprites_group.add(waste)
                    for waste in waste_sprites_group:
                        if waste.update(): waste_sprites_group.remove(waste)
                    for waste in waste_sprites_group:
                        if pygame.sprite.collide_mask(waste, dustbin):
                            game_sounds['get'].play()

                            waste_sprites_group.remove(waste)
                            touched=waste.selected_key
                            if touched=='37' or touched=='38' or touched=='39':
                                score+=10
                            else:
                                lives-=1
                                score-=5
                            if score > highest_score: highest_score = score
                    dustbin.draw(screen)
                    waste_sprites_group.draw(screen)
                    score_text = f'Score: {score}, Highest: {highest_score},Lifesleft: {lives}'
                    score_text = font.render(score_text, True, (0, 0, 0))
                    score_rect = score_text.get_rect()
                    score_rect.topleft = [5, 5]
                    screen.blit(score_text, score_rect)
                    if(lives==0):
                        gameended=True
                        break
                    if (pygame.time.get_ticks()-start_time) >= 80000  and (pygame.time.get_ticks()-start_time) < 90000 :
                        pygame.display.flip()
                        clock.tick(cfg.FPS)
                        continue
                    if (pygame.time.get_ticks()-start_time) >= 50000  and (pygame.time.get_ticks()-start_time) < 60000 :
                        pygame.display.flip()
                        clock.tick(cfg.FPS)
                        continue 

                    if (pygame.time.get_ticks()-start_time) >= 30000  :
                        current_left=dustbin.rect.left
                        current_top=dustbin.rect.top
                        break
                    pygame.display.flip()
                    clock.tick(cfg.FPS) 
                if(gameended==True):
                    break    
                dustbin = Dustbin(game_images['wet'], position=(current_left, current_top))   
            fp = open(cfg.HIGHEST_SCORE_RECORD_FILEPATH, 'w')
            fp.write(str(highest_score))
            fp.close()
            if(gameended==True):
                flag=ShowEndGameInterface_two(screen, cfg, score, highest_score, resource_loader)
            else:
                flag = ShowEndGameInterface(screen, cfg, score, highest_score, resource_loader)
            

            
