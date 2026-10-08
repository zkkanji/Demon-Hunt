import pygame
import src.game as game
from .enemy_base import Enemy
from src.utils.progressbar import ProgressBar
from src.entities.projectile import AnimatedProjectile
from src.utils.sprite_utils import get_sprite_bounds, make_shadow

class Devil3(Enemy):

    def __init__(self):
        self.color = (67, 64, 64)
        pass