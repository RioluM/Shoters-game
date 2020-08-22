from Objects.Bullet import Bullet
from Objects.Wall import Wall
from Network import Network
from math import sqrt
from pygame import *
import threading


class Server:
    def __init__(self):
        self.players = {}
        self.bullets = []
        self.walls = []
        self.network = Network(1)

    def run_server(self):
        self.network.socket.listen()
        threading.Thread(target=self.bullets_thread).start()
        threading.Thread(target=self.walls_thread).start()
        while True:
            conn, address = self.network.socket.accept()
            threading.Thread(target=self.add_new_player, args=(conn, str(address))).start()

    def add_new_player(self, conn, address):
        new_player = self.network.receive(conn)
        self.players[address] = new_player
        number = len(self.players)
        print(f"New player nr {number}")
        self.player_thread(number, conn, address)

    def player_thread(self, player_number, conn, address):
        disconnected = False
        while not disconnected:
            msg = self.network.receive(conn)
            if address not in self.players.keys():
                self.network.send(["Lost"], conn)
                disconnected = True
            elif type(msg) is dict:
                self.players[address].update_position(msg["x"], msg["y"])
                self.sending_data(conn, address)
            elif type(msg) is Bullet:
                msg.set_owner(address)
                self.bullets.append(msg)
            elif type(msg) is Wall:
                self.walls.append(msg)
            elif msg == "Disconnect":
                disconnected = True
                self.players.pop(address)
        print(f"Player nr {player_number} disconnected")
        conn.close()

    def sending_data(self, conn, address):
        seen_players = []
        seen_bullets = []
        seen_walls = []
        for player_key in self.players.keys():
            if address != player_key and \
                    abs(self.players[address].position["x"]-self.players[player_key].position["x"]) < 550 and \
                    abs(self.players[address].position["y"]-self.players[player_key].position["y"]) < 450:
                seen_players.append(self.players[player_key].position)
        for bullet in self.bullets:
            if abs(self.players[address].position["x"]-bullet.position["x"]) < 550 and \
               abs(self.players[address].position["y"]-bullet.position["y"]) < 450:
                seen_bullets.append(bullet.position)
        for wall in self.walls:
            if abs(self.players[address].position["x"] - wall.position["x"]) < 550 and \
                    abs(self.players[address].position["y"] - wall.position["y"]) < 450:
                wall_info = wall.position
                wall_info["rotation"] = wall.rotation
                seen_walls.append(wall_info)
        self.network.send([seen_bullets, seen_walls, seen_players], conn)

    def bullets_thread(self):
        clock = time.Clock()
        while True:
            left_bullets = []
            for bullet in self.bullets:
                bullet.move()
                if (bullet.position["x"]-2000)**2+(bullet.position["y"]-2000)**2 <= 1830**2:
                    left_bullets.append(bullet)
                else:
                    continue
                player_defeated = None
                for player_k in self.players.keys():
                    player = self.players[player_k]
                    x_vector = player.position["x"]-bullet.position["x"]
                    y_vector = player.position["y"] - bullet.position["y"]
                    distance = sqrt(x_vector**2+y_vector**2)
                    if distance <= 30 and bullet.defeat_opponent(player_k):
                        left_bullets.remove(bullet)
                        player_defeated = player_k
                        break
                if player_defeated is not None:
                    self.players.pop(player_defeated)
            self.bullets = left_bullets.copy()
            clock.tick(60)

    def walls_thread(self):
        clock = time.Clock()
        prev_time = time.get_ticks()
        while True:
            left_walls = []
            for wall in self.walls:
                if not wall.time_up((time.get_ticks()-prev_time)/1000):
                    left_walls.append(wall)
                stopped_bullet = None
                for bullet in self.bullets:
                    if wall.block(bullet):
                        stopped_bullet = bullet
                        break
                if stopped_bullet is not None:
                    self.bullets.remove(stopped_bullet)
            prev_time = time.get_ticks()
            self.walls = left_walls.copy()
            clock.tick(60)


