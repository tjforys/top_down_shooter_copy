from typing import List

import pygame

from objects.log import Log


class QOL:
    @staticmethod
    def delete_logs_after_they_expire(logs: List[Log]) -> List[Log]:
        return list(filter(lambda log: log.show_until_game_time_in_ms > pygame.time.get_ticks(), logs))
