import pygame
class PygameResourceLoader():
    def __init__(self, image_paths_dict=None, sound_paths_dict=None, font_paths_dict=None, bgm_path=None):
        self.bgm_path = bgm_path
        self.font_paths_dict = font_paths_dict
        self.image_paths_dict = image_paths_dict
        self.sound_paths_dict = sound_paths_dict
        self.fonts = self.fontload(font_paths_dict)
        self.images = self.defaultload(image_paths_dict, pygame.image.load)
        self.sounds = self.defaultload(sound_paths_dict, pygame.mixer.Sound)
    def defaultload(self, resources_dict, load_func):
        if resources_dict is None: return dict()
        assert isinstance(resources_dict, dict)
        resources = dict()
        for key, value in resources_dict.items():
            if isinstance(value, dict):
                resources[key] = self.defaultload(value, load_func)
            elif isinstance(value, list):
                resources[key] = list()
                for path in value: resources[key].append(load_func(path))
            else:
                resources[key] = load_func(value)
        return resources
    def fontload(self, font_paths_dict):
        if font_paths_dict is None: return dict()
        assert isinstance(font_paths_dict, dict)
        fonts = dict()
        for key, value in font_paths_dict.items():
            if not value.get('system_font', False):
                fonts[key] = pygame.font.Font(value['name'], value['size'])
            else:
                fonts[key] = pygame.font.SysFont(value['name'], value['size'])
        return fonts
    def playbgm(self):
        pygame.mixer.music.load(self.bgm_path)
        pygame.mixer.music.play(-1, 0.0)