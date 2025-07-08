from typing import List

import pygame

from classes.file_paths import FilePaths
from objects.bullet import Bullet
from objects.enemy import Enemy, BasicEnemy, Goku, Pasterz, Michael
from objects.player import Player
import time
import random

from utils.movement_utils import Movement


class EnemyUtils:
    @classmethod
    def handle_enemies(cls, screen, enemies: List[Enemy], player: Player, bullets: List[Bullet]):
        for enemy in enemies:
            cls.move_enemy(enemy, player)
            cls.deal_dmg_to_enemy(enemy, bullets)

            if isinstance(enemy, Michael):
                if not enemy.was_seen and Movement.is_inside_arena(screen.x, screen.y, enemy.x, enemy.y):
                    enemy.music_list[0].play()
                    enemy.was_seen = True
        enemies_alive = len(enemies)
        enemies = cls.delete_dead_enemies(enemies)
        player.kill_counter += (enemies_alive - len(enemies))
        return enemies


    @staticmethod
    def manage_enemy_collision(screen, player: Player, enemies: List[Enemy]):
        for enemy in [enemy for enemy in enemies if isinstance(enemy, Michael)]:
            if player.rect.colliderect(enemy.rect):
                player.take_damage(3)
                sprite = pygame.image.load(FilePaths.png_explosion).convert_alpha()
                sprite = pygame.transform.scale(sprite, (250, 150))
                screen.screen.blit(sprite, (player.x-player.hitbox_x/2-100, player.y-player.hitbox_y/2-80))
                pygame.display.flip()
                time.sleep(0.5)
                enemies.remove(enemy)

        if player.rect.collideobjects([enemy.rect for enemy in enemies]):
            player.take_damage(1)

        return enemies



    @staticmethod
    def deal_dmg_to_enemy(enemy: Enemy, bullets: List[Bullet]) -> Enemy:
        for bullet in reversed(bullets):
            if enemy.is_hit(bullet):
                enemy.take_damage(bullet.damage)
        return enemy


    @staticmethod
    def move_enemy(enemy: Enemy, player: Player) -> Enemy:
        return enemy.move(player.x, player.y)


    @staticmethod
    def delete_dead_enemies(enemies: List[Enemy]) -> List[Enemy]:
        return list(filter(lambda e: e.health > 0, enemies))


    @staticmethod
    def generate_enemies(enemy_spawn_cd: float, enemy_spawn_location_list: List[tuple], enemy_spawn_time: float, enemies: List[Enemy]):
        if time.time() - enemy_spawn_time > enemy_spawn_cd:
            spawn_coords = random.choice(enemy_spawn_location_list)
            enemy_type = random.randint(1, 4)
            if enemy_type == 1:
                enemies.append(BasicEnemy(spawn_coords[0], spawn_coords[1]))
            if enemy_type == 2:
                enemies.append(Goku(spawn_coords[0], spawn_coords[1]))
            if enemy_type == 3:
                enemies.append(Pasterz(spawn_coords[0], spawn_coords[1]))
            if enemy_type == 4:
                enemies.append(Michael(spawn_coords[0], spawn_coords[1]))
            enemy_spawn_time = time.time()
        return enemy_spawn_time, enemies
    
    @staticmethod
    def play_enemy_sounds(enemies: List[Enemy]):
        for enemy in enemies:
            if isinstance(enemy, Michael):
                continue
            enemy.play_random_sound()


    @staticmethod
    def shoot_bullets(enemies: List[Enemy], enemy_bullets: List[Bullet], player: Player):
        for enemy in enemies:
            if isinstance(enemy, Pasterz):
                enemy_bullets = enemy.shoot(player, enemy_bullets)
        return enemy_bullets
