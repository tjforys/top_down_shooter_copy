import math
from typing import List
import pygame
import random
from classes.file_paths import FilePaths
from constants import Constants
from objects.bullet import Bullet
from objects.music import Music
from objects.player import Player
import time
from user_options import UserOptions


class Enemy:
    def __init__(self, pos_x: int, pos_y: int, speed: float, max_hp: int, hitbox_x: float, hitbox_y: float,  music_list: List[Music], musicCD: float):
        self.x = pos_x
        self.y = pos_y
        self.speed = speed
        self.max_hp = max_hp
        self.health = max_hp
        self.hitbox_x = hitbox_x
        self.hitbox_y = hitbox_y
        self.music_list = music_list
        self.last_music_time = 0
        self.musicCD = musicCD
        self.rect = pygame.Rect(self.x - self.hitbox_x/2, self.y - self.hitbox_y/2, self.hitbox_x, self.hitbox_y)
        self.last_movement_time_in_miliseconds = 0


    def move(self, player_x: int, player_y: int):
        if pygame.time.get_ticks() - Constants.time_between_movement_in_miliseconds > self.last_movement_time_in_miliseconds:
            whole_distance = math.dist((self.x, self.y), (player_x, player_y))
            if whole_distance == 0:
                whole_distance = 1
            distance_x = player_x - self.x
            distance_y = player_y - self.y

            speed_x = self.speed*distance_x/whole_distance
            speed_y = self.speed*distance_y/whole_distance

            self.x += speed_x
            self.y += speed_y
            self.rect = pygame.Rect(self.x - self.hitbox_x/2, self.y - self.hitbox_y/2, self.hitbox_x, self.hitbox_y)
            self.last_movement_time_in_miliseconds = pygame.time.get_ticks()


    def is_hit(self, bullet: Bullet):
        return self.rect.colliderect(bullet.rect)
    

    def play_random_sound(self):
        if time.time() - self.last_music_time > self.musicCD:
            random.choice(self.music_list).play()
            self.last_music_time = time.time()


    def take_damage(self, amount: float):
        self.health -= amount
        if self.health < 1:
            if UserOptions.game_sounds:
                Music(FilePaths.mp3_enemy_death, volume=0.3).play()


class BasicEnemy(Enemy):
    def __init__(self, pos_x, pos_y):
        sprite = pygame.image.load(FilePaths.png_enemy_sprite).convert_alpha()
        image_proportions = sprite.get_height()/sprite.get_width()
        super().__init__(
            max_hp=10,
            pos_x=pos_x,
            pos_y=pos_y,
            speed=0.5,
            hitbox_x=30,
            hitbox_y=30*image_proportions,
            music_list=[Music(target_file=FilePaths.mp3_enemy, volume=0.05)],
            musicCD=5
        )
        enemy = pygame.transform.scale(sprite, (self.hitbox_x, self.hitbox_y))
        self.sprite = enemy



class Goku(Enemy):
    def __init__(self, pos_x, pos_y):
        sprite = pygame.image.load(FilePaths.png_goku).convert_alpha()
        image_proportions = sprite.get_height()/sprite.get_width()       
        super().__init__(
            max_hp=5,
            pos_x=pos_x,
            pos_y=pos_y,
            speed=1,
            hitbox_x=40,
            hitbox_y=40*image_proportions,
            music_list=[Music(target_file=FilePaths.mp3_goku1, volume=0.2), Music(target_file=FilePaths.mp3_goku2, volume=0.2), Music(FilePaths.mp3_goku3, volume=0.2)],
            musicCD=5
        )
        goku = pygame.transform.scale(sprite, (self.hitbox_x, self.hitbox_y))
        self.sprite = goku


class Pasterz(Enemy):
    def __init__(self, pos_x, pos_y):
        sprite = pygame.image.load(FilePaths.png_shooter).convert_alpha()
        image_proportions = sprite.get_height()/sprite.get_width()       
        super().__init__(
            max_hp=7,
            pos_x=pos_x,
            pos_y=pos_y,
            speed=0.3,
            hitbox_x=40,
            hitbox_y=40*image_proportions,
            music_list=[Music(target_file=FilePaths.mp3_black_impostor, volume=0.05)],
            musicCD=5
        )
        self.shoot_dist = 150
        self.shoot_cd = 3
        self.shoot_time = 0
        self.in_range = False
        pasterz = pygame.transform.scale(sprite, (self.hitbox_x, self.hitbox_y))
        self.sprite = pasterz

    def move(self, player_x: int, player_y: int):
        if pygame.time.get_ticks() - Constants.time_between_movement_in_miliseconds > self.last_movement_time_in_miliseconds:
            whole_distance = math.dist((self.x, self.y), (player_x, player_y))
            if whole_distance == 0:
                whole_distance = 1
            distance_x = player_x - self.x
            distance_y = player_y - self.y

            speed_x = self.speed*distance_x/whole_distance
            speed_y = self.speed*distance_y/whole_distance
            if whole_distance > self.shoot_dist:
                self.x += speed_x
                self.y += speed_y
                self.in_range = False
            else:
                self.in_range = True

            self.rect = pygame.Rect(self.x - self.hitbox_x/2, self.y - self.hitbox_y/2, self.hitbox_x, self.hitbox_y)
            self.last_movement_time_in_miliseconds = pygame.time.get_ticks()

    def shoot(self, player: Player, enemy_bullet_list: List[Bullet]):
        if self.in_range and time.time() - self.shoot_time > self.shoot_cd:
            enemy_bullet_list.append(Bullet(self.x, self.y, player.x, player.y, speed=0.5, radius=10))
            self.shoot_time = time.time()
        return enemy_bullet_list


class Michael(Enemy):
    def __init__(self, pos_x, pos_y):
        sprite = pygame.image.load(FilePaths.png_michael).convert_alpha()
        image_proportions = sprite.get_height() / sprite.get_width()
        super().__init__(
            max_hp=3,
            pos_x=pos_x,
            pos_y=pos_y,
            speed=0.8,
            hitbox_x=40,
            hitbox_y=40 * image_proportions,
            music_list=[Music(target_file=FilePaths.mp3_michael, volume=0.2)],
            musicCD=5
        )
        michael = pygame.transform.scale(sprite, (self.hitbox_x, self.hitbox_y))
        self.sprite = michael
        self.was_seen = False
        