from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import pygame
import data.constants as c
from data.particles import KunaiProjectile

class Skill(ABC):
    """Base class for all skills"""
    
    def __init__(self, player, cooldown: float = 0.0, chakra_cost: int = 0):
        self.player = player
        self.cooldown = cooldown
        self.chakra_cost = chakra_cost
        self.current_cooldown = 0.0
        self.is_active = False
        self.duration = 0.0
        self.active_timer = 0.0
        self.skill_type = None  
        
        
    def can_use(self, chakra) -> bool:
        """Check if skill can be used"""
        return (self.current_cooldown <= 0 and 
                chakra >= self.chakra_cost and
                not self.is_active)
    
    def use(self, dt: float) -> bool:
        """Attempt to use the skill"""
        if not self.can_use(self.player.chakra):
            return False
            
        self.player.chakra -= self.chakra_cost
        self.current_cooldown = self.cooldown
        self.is_active = True
        self.active_timer = self.duration
        
        self._on_activate(dt)
        return True
    
    def update(self, dt: float):
        """Update skill state"""
        if self.current_cooldown > 0:
            self.current_cooldown -= dt
            print(self.current_cooldown)
            
        if self.is_active and self.duration > 0:
            self.active_timer -= dt
            if self.active_timer <= 0:
                self._on_deactivate(dt)
                self.is_active = False
            else:
                self._on_active_update(dt)
    
    @abstractmethod
    def _on_activate(self, dt: float):
        """Called when skill is activated"""
        pass
    
    def _on_active_update(self, dt: float):
        """Called while skill is active (optional)"""
        pass
    

    def _on_deactivate(self, dt: float):
        """Called when skill deactivates (optional)"""
        pass
    
    def get_cooldown_percentage(self) -> float:
        """Get cooldown as percentage (0.0 to 1.0)"""
        if self.cooldown <= 0:
            return 0.0
        return max(0.0, self.current_cooldown / self.cooldown)

class NinjaTime(Skill):
    """Slow down time for the player"""
    
    def __init__(self, player):
        super().__init__(player, cooldown=10.0, chakra_cost=30)
        self.duration = 5.0
        self.time_scale = 0.5
        
    def _on_activate(self, dt: float):
        # Slow down time globally by modifying the game state
        # This will affect all players and enemies
        if hasattr(self.player, 'game_state'):
            self.player.game_state.time_slow_multiplier = self.time_scale
            self.player.game_state.time_slow_timer = 0
        
    def _on_deactivate(self, dt: float):
        # Restore normal time
        if hasattr(self.player, 'game_state'):
            self.player.game_state.time_slow_multiplier = 1.0
            self.player.game_state.time_slow_timer = 0

    def update(self, dt: float):
        if self.is_active and self.player.chakra > 10 * dt:
            self.player.chakra -= 10 * dt
        else:
            self.is_active = False


class Dash(Skill):
    """Quick dash in movement direction"""
    
    def __init__(self, player):
        super().__init__(player, cooldown=2.0, chakra_cost=15)
        self.dash_speed = 350  # Pixels per second
        self.duration = 0.2
        self.skill_type = "movement"
        self.original_x_vel = 0
        self.original_y_vel = 0
        
    def _on_activate(self, dt: float):
        # Store original velocity
        self.original_x_vel = self.player.x_vel
        self.original_y_vel = self.player.y_vel
        self.player.move_locked = True
        # Get movement direction and apply dash
        intent = self.player.input_handler.get_inputs()
        dx = intent.get(c.Actions.MOVE_X, 0)
        dy = 0#intent.get(c.Actions.MOVE_Y, 0)
        
        # Default to right direction if no movement input
        if abs(dx) < 0.1 and abs(dy) < 0.1:
            dx = 1  # Default to right
            dy = 0
        
        # Apply dash velocity
        self.player.x_vel = dt * self.dash_speed
        #self.player.y_vel = dy * self.dash_speed
        
        
    def _on_deactivate(self, dt: float):
        # Restore original velocity
        self.player.x_vel = 0
        self.player.y_vel = 0
        self.player.move_locked = False

    def _on_active_update(self, dt: float):
        self.player.x_vel = self.dash_speed * dt
        self.player.y_vel = 0

class Teleport(Skill):
    """Teleport in movement direction"""
    
    def __init__(self, player):
        super().__init__(player, cooldown=5.0, chakra_cost=25)
        self.teleport_distance = 200
        
    def _on_activate(self, dt: float):
        intent = self.player.input_handler.get_inputs()
        dx = intent.get(c.Actions.MOVE_X, 0)
        dy = intent.get(c.Actions.MOVE_Y, 0)
        
        if abs(dx) > 0.1 or abs(dy) > 0.1:
            # Calculate teleport position
            teleport_x = self.player.pos_x + (dx * self.teleport_distance)
            teleport_y = self.player.pos_y + (dy * self.teleport_distance)
            
            # Clamp to screen bounds
            teleport_x = max(0, min(teleport_x, c.SCREEN_WIDTH - self.player.rect.width))
            teleport_y = max(0, min(teleport_y, c.SCREEN_HEIGHT - self.player.rect.height))
            
            self.player.move(teleport_x, teleport_y) 

class KunaiThrow(Skill):
    """Throw a kunai"""
    def __init__(self, player):
        super().__init__(player, cooldown=1.0, chakra_cost=5)
        self.kunai_speed = 600

    def _on_activate(self, dt: float):
        # Get direction from input
        intent = self.player.input_handler.get_inputs()
        dx = intent.get(c.Actions.MOVE_X, 0)
        dy = intent.get(c.Actions.MOVE_Y, 0)

        # Default to right direction if no input
        if abs(dx) < 0.1 and abs(dy) < 0.1:
            dx = 1  # Default to right
            dy = 0

        # Normalize direction
        mag = (dx ** 2 + dy ** 2) ** 0.5
        if mag == 0:
            dx, dy = 1, 0  # Default right
        else:
            dx /= mag
            dy /= mag

        # Create kunai projectile
        kunai = KunaiProjectile(
            x=self.player.pos_x + self.player.rect.width // 2,
            y=self.player.pos_y + self.player.rect.height // 2,
            vx=dx * self.kunai_speed,
            vy=dy * self.kunai_speed
        )
        # Add to player's projectile group or global group
        if hasattr(self.player, "projectile_group"):
            self.player.projectile_group.add(kunai)
        elif hasattr(self.player, "particle_group"):
            self.player.particle_group.add(kunai)
        else:
            # Fallback: try to add to a global group if available
            pass