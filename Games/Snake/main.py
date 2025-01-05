# making snake game in python


import pygame as pg
from sys import exit
from random import randint

GAME_SIZE = (600, 600)
FPS = 3
TILE_SIZE = 30


class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(GAME_SIZE)
		pg.display.set_caption("Snake")
		self.clock = pg.time.Clock()
		self.velocity = [1, 0]
		self.velo_dict = {pg.K_a : [-1, 0], pg.K_d : [1, 0], pg.K_w : [0, -1], pg.K_s : [0, 1]}
		self.opp_key = {pg.K_a : pg.K_d, pg.K_w : pg.K_s, pg.K_s : pg.K_w, pg.K_d : pg.K_a}
		self.player_snake = [[2, 0], [1, 0], [0, 0]]
		self.apple_pos = list()
		self.font = pg.font.Font('Fonts/knight_warrior.otf', 40)
		self.restart_font = pg.font.Font('Fonts/knight_warrior.otf', 60)
		self.score = 0
		self.running = True
		self.run()

	def get_usr_input(self):
		keys = pg.key.get_pressed()
		for velo in self.velo_dict:
			if keys[velo]:
				if self.velocity != self.velo_dict[self.opp_key[velo]]:
					self.velocity = self.velo_dict[velo]

	def get_apple_pos(self):
		temp = []
		while True:
			temp = [randint(0, GAME_SIZE[0] // TILE_SIZE), randint(0, GAME_SIZE[1] // TILE_SIZE)]
			if temp not in self.player_snake: break
		self.apple_pos = temp

	def draw_player(self):
		for block in self.player_snake:
			if self.player_snake.index(block) == 0:
				pg.draw.rect(self.screen, '#0ca69b', (block[0] * TILE_SIZE, block[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
				continue
			pg.draw.rect(self.screen, '#0b6b85', (block[0] * TILE_SIZE, block[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

	def decorate_bg(self):
		colors = ['#45ba1a', '#2b850b']
		for x in range(GAME_SIZE[0] // TILE_SIZE):
			for y in range(GAME_SIZE[1] // TILE_SIZE):
				index = (x + y) % 2
				pg.draw.rect(self.screen, colors[index], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

	def draw_apple(self):
		pg.draw.rect(self.screen, 'red', (self.apple_pos[0] * TILE_SIZE, self.apple_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

	def check_game_over(self):
		head = self.player_snake[0]
		if head[0] < 0 or head[1] < 0:
			return True
		if head[0] * TILE_SIZE > GAME_SIZE[0] or head[1] * TILE_SIZE > GAME_SIZE[1]:
			return True
		return False

	def move_player(self):
		if self.check_game_over(): 
			self.running = False
			return

		new_head = [self.player_snake[0][0] + self.velocity[0], self.player_snake[0][1] + self.velocity[1]]
		self.player_snake.insert(0, new_head)

		if new_head == self.apple_pos:
			self.apple_pos = []
			self.score += 1
		elif new_head in self.player_snake[1:]:
			self.running = False
		else:
			self.player_snake.pop()

	def reset(self):
		self.velocity = [1, 0]
		self.player_snake = [[2, 0], [1, 0], [0, 0]]
		self.apple_pos = []
		self.score = 0

	def restart_screen(self):
		msg = self.restart_font.render('Press Space To Continue', False, 'purple')		
		msg_rect = msg.get_rect(midtop = (GAME_SIZE[0] // 2, 20))
		self.screen.blit(msg, msg_rect)

	def display_score(self):
		msg = self.font.render(f'Score : {self.score}', False, 'purple')
		msg_rect = msg.get_rect(midbottom = (GAME_SIZE[0] // 2, GAME_SIZE[1]))
		self.screen.blit(msg, msg_rect)

	def run(self):
		while True:

			self.screen.fill('black')

			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()
				if not self.running:
					if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
						self.running = True
						self.reset()

			if self.running:
				if not self.apple_pos: self.get_apple_pos()
				self.decorate_bg()
				self.get_usr_input()
				self.draw_player()
				self.draw_apple()
				self.move_player()
			else:
				self.restart_screen()

			self.display_score()

			pg.display.update()
			self.clock.tick(FPS)


if __name__ == '__main__':
	Game()