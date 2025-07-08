from typing import List

from objects.bullet import Bullet
from objects.enemy import Enemy
from objects.screen import Screen


class BulletUtils:
    @classmethod
    def handle_bullets(cls, screen: Screen, bullets: List[Bullet]):
        bullets = cls.filter_out_of_bounds_bullets(screen, bullets)

        for bullet in bullets:
            bullet.move()

        return bullets


    @staticmethod
    def filter_out_of_bounds_bullets(screen: Screen, bullets: List[Bullet]) -> List[Bullet]:
        return list(filter(lambda b: b.is_in_bounds(screen.x, screen.y), bullets))


    @staticmethod
    def get_hit_bullets(bullets: List[Bullet], enemies: List[Enemy]) -> List[Bullet]:
        return list(filter(lambda b: any([enemy_obj.is_hit(b) for enemy_obj in enemies]), bullets))


    @staticmethod
    def delete_hit_bullets(bullets: List[Bullet], hit_bullets: List[Bullet]):
        for hit_bullet in hit_bullets:
            bullets.remove(hit_bullet)
        return bullets
