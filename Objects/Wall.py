from Objects.GameObject import GameObject
from math import sqrt, sin, cos, pi


class Wall(GameObject):
    def __init__(self, position_x, position_y, rotation):
        super().__init__(position_x, position_y)
        self.rotation = rotation
        self.time = 0
        self.time_to_live = 5

    def time_up(self, time):
        self.time += time
        if self.time >= self.time_to_live:
            return True
        return False

    def block(self, colliding_object):
        width = abs(cos(self.rotation / 180 * pi) * 40) + abs(sin(self.rotation / 180 * pi) * 75)
        height = abs(cos(self.rotation / 180 * pi) * 75) + abs(sin(self.rotation / 180 * pi) * 40)
        if cos(self.rotation / 180 * pi) >= 0:
            if self.position["x"] + width + 30 * cos(self.rotation / 180 * pi) - width / 2 * \
                    sin(abs(self.rotation / 180 * pi)) < colliding_object.position["x"] or \
                    colliding_object.position["x"] < self.position["x"] + 30 * cos(self.rotation / 180 * pi) - width / \
                    2 * sin(abs(self.rotation / 180 * pi)):
                return False
        else:
            if self.position["x"] - width + 30 * cos(self.rotation / 180 * pi) + width / 2 * \
                    sin(abs(self.rotation / 180 * pi)) > colliding_object.position["x"] or \
                    colliding_object.position["x"] > self.position["x"] + 30 * cos(self.rotation / 180 * pi) + width / \
                    2 * sin(abs(self.rotation / 180 * pi)):
                return False
        if self.rotation >= 0:
            if self.position["y"] - 30 * sin(abs(self.rotation / 180 * pi)) + height / 2 * \
                    abs(cos(self.rotation / 180 * pi)) < colliding_object.position["y"] or \
                    colliding_object.position["y"] < self.position["y"] - height - 30 * \
                    sin(abs(self.rotation / 180 * pi)) + height / 2 * abs(cos(self.rotation / 180 * pi)):
                return False
        else:
            if self.position["y"] + 30 * sin(abs(self.rotation / 180 * pi)) - height / 2 * \
                    abs(cos(self.rotation / 180 * pi)) > colliding_object.position["y"] or \
                    colliding_object.position["y"] > self.position["y"] + height + 30 * \
                    sin(abs(self.rotation / 180 * pi)) - height / 2 * abs(cos(self.rotation / 180 * pi)):
                return False
        x_vector = self.position["x"] + 28 * cos(self.rotation / 180 * pi) - colliding_object.position["x"]
        y_vector = self.position["y"] - 28 * sin(self.rotation / 180 * pi) - colliding_object.position["y"]
        distance = sqrt(x_vector ** 2 + y_vector ** 2)
        if 43 >= distance >= 33:
            return True
        return False
