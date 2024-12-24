# settings

import pygame as pg
from sys import exit


TILE_MAP = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
[0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0,],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1,],
[1, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1,],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
]

TILE_SIZE = 60
SCREEN_SIZE =  (len(TILE_MAP[0]) * TILE_SIZE, len(TILE_MAP) * TILE_SIZE)
FPS = 60
TILE_WIDTH = 1
PLAYER_SPEED = (TILE_SIZE // FPS) * 4
PLAYER_ACC = 1
PLAYER_MAX_ACC = 2 * TILE_SIZE
PLAYER_JUMP_VAL = 13
