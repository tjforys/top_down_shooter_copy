import pygame


class Log:
    def __init__(self, message: str, show_duration_in_ms: int):
        self.message = message
        self.show_until_game_time_in_ms = pygame.time.get_ticks() + show_duration_in_ms
