# settings for playformer trial 3

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

COL_SIZE = 60
SCREEN_SIZE = (len(TILE_MAP[0]) * COL_SIZE, len(TILE_MAP) * COL_SIZE)
FPS = 30
TILE_WIDTH = 1
PLAYER_SPEED = (COL_SIZE // FPS) * 4
PLAYER_ACC = 1
PLAYER_MAX_ACC = 2 * COL_SIZE
PLAYER_JUMP_VAL = 13
