import pygame


class Cursor:
    def __init__(self, cursor_type: str):
        cursor = pygame.image.load(cursor_type).convert_alpha()

        self.img = pygame.transform.scale(cursor, (36, 36*cursor.get_height()/cursor.get_width()))
        self.img_rect = self.img.get_rect()
