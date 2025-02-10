# # Tetris

import pygame as pg
from sys import exit
from settings import *
from random import randint, choice
import os

if os.name != "nt":
	os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Game:

	def __init__(self):
		pg.init()
		pg.display.set_caption("Tetris")
		self.screen = pg.display.set_mode((GAME_SIZE[0] + SCORE_WIDTH, GAME_SIZE[1]))
		self.clock = pg.time.Clock()
		self.running = True
		self.bricks = BRICKS
		self.brick = list()
		self.bricks_on_floor = list()
		self.score = 0
		self.high_score = 0
		self.font = pg.font.Font('Fonts\\knight_warrior.otf', 50) if os.name == "nt" else pg.font.Font('Fonts//knight_warrior.otf', 50)
		self.fall_speed = BRICK_FALLING_SPEED
		self.run()

	def draw_grid(self):
		for x in range(GAME_SIZE[0] // COL_SIZE):
			color = list(GRID_COLOR)
			for y in range(GAME_SIZE[1] // COL_SIZE):
				pg.draw.rect(self.screen, tuple(color), (x * COL_SIZE, y * COL_SIZE, COL_SIZE, COL_SIZE), width = GRID_WIDTH)
				# color = [max(0, val + int(255 / (GAME_SIZE[1] / COL_SIZE))) for val in color] # for black and white grid
				color = [min(255, val + randint(1, 30)) for val in color] # for raindbow grid (I prefer this one)

	def get_brick(self):
		brick = choice(list(self.bricks.values()))
		index = randint(0, len(brick) - 1)
		color = choice(BRICK_COLORS)
		y = -COL_SIZE
		x = COL_SIZE * ((GAME_SIZE[0] / COL_SIZE) // 2)
		for i in range(0, GAME_SIZE[0] // COL_SIZE):
			outside_bd = False
			for val in brick[index](x, y):
				if val[0] < 0 or val[0] > GAME_SIZE[0]:
					outside_bd = True
				if outside_bd: break
			if outside_bd:
				outside_bd = False
			else: break
			x += COL_SIZE
		return {'brick' : brick, 'index' : index, 'pos' : [x, y], 'color' : color}

	def draw_brick(self, brick):
		positions = brick['brick'][brick['index']](brick['pos'][0], brick['pos'][1])
		for pos in positions:
			pg.draw.rect(self.screen, brick['color'], (pos[0], pos[1], COL_SIZE, COL_SIZE), BRICK_WIDTH, BRICK_STYLE)

	def move_brick(self):
		brick = self.brick[0]
		self.brick.clear()
		temp_pos = brick['pos']
		pos = [temp_pos[0], temp_pos[1] + COL_SIZE]
		brick['pos'] = pos
		self.brick.append(brick)

	def check_brick_floor_contact(self):
		if not self.brick: return
		brick = self.brick[0]
		positions = brick['brick'][brick['index']](brick['pos'][0], brick['pos'][1])
		for pos in positions:
			if pos[1] + COL_SIZE == GAME_SIZE[1]:
				for pos in positions:
					self.bricks_on_floor.append((pos[0], pos[1], brick['color']))
				self.brick.clear()

	def brick_contact(self):
		if not self.brick: return
		brick = self.brick[0]
		positions = brick['brick'][brick['index']](brick['pos'][0], brick['pos'][1])
		occupied_pos = list()
		for brick_ in self.bricks_on_floor:
			occupied_pos.append((brick_[0], brick_[1]))
		for pos in positions:
			if (pos[0], pos[1] + COL_SIZE) in occupied_pos:
				self.detect_over()
				for pos in positions:
					self.bricks_on_floor.append((pos[0], pos[1], brick['color']))
				self.brick.clear()

	def draw_fallen_bricks(self):
		for brick in self.bricks_on_floor:
			pg.draw.rect(self.screen, brick[2], (brick[0], brick[1], COL_SIZE, COL_SIZE), BRICK_WIDTH, BRICK_STYLE)

	def check_valid_movement(self, brick, delta):
		positions = brick['brick'][brick['index']](brick['pos'][0], brick['pos'][1])
		for pos in positions:
			if not (pos[0] + delta >= 0 and pos[0] + delta <= GAME_SIZE[0]):
				return False
		return True

	def check_brick_line(self):
		occupied_pos = list()
		for brick in self.bricks_on_floor:
			occupied_pos.append((brick[0], brick[1]))
		for y in range(GAME_SIZE[1] // COL_SIZE):
			seen_space = False
			for x in range(GAME_SIZE[0] // COL_SIZE):
				if (x * COL_SIZE, y * COL_SIZE) not in occupied_pos:
					seen_space = True
					break
			if not seen_space:
				self.del_line(y * COL_SIZE)

	def display_score_details(self):
		high_score_surf = self.font.render(f'High Score : {self.high_score}', False, FONT_COLOR)
		score_surf = self.font.render(f'Your Score : {self.score}', False, FONT_COLOR)
		if self.running:
			high_score_rect = high_score_surf.get_rect(midtop = (GAME_SIZE[0] + (SCORE_WIDTH // 2), GAME_SIZE[1] // 4))
			score_rect = high_score_surf.get_rect(midtop = (GAME_SIZE[0] + (SCORE_WIDTH // 2), GAME_SIZE[1] - (GAME_SIZE[1] // 4)))
		else:
			high_score_rect = high_score_surf.get_rect(midtop = ((GAME_SIZE[0] + SCORE_WIDTH) // 2, GAME_SIZE[1] // 4))
			score_rect = high_score_surf.get_rect(midtop = ((GAME_SIZE[0] + SCORE_WIDTH) // 2, GAME_SIZE[1] - (GAME_SIZE[1] // 4)))
			msg_surf = self.font.render(f'Press Space To Continute', False, FONT_COLOR)
			msg_rect = msg_surf.get_rect(midtop = ((GAME_SIZE[0] + SCORE_WIDTH) / 2, GAME_SIZE[1] - (GAME_SIZE[1] / 2)))
			self.screen.blit(msg_surf, msg_rect)
		self.screen.blit(high_score_surf, high_score_rect)
		self.screen.blit(score_surf, score_rect)

	def del_line(self, line_y):
		self.score += 100
		self.bricks_on_floor = [(x, y, color) for x, y, color in self.bricks_on_floor if y != line_y]
		self.bricks_on_floor = [(x, y + COL_SIZE, color) if y < line_y else (x, y, color) for x, y, color in self.bricks_on_floor]
		
	def get_usr_input(self):
		brick = self.brick[0]
		index = brick['index']
		pos = brick['pos']
		keys = pg.key.get_pressed()
		if keys[pg.K_UP] or keys[pg.K_w]:
			if index + 1 > len(brick['brick']) - 1:
				index = 0
			else: index += 1
		if keys[pg.K_DOWN] or keys[pg.K_s]:
			if index - 1 < 0:
				index = len(brick['brick']) - 1
			else: index -= 1
		if keys[pg.K_LEFT] or keys[pg.K_a]:
			if self.check_valid_movement(brick, - COL_SIZE):
				pos = [pos[0] - COL_SIZE, pos[1]]
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			if self.check_valid_movement(brick, COL_SIZE):
				pos = [pos[0] + COL_SIZE, pos[1]]

		self.brick.clear()
		brick['index'] = index
		brick['pos'] = pos
		self.brick.append(brick)

	def detect_over(self):
		if not self.brick: return
		brick = self.brick[0]
		pos = brick['pos']
		positions = brick['brick'][brick['index']](pos[0], pos[1])
		for pos_ in positions:
			if pos_[1] <= 0:
				self.running = False

	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()
				if self.running and self.brick:
					if event.type == pg.KEYDOWN:
						brick = self.brick[0]
						index = brick['index']
						pos = brick['pos']
						if event.key == pg.K_UP or event.key == pg.K_w:
							if index + 1 > len(brick['brick']) - 1:
								index = 0
							else: index += 1
						if event.key == pg.K_DOWN or event.key == pg.K_s:
							if index - 1 < 0:
								index = len(brick['brick']) - 1
							else: index -= 1
						if event.key == pg.K_LEFT or event.key == pg.K_a:
							if self.check_valid_movement(brick, - COL_SIZE):
								pos = [pos[0] - COL_SIZE, pos[1]]
						if event.key == pg.K_RIGHT or event.key == pg.K_d:
							if self.check_valid_movement(brick, COL_SIZE):
								pos = [pos[0] + COL_SIZE, pos[1]]

						self.brick.clear()
						brick['index'] = index
						brick['pos'] = pos
						self.brick.append(brick)
				else:
					if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
						self.running = True
						self.high_score = max(self.score, self.high_score)
						self.brick.clear()
						self.bricks_on_floor.clear()
						self.score = 0

			self.screen.fill('black')

			if self.running:
				if not self.brick:
					self.brick.append(self.get_brick())
				self.draw_grid()
				self.move_brick()
				self.get_usr_input()
				self.brick_contact()
				self.check_brick_floor_contact()
				_ = self.draw_brick(self.brick[0]) if self.brick else None
				self.draw_fallen_bricks()
				self.check_brick_line()
			self.display_score_details()

			self.clock.tick(FPS)
			pg.display.flip()


if __name__ == '__main__':
	Game()


