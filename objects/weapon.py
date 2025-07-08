from enum import Enum

import pygame

from objects.bullet import Bullet
from classes.file_paths import FilePaths
import time
import random

from objects.music import Music
from user_options import UserOptions


class ShootType(Enum):
    MANUAL = 0
    AUTOMATIC = 1


class Weapon:
    def __init__(self, bullet_damage: float, bullet_speed: float, shoot_cd: float, shot_amount: int, max_magazine: int, reload_time: float, spread: int, bullet_size: int, shot_speed_spread: float, shoot_type: ShootType, sfx: Music):
        self.bullet_damage = bullet_damage
        self.bullet_speed = bullet_speed
        self.shoot_cd = shoot_cd
        self.shot_amount = shot_amount
        self.max_magazine = max_magazine
        self.current_magazine = max_magazine
        self.reload_time = reload_time
        self.reloading = False
        self.reload_start_time = 0
        self.spread = spread
        self.bullet_size = bullet_size
        self.last_shot_time = 0
        self.shot_speed_spread = shot_speed_spread
        self.shoot_type = shoot_type
        self.sfx = sfx


    def can_weapon_shoot(self) -> bool:
        if self.reloading:
            self.has_reload_ended()

        if time.time() - self.last_shot_time > self.shoot_cd and not self.reloading:
            if self.current_magazine == 0:
                self.start_reload()
                return False
            return True


    def shoot(self, pos_x, pos_y, bullet_list):
        if UserOptions.game_sounds:
            self.sfx.play()

        dest_x, dest_y = pygame.mouse.get_pos()
        for i in range(self.shot_amount):
            bullet_list.append(Bullet(pos_x=pos_x,
                                      pos_y=pos_y,
                                      dest_x=dest_x + random.randint(-self.spread, self.spread),
                                      dest_y=dest_y + random.randint(-self.spread, self.spread),
                                      speed=self.bullet_speed + random.uniform(-self.shot_speed_spread, self.shot_speed_spread),
                                      radius=self.bullet_size,
                                      damage=self.bullet_damage))
        self.current_magazine -= 1
        self.last_shot_time = time.time()
        return bullet_list

    def start_reload(self):
        if not self.reloading:
            self.reload_start_time = time.time()
            self.reloading = True
            if UserOptions.game_sounds:
                Music(FilePaths.mp3_reload, volume=0.3).play()


    def has_reload_ended(self):
        if self.reloading and time.time() - self.reload_start_time > self.reload_time:
            self.current_magazine = self.max_magazine
            self.reloading = False


class Glock(Weapon):
    def __init__(self):
        super().__init__(bullet_damage=1, bullet_speed=2.5, shoot_cd=0, shot_amount=1, max_magazine=10, reload_time=1.5, spread=0, bullet_size=7, shot_speed_spread=0, shoot_type=ShootType.MANUAL,
                         sfx=Music(target_file=FilePaths.mp3_glock, volume=0.05, loop=False))


class Shotgun(Weapon):
    def __init__(self):
        super().__init__(bullet_damage=1, bullet_speed=1.5, shoot_cd=0.5, shot_amount=3, max_magazine=3, reload_time=3, spread=40, bullet_size=10, shot_speed_spread=0.2, shoot_type=ShootType.MANUAL,
                         sfx=Music(target_file=FilePaths.mp3_shotgun, volume=0.05, loop=False))


class AR15(Weapon):
    def __init__(self):
        super().__init__(bullet_damage=1, bullet_speed=3, shoot_cd=0.1, shot_amount=1, max_magazine=30, reload_time=2, spread=0, bullet_size=8, shot_speed_spread=0, shoot_type=ShootType.AUTOMATIC,
                         sfx=Music(target_file=FilePaths.mp3_AR15, volume=0.05, loop=False))
