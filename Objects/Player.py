from Objects.MovableObject import MovableObject
from Objects.Bullet import Bullet
from Objects.Wall import Wall
from math import atan2, pi
from pygame import *


class Player(MovableObject):
    def __init__(self):
        super().__init__(2000, 2000, 6)
        self.wall_cooldown = time.get_ticks()/1000-7
        self.move_direction = {K_w: False,
                               K_s: False,
                               K_a: False,
                               K_d: False}

    def shoot(self, aim_x_position, aim_y_position):
        if aim_y_position != 0 and aim_x_position != 0:
            bullet = Bullet(self.position["x"], self.position["y"], aim_x_position, aim_y_position)
            return bullet
        else:
            return None

    def set_wall(self, x_position, y_position):
        if time.get_ticks()/1000 - self.wall_cooldown > 7:
            self.wall_cooldown = time.get_ticks()/1000
            rotation = atan2(-y_position, x_position)*180/pi
            return Wall(self.position["x"], self.position["y"], rotation)
        return None

    def move(self):
        x_move = 0
        y_move = 0
        if self.move_direction[K_w] is True and self.move_direction[K_s] is False:
            y_move = -self.speed
        elif self.move_direction[K_w] is False and self.move_direction[K_s] is True:
            y_move = self.speed
        if self.move_direction[K_a] is True and self.move_direction[K_d] is False:
            x_move = -self.speed
        elif self.move_direction[K_a] is False and self.move_direction[K_d] is True:
            x_move = self.speed
        new_position_x = self.position["x"] + x_move
        new_position_y = self.position["y"] + y_move
        if (new_position_x-2000)**2+(new_position_y-2000)**2 <= 1810**2:
            self.update_position(new_position_x, new_position_y)
