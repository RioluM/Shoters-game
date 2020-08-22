from Objects.Player import Player
from Client.Screen import Screen
from Network import Network
from pygame import *
import threading


class Game:
    def __init__(self):
        self.player = Player()
        self.network = Network()
        self.network.send(self.player)
        print(f"Connected")
        self.screen = Screen()
        self.data_ready = False
        self.running = True
        self.data = [[], [], []]
        self.wall_to_send = None
        self.bullet_to_send = None

    def run_game(self):
        clock = time.Clock()
        threading.Thread(target=self.data_transfer_thread, args=()).start()
        while self.running:
            while not self.data_ready:
                pass
            self.screen.update(self.player.position, self.data[0], self.data[1], self.data[2])
            self.data_ready = False
            for ev in event.get():
                if ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        self.running = False
                        self.network.send("Disconnect")
                        quit()
                    if ev.key == K_w or ev.key == K_s or ev.key == K_a or ev.key == K_d:
                        self.player.move_direction[ev.key] = True
                    if ev.key == K_SPACE:
                        x, y = mouse.get_pos()
                        x_position = x - self.screen.width / 2
                        y_position = y - self.screen.height / 2
                        wall = self.player.set_wall(x_position, y_position)
                        if wall is not None:
                            self.wall_to_send = wall
                if ev.type == KEYUP:
                    if ev.key == K_w or ev.key == K_s or ev.key == K_a or ev.key == K_d:
                        self.player.move_direction[ev.key] = False
                if ev.type == MOUSEBUTTONDOWN:
                    if ev.button == 1:
                        x_position = ev.pos[0] - self.screen.width/2
                        y_position = ev.pos[1] - self.screen.height/2
                        bullet = self.player.shoot(x_position, y_position)
                        if bullet is not None:
                            self.bullet_to_send = bullet
            self.player.move()
            clock.tick(60)

    def data_transfer_thread(self):
        while True:
            if self.bullet_to_send is not None:
                self.network.send(self.bullet_to_send)
                self.bullet_to_send = None
            if self.wall_to_send is not None:
                self.network.send(self.wall_to_send)
                self.wall_to_send = None
            if self.running:
                self.network.send(self.player.position)
                self.data = self.network.receive()
            else:
                break
            if self.data[0] == "Lost":
                self.running = False
                quit()
                break
            self.data_ready = True
