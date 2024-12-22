# Making a simple platformer game logic in pygame python

import pygame as pg
from sys import exit


COL_SIZE = 50
SCREEN_SIZE = (500, 500)

TILE_MAP = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        pg.display.set_caption("Platformer Trial")
        self.running = True
        self.clock = pg.time.Clock()
        self.player = Player(self.screen, (200, 200), (20, 40))
        self.map = Map(self.screen)
        self.collision = Collision()
        self.run()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()

            self.screen.fill('black')

            self.map.make_map()
            self.player.update()

            # collision
            if self.collision.check_collision(self.player, self.map): 
                self.player.fall = False
            else: 
                self.player.fall = True

            # camera
            if self.player.shift_camera():
                if self.player.direction_x[0] or self.player.direction_x[1]:
                    if self.player.direction_x[0]:
                        self.map.shift(5, 0)
                    else:
                        self.map.shift(-5, 0)
                else:
                    if self.player.direction_y[0]:
                        self.map.shift(0, 5)
                    else:
                        self.map.shift(0, -5)

            # print(self.player.get_player_pos())

            pg.display.flip()
            self.clock.tick(60)


class Player:

    def __init__(self, screen, pos, dimensions):
        self.screen = screen
        self.pos = list(pos)
        self.dimen = dimensions
        self.velocity = 1
        self.fall = True
        self.player = pg.Surface((20, 40))
        self.player_rect = self.player.get_rect()
        self.player_rect.x = pos[0]
        self.player_rect.y = pos[1]
        self.direction_x = [0, 0]
        self.direction_y = [0, 1]

    def update(self):
        self.get_input()
        self.apply_gravity()
        self.draw()

    def move(self, delta):
        self.player_rect.x += delta

    def get_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            if not self.shift_camera(): self.move(-5)
            self.direction_x = [1, 0]
        elif keys[pg.K_RIGHT]:
            if not self.shift_camera(): self.move(5)
            self.direction_x = [0, 1]
        else:
            self.direction_x = [0, 0]
        if keys[pg.K_SPACE]:
            self.fall = True
            self.velocity = -10
            self.direction_y = [1, 0]

    def draw(self):
        self.screen.blit(self.player, self.player_rect)
        pg.draw.rect(self.screen, 'red', self.player_rect)

    def apply_gravity(self):
        if self.fall: self.velocity = min(10, self.velocity + 1)
        else:
            self.direction_y = [0, 0]
            self.velocity = 0
        if not self.shift_camera():
            self.player_rect.y += self.velocity

    def get_player_pos(self):
        return (self.player_rect.x // COL_SIZE, self.player_rect.y // COL_SIZE)

    def shift_camera(self):
        if self.player_rect.left <= 100 and self.direction_x[0]:
            return True
        if self.player_rect.right >= SCREEN_SIZE[1] - 100 and self.direction_x[1]:
            return True
        if self.player_rect.top <= 100 and self.direction_y[0]:
            return True
        if self.player_rect.bottom <= 100 and self.direction_y[1]:
            return True
        return False


class Map:

    def __init__(self, screen):
        self.screen = screen
        self.tiles = []
        self.load_tiles()

    def load_tiles(self):
        for row_index, row in enumerate(TILE_MAP):
            for col_index, col in enumerate(row):
                if col:
                    self.tiles.append(pg.Rect(col_index * COL_SIZE, row_index * COL_SIZE, COL_SIZE, COL_SIZE))

    def make_map(self):
        for tile in self.tiles:
            pg.draw.rect(self.screen, 'gray', tile)

    def shift(self, delta_x, delta_y):
        for tile in self.tiles:
            tile.x += delta_x
            tile.y += delta_y


class Collision:

    def __init__(self):
        pass

    def check_collision(self, player, map):
        player_ = player.player_rect
        for tile in map.tiles:
            if player_.colliderect(tile):
                return True
        return False


if __name__ == "__main__":
    Game()