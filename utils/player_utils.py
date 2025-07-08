from objects.player import Player
from objects.bullet import Bullet
from typing import List


class PlayerUtils:
    @staticmethod
    def manage_enemy_bullets_collistion(player: Player, enemy_bullets: List[Bullet]):
        if player.rect.collideobjects([bullet.rect for bullet in enemy_bullets]):
            player.take_damage(1)
        return list(filter(lambda b: not b.rect.colliderect(player.rect), enemy_bullets))
