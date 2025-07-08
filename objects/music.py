import pygame


class Music:
    def __init__(self, target_file: str, volume: float = 0.1, loop: bool = False):
        self._target_file = target_file
        self.volume = volume
        self._loop = -1 if loop else 0
        pygame.mixer.init()
        pygame.mixer.set_num_channels(15)


    def play(self):
        music = pygame.mixer.Sound(self._target_file)
        music.set_volume(self.volume)
        music.play(self._loop)


    def set_target_file(self, new_file: str):
        self._target_file = new_file



    
