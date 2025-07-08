import pygame
import time
from classes.direction_enums import Directions
from classes.file_paths import FilePaths
from constants import Constants
from utils.movement_utils import Movement


class Player:
    def __init__(self, x: int, y: int, radius: int, speed: float, hitbox_x: int, hitbox_y, max_hp: int):
        self.rotation = Directions.RIGHT
        self.x = x
        self.y = y
        self.hitbox_x = hitbox_x
        self.hitbox_y = hitbox_y
        self.radius = radius
        self.max_hp = max_hp
        self.health = max_hp
        self._speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.hitbox_x, self.hitbox_y)
        self.i_frame_time = 0
        self.i_frames = 1
        self.alive = True
        self.last_movement_time_in_miliseconds = 0
        self.kill_counter = 0

        player = pygame.image.load(FilePaths.png_player).convert_alpha()
        player = pygame.transform.scale(player, (self.hitbox_x, self.hitbox_y))
        self.sprite = player

    
    def move(self, area_x, area_y):
        if pygame.time.get_ticks() - Constants.time_between_movement_in_miliseconds > self.last_movement_time_in_miliseconds:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.x -= self._speed
                self.rotation = Directions.LEFT

            if keys[pygame.K_w]:
                self.y -= self._speed

            if keys[pygame.K_s]:
                self.y += self._speed

            if keys[pygame.K_d]:
                self.x += self._speed
                self.rotation = Directions.RIGHT

            self.x, self.y = Movement.put_back_in_arena_if_outside(area_x, area_y, self.x, self.y)
            self.rect = pygame.Rect(self.x - self.hitbox_x/2, self.y - self.hitbox_y/2, self.hitbox_x, self.hitbox_y)
            self.last_movement_time_in_miliseconds = pygame.time.get_ticks()


    def dash(self, dash_distance, area_x, area_y):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= dash_distance
        if keys[pygame.K_w]:
            self.y -= dash_distance
        if keys[pygame.K_d]:
            self.x += dash_distance
        if keys[pygame.K_s]:
            self.y += dash_distance

        self.x, self.y = Movement.put_back_in_arena_if_outside(area_x, area_y, self.x, self.y)

    def take_damage(self, amount: float = 1):
        if time.time() - self.i_frame_time > self.i_frames:
            self.health -= amount
            self.i_frame_time = time.time()
            