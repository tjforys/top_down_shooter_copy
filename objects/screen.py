from typing import List

import pygame

from classes.colors import Color
from classes.direction_enums import Directions
from objects.bullet import Bullet
from objects.cursor import Cursor
from objects.enemy import Enemy
from objects.gif_background import BackgroundGIF
from objects.log import Log
from objects.player import Player
from objects.weapon import Weapon
from user_options import UserOptions


class Screen:
    def __init__(self, screen_x, screen_y):
        self.x = screen_x
        self.y = screen_y
        self.screen = self._initialize_screen()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    
    def _initialize_screen(self):
        return pygame.display.set_mode([self.x, self.y])
    

    def show_current_time(self, current_time_in_ms: int) -> None:
        text_surface = self.font.render(f'{current_time_in_ms/1000}s', False, Color.white)
        text_rect = text_surface.get_rect(center=(self.x/2, 15))
        self.screen.blit(text_surface, text_rect)


    def show_game_over(self):
        text_surface = self.font.render(f'GAME OVER', False, Color.white)
        text_rect = text_surface.get_rect(center=(self.x/2, self.y/2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                    exit()


    def draw_everything(self, player: Player, weapon: Weapon, bullets: List[Bullet], enemies: List[Enemy], background_gif: BackgroundGIF, game_time_in_ms: int, cursor: Cursor, enemy_bullets: List[Bullet], logs: List[Log]):
        if UserOptions.disable_brain_rot:
            self.fill_screen(Color.gray)
            self.draw_enemy_hitbox(enemies)
            self.draw_player_hitbox(player)
        else:
            self.draw_background_gif_pic(background_gif)
            self.draw_enemies(enemies)
            self.draw_player(player)
        self.draw_hp_bars(player, enemies)
        self.draw_bullets(bullets)
        self.draw_enemy_bullets(enemy_bullets=enemy_bullets)
        self.draw_cursor(cursor)
        self.show_current_time(game_time_in_ms)
        self.draw_kill_counter(player)
        self.draw_logs(logs)
        self.draw_gun_ammo(weapon)

        if player.health <= 0:
            self.show_game_over()
 
        pygame.display.flip()


    def fill_screen(self, color: tuple):
        self.screen.fill(color)


    def draw_player(self, player: Player):
        if player.rotation is Directions.RIGHT:
            self.screen.blit(player.sprite, (player.x-player.hitbox_x/2, player.y-player.hitbox_y/2))
        if player.rotation is Directions.LEFT:
            self.screen.blit(pygame.transform.flip(player.sprite, True, False), (player.x-player.hitbox_x/2, player.y-player.hitbox_y/2))


    def draw_background_gif_pic(self, gif: BackgroundGIF):
        last_draw_time_to_update = False
        game_time_in_ms = pygame.time.get_ticks()

        if game_time_in_ms - gif.last_draw_time_in_ms > gif.draw_frequency_in_ms:
            gif.current_frame += 1
            last_draw_time_to_update = True

        pic_to_draw = gif.frames_list[gif.current_frame % len(gif.frames_list)]
        self.screen.blit(pic_to_draw, (0, 0))

        if last_draw_time_to_update:
            gif.last_draw_time_in_ms = pygame.time.get_ticks()


    def draw_enemies(self, enemies: List[Enemy]):
        for enemy in enemies:
            self.screen.blit(enemy.sprite, (enemy.x - enemy.hitbox_x / 2, enemy.y - enemy.hitbox_y / 2))


    def draw_bullets(self, bullets: List[Bullet]):
        for bullet in bullets:
            pygame.draw.circle(self.screen, Color.black, (bullet.x, bullet.y), bullet.radius)


    def draw_enemy_bullets(self, enemy_bullets: List[Bullet]):
        for bullet in enemy_bullets:
            pygame.draw.circle(self.screen, Color.blue, (bullet.x, bullet.y), bullet.radius)


    def draw_cursor(self, cursor: Cursor):
        cursor.img_rect.center = pygame.mouse.get_pos()
        self.screen.blit(cursor.img, cursor.img_rect)


    def draw_player_hitbox(self, player: Player):
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(player.x - player.hitbox_x/2, player.y - player.hitbox_y/2, player.hitbox_x, player.hitbox_y))
        pygame.draw.circle(self.screen, (0, 0, 0), (player.x, player.y), 10)


    def draw_enemy_hitbox(self, enemies: List[Enemy]):
        for enemy in enemies:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(enemy.x - enemy.hitbox_x / 2, enemy.y - enemy.hitbox_y / 2, enemy.hitbox_x, enemy.hitbox_y))


    def draw_hp_bars(self, player: Player, enemies: List[Enemy]):
        self.draw_health_bar(player)
        for enemy in enemies:
            self.draw_health_bar(enemy)


    def draw_health_bar(self, entity):
        bar_width = 60
        bar_height = 5
        bar_rect = pygame.Rect(entity.x - bar_width/2, entity.y - entity.hitbox_y/2 - 10, bar_width, bar_height)
        entity_health_percent = entity.health/entity.max_hp

        if entity.health != entity.max_hp:
            pygame.draw.rect(self.screen, Color.red, bar_rect)
            pygame.draw.rect(self.screen, Color.green, (bar_rect.x, entity.y - entity.hitbox_y/2 - 10, bar_width*entity_health_percent, bar_height))


    def draw_gun_ammo(self, current_weapon: Weapon):
        for i in range(current_weapon.current_magazine):
            ammo = pygame.Rect(self.x - 20 - i*20, self.y - 50, 10, 30)
            pygame.draw.rect(self.screen, Color.black, ammo)


    def draw_kill_counter(self, player: Player):
        text_surface = self.font.render(f'kills: {player.kill_counter}', False, Color.white)
        text_rect = text_surface.get_rect(center=(self.x / 2, 45))
        self.screen.blit(text_surface, text_rect)


    def draw_logs(self, logs: List[Log]):
        y = self.y - 50
        for log in logs:
            text_surface = self.font.render(log.message, False, Color.white)
            text_rect = text_surface.get_rect(topleft=(10, y))
            self.screen.blit(text_surface, text_rect)
            y -= 30
