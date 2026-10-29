import pygame
import math
from .melee_base import MeleeBase
from src.entities.sword_sweep import SwordSweep
from src.constants import FPS
from src.utils.progressbar import ProgressBar
from src.utils.assets import lazy_scaled_frames

class Sword(MeleeBase):
    
    def __init__(self):
        super().__init__(name = "sword", damage = 20, is_automatic = False, melee_range = 170 , attack_cooldown = 300, crit_mult = 2.0)
        #melee range should be 170
        # Load sword sweep animation frames
        sweep_scale = 5.7
        self.sweep_frames = lazy_scaled_frames(
            "assets/misc/sword-sweep/sword-sweep{i}.png",
            range(1, 13),
            sweep_scale,
        )
        
        self.sweeps = pygame.sprite.Group()  # Group to manage active sweep projectiles
        
        # Create cooldown progress bar (small, above player)
        self.cooldown_bar = ProgressBar(0, 0, self.attack_cooldown, "assets/misc/player-util-bar.png", 1.6, 1.6, fill_color=(192, 192, 192))

    def attack(self, player_pos, direction):
        if not self.check_attack_ready():
            return False  # Attack blocked by cooldown
        
        # Unpack position and direction
        px, py = player_pos
        dx, dy = direction
        
        # Calculate angle from direction vector (sprite aims right at 0 radians)
        angle = math.atan2(dy, dx)
        
        # Spawn sweep at edge of attack range, not player center
        # Use 40 pixel offset in attack direction
        spawn_offset = 15
        spawn_x = px + dx * spawn_offset
        spawn_y = py + dy * spawn_offset
        
        # Calculate velocity so sweep travels melee_range distance in attack_cooldown time
        # velocity = distance / time = melee_range / (attack_cooldown ms converted to frames)
        velocity = (self.melee_range * 1000) / (self.attack_cooldown * FPS)
        
        vx = dx * velocity
        vy = dy * velocity
        
        # Create the sweep projectile with rotation angle at spawn position
        is_critical = self.roll_critical_hit()
        sweep_damage = round(self.damage * self.crit_multiplier) if is_critical else self.damage
        sweep = SwordSweep(
            spawn_x, 
            spawn_y, 
            vx, 
            vy, 
            sweep_damage,
            self.attack_cooldown, 
            self.sweep_frames, 
            angle=angle,
            is_critical=is_critical
        )
        self.sweeps.add(sweep)
        
        # Reset attack cooldown timer
        self.time_from_last_attack = pygame.time.get_ticks()
        return True  # Attack succeeded

    def update(self):
        self.sweeps.update()  # Update all active sweep projectiles