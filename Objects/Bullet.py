from Objects.MovableObject import MovableObject
from math import sqrt


class Bullet(MovableObject):
    def __init__(self, position_x, position_y, direction_x, direction_y):
        super().__init__(position_x, position_y, 5)
        scale = self.speed/sqrt(direction_x*direction_x + direction_y*direction_y)
        self.direction = {"x": direction_x*scale, "y": direction_y*scale}
        self.owner = None

    def move(self):
        super().update_position(self.position["x"]+self.direction["x"], self.position["y"]+self.direction["y"])

    def defeat_opponent(self, opponent):
        if self.owner != opponent:
            return True
        return False

    def set_owner(self, owner):
        self.owner = owner
