import math
import pygame
from typing import List

from constants import Constants


class Bullet:
    def __init__(self, pos_x: int, pos_y: int, dest_x: int, dest_y: int, speed: float, radius: int = 40, damage: float = 1):
        self.x: int = pos_x
        self.y: int = pos_y
        self._dest_x: int = dest_x
        self._dest_y: int = dest_y
        self.radius = radius
        self._speed: list = self._get_bullet_speed(speed)
        self.rect = pygame.Rect(self.x - self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)
        self.last_movement_time_in_miliseconds = 0
        self.damage = damage
        
    def _get_bullet_speed(self, speed: float) -> List[float]:
        whole_distance = math.dist((self.x, self.y), (self._dest_x, self._dest_y))
        distance_x = self._dest_x - self.x
        distance_y = self._dest_y - self.y

        speed_x = speed*distance_x/whole_distance
        speed_y = speed*distance_y/whole_distance
        
        return [speed_x, speed_y]

    def move(self):
        if pygame.time.get_ticks() - Constants.time_between_movement_in_miliseconds > self.last_movement_time_in_miliseconds:
            self.x += self._speed[0]
            self.y += self._speed[1]
            self.rect = pygame.Rect(self.x - self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)
            self.last_movement_time_in_miliseconds = pygame.time.get_ticks()

    def is_in_bounds(self, area_x, area_y):
        return -area_x/2 < self.x < area_x+area_x/2 and -area_y / 2 < self.y < area_y + area_y / 2
    