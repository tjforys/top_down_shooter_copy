import pygame
import time

from typing import List

from objects.cursor import Cursor
from objects.log import Log
from objects.music import Music
from objects.bullet import Bullet
from objects.gif_background import BackgroundGIF
from objects.player import Player
from objects.screen import Screen
from objects.enemy import Enemy
from objects.weapon import Glock, ShootType, AR15
from objects.weapon import Shotgun

from classes.file_paths import FilePaths
from utils.bullet_utils import BulletUtils
from utils.enemy_utils import EnemyUtils
from utils.player_utils import PlayerUtils
from user_options import UserOptions
from utils.quality_of_life_utils import QOL


def main():
    running = True

    pygame.mouse.set_visible(False)
    if UserOptions.game_sounds:
        sfx = Music(target_file=FilePaths.mp3_sfx, volume=0.05, loop=False)
        bg_music = Music(target_file=FilePaths.mp3_monday, volume=0.1, loop=True)
        bg_music.play()


    screen = Screen(screen_x=800, screen_y=800)
    background_gif = BackgroundGIF(gif_frames_folder=FilePaths.gif_monday_2, draw_frequency_in_ms=75, res_x=screen.x, res_y=screen.y)
    cursor = Cursor(FilePaths.png_shotgun_cursor)
    player = Player(x=400, y=400, radius=10, speed=1, hitbox_x=40, hitbox_y=52, max_hp=10)

    weapon_counter = 0
    weapon_list = [Shotgun(), Glock(), AR15()]
    current_weapon = weapon_list[0]
    cursor_list = [Cursor(FilePaths.png_shotgun_cursor), Cursor(FilePaths.png_glock_cursor), Cursor(FilePaths.png_ar15_cursor)]

    bullets: List[Bullet] = []
    enemy_bullets: List[Bullet] = []
    enemies: List[Enemy] = []
    enemy_spawn_cd = 5
    enemy_spawn_time = 0
    enemy_spawn_location_list = [(0, 0), (1000, 1000), (1000, 1500), (1000, 500), (-500, 1000)]

    logs = []

    while running:
        game_time_in_ms = pygame.time.get_ticks()

        player.move(screen.x, screen.y)

        if current_weapon.shoot_type == ShootType.AUTOMATIC:
            if pygame.mouse.get_pressed()[0]:
                if current_weapon.can_weapon_shoot():
                    bullets = current_weapon.shoot(pos_x=player.x, pos_y=player.y, bullet_list=bullets)

        for event in pygame.event.get():
            pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_weapon.shoot_type == ShootType.MANUAL:
                    if event.button == 1:  # to left-click
                        if current_weapon.can_weapon_shoot():
                            bullets = current_weapon.shoot(pos_x=player.x, pos_y=player.y, bullet_list=bullets)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    player.dash(dash_distance=100, area_x=screen.x, area_y=screen.y)

                if event.key == pygame.K_z:
                    if UserOptions.game_sounds:
                        Music(FilePaths.mp3_change_weapon, volume=0.3).play()
                    weapon_counter += 1
                    current_weapon = weapon_list[weapon_counter % len(weapon_list)]
                    cursor = cursor_list[weapon_counter % len(cursor_list)]

                if event.key == pygame.K_r and current_weapon.reloading is False and current_weapon.current_magazine != current_weapon.max_magazine:
                    current_weapon.start_reload()

                if event.key == pygame.K_1:
                    logs.append(Log(message="Upgraded dmg", show_duration_in_ms=1000))
                    current_weapon.bullet_damage += 1

                if event.key == pygame.K_2:
                    logs.append(Log(message="Upgraded bullet size", show_duration_in_ms=4000))
                    current_weapon.bullet_size += 1

            if event.type == pygame.QUIT:
                running = False

        enemy_bullets = EnemyUtils.shoot_bullets(enemies=enemies, enemy_bullets=enemy_bullets, player=player)

        enemy_bullets = BulletUtils.handle_bullets(screen=screen, bullets=enemy_bullets)

        bullets = BulletUtils.handle_bullets(screen, bullets)
        hit_bullets = BulletUtils.get_hit_bullets(bullets=bullets, enemies=enemies)
        bullets = BulletUtils.delete_hit_bullets(bullets, hit_bullets)

        enemies = EnemyUtils.manage_enemy_collision(screen=screen, player=player, enemies=enemies)
        enemies = EnemyUtils.handle_enemies(screen=screen, enemies=enemies, bullets=hit_bullets, player=player)
        enemy_bullets = PlayerUtils.manage_enemy_bullets_collistion(player=player, enemy_bullets=enemy_bullets)
        enemy_spawn_time, enemies = EnemyUtils.generate_enemies(
            enemy_spawn_cd=enemy_spawn_cd,
            enemy_spawn_location_list=enemy_spawn_location_list,
            enemy_spawn_time=enemy_spawn_time,
            enemies=enemies)

        logs = QOL.delete_logs_after_they_expire(logs)

        # Draw a solid blue circle in the center
        if UserOptions.game_sounds:
            EnemyUtils.play_enemy_sounds(enemies=enemies)

        screen.draw_everything(player=player,
                               weapon=current_weapon,
                               enemies=enemies,
                               bullets=bullets,
                               background_gif=background_gif,
                               cursor=cursor,
                               game_time_in_ms=game_time_in_ms,
                               enemy_bullets=enemy_bullets,
                               logs=logs)
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    main()
