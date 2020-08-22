from Objects.GameObject import GameObject


class MovableObject(GameObject):
    def __init__(self, position_x, position_y, speed):
        super().__init__(position_x, position_y)
        self.speed = speed

    def update_position(self, x_move, y_move):
        self.position["x"] = x_move
        self.position["y"] = y_move
