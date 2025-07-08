import os
from typing import List

import pygame
from pygame import Surface


class BackgroundGIF:
    def __init__(self, gif_frames_folder: str, draw_frequency_in_ms: int, res_x: int, res_y: int):
        self.frames_list: List[Surface] = []
        self.draw_frequency_in_ms: int = draw_frequency_in_ms
        self.current_frame: int = 0
        self.last_draw_time_in_ms: int = 0

        for gif_frame in os.listdir(gif_frames_folder):
            cat = pygame.image.load(f"{gif_frames_folder}\{gif_frame}").convert()
            self.frames_list.append(pygame.transform.scale(cat, (res_x, res_y)))
