from math import sin, cos, pi
from pygame import *


class Screen:
    def __init__(self):
        self.player_image = image.load("../Sources/player.png")
        self.wall_image = image.load("../Sources/wall.png")
        self.bullet_image = image.load("../Sources/bullet.png")
        self.background_image = image.load("../Sources/background.png")
        self.screen = display.set_mode(size=(0, 0), flags=FULLSCREEN)
        display.set_caption("Shoters")
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.scale = self.width/1000
        self.player_width = self.player_height = self.scale*50
        self.wall_width = self.player_width*33/40
        self.wall_height = self.player_width*1.5
        self.bullet_width = self.bullet_height = self.scale * 10
        self.background_width = self.background_height = 4000*self.scale
        self.player_image = transform.scale(self.player_image, (int(self.player_width), int(self.player_height)))
        self.wall_image = transform.scale(self.wall_image, (int(self.wall_width), int(self.wall_height)))
        self.bullet_image = transform.scale(self.bullet_image, (int(self.bullet_width), int(self.bullet_height)))
        self.background_image = transform.scale(self.background_image,
                                                (int(self.background_width), int(self.background_height)))

    def update(self, *args):
        background_shift_x = -args[0]["x"]*self.scale+self.width/2
        background_shift_y = -args[0]["y"]*self.scale+self.height/2
        self.screen.blit(self.background_image, (background_shift_x, background_shift_y))
        for bullet in args[1]:
            self.screen.blit(self.bullet_image,
                             (bullet["x"]*self.scale+background_shift_x-self.bullet_width/2,
                              bullet["y"]*self.scale+background_shift_y-self.bullet_height/2))
        for wall in args[2]:
            radians_rotation = wall["rotation"]/180*pi
            actual_wall = transform.rotate(self.wall_image, wall["rotation"])
            self.screen.blit(actual_wall,
                             (wall["x"]*self.scale+background_shift_x-actual_wall.get_width()/2
                              + self.player_width*cos(radians_rotation),
                              wall["y"]*self.scale+background_shift_y-actual_wall.get_height()/2
                              - self.player_width*sin(radians_rotation)))
        self.screen.blit(self.player_image,
                         ((self.width - self.player_width) / 2, (self.height - self.player_width) / 2))
        for player in args[3]:
            self.screen.blit(self.player_image,
                             (player["x"]*self.scale+background_shift_x-self.player_width/2,
                              player["y"]*self.scale+background_shift_y-self.player_height/2))
        display.update()
