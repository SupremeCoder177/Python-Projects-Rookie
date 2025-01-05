# Making pong in python

import pygame as pg
from sys import exit
from settings import *
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((GAME_SIZE[0], GAME_SIZE[1]))
		self.running_game = True
		self.clock = pg.time.Clock()
		self.player_x = player_x
		self.player_y = player_y
		self.BALL_UP = BALL_GOING_UP
		self.BALL_DOWN = BALL_GOING_DOWN
		self.BALL_LEFT = BALL_GOING_LEFT
		self.BALL_RIGHT = BALL_GOING_RIGHT
		self.ball_x = ball_x
		self.ball_y = ball_y
		self.score = 0
		self.font = pg.font.Font('Fonts//knight_warrior.otf', 50) if os.name == 'posix' else pg.font.Font('Fonts\\knight_warrior.otf', 50)
		
		pg.display.set_caption('Pong')

		self.run()

	def decorate(self):
		pg.draw.circle(self.screen, CIRCLE_COLOR, (GAME_SIZE[0] / 2, GAME_SIZE[1] / 2), GAME_SIZE[0] / 10)
		pg.draw.circle(self.screen, DECORATION_COLOR, (GAME_SIZE[0] / 2, GAME_SIZE[1] / 2), GAME_SIZE[0] / 10, width = DECOR_WIDTH)
		pg.draw.circle(self.screen, 'white', (GAME_SIZE[0] / 2, GAME_SIZE[1] / 2), GAME_SIZE[0] / 20, width = DECOR_WIDTH)
		pg.draw.rect(self.screen, 'white', (GAME_SIZE[0] - 100, GAME_SIZE[1] / 2 - 150, 100, 300))
		pg.draw.rect(self.screen, DECORATION_COLOR, (GAME_SIZE[0] - 100, GAME_SIZE[1] / 2 - 150, 100, 300), width = DECOR_WIDTH)
		pg.draw.circle(self.screen, 'white', (0, 0), ARC_SIZE)
		pg.draw.circle(self.screen, DECORATION_COLOR, (0, 0), ARC_SIZE, width = DECOR_WIDTH // 2)
		pg.draw.circle(self.screen, 'white', (GAME_SIZE[0], 0), ARC_SIZE)
		pg.draw.circle(self.screen, DECORATION_COLOR, (GAME_SIZE[0], 0), ARC_SIZE, width = DECOR_WIDTH // 2)
		pg.draw.circle(self.screen, 'white', (0, GAME_SIZE[1]), ARC_SIZE)
		pg.draw.circle(self.screen, DECORATION_COLOR, (0, GAME_SIZE[1]), ARC_SIZE, width = DECOR_WIDTH // 2)
		pg.draw.circle(self.screen, 'white', (GAME_SIZE[0], GAME_SIZE[1]), ARC_SIZE)
		pg.draw.circle(self.screen, DECORATION_COLOR, (GAME_SIZE[0], GAME_SIZE[1]), ARC_SIZE, width = DECOR_WIDTH // 2)
		pg.draw.circle(self.screen, 'white', (GAME_SIZE[0] / 2, 0), GAME_SIZE[0] / 10)
		pg.draw.circle(self.screen, 'white', (GAME_SIZE[0] / 2, GAME_SIZE[1]), GAME_SIZE[0] / 10)
		pg.draw.circle(self.screen, DECORATION_COLOR, (GAME_SIZE[0] / 2, GAME_SIZE[1]), GAME_SIZE[0] / 10, width = DECOR_WIDTH // 2)
		pg.draw.circle(self.screen, DECORATION_COLOR, (GAME_SIZE[0] / 2, 0), GAME_SIZE[0] / 10, width = DECOR_WIDTH // 2)
		pg.draw.line(self.screen, DECORATION_COLOR, (0, 0), (GAME_SIZE[0], 0), width = DECOR_WIDTH)		
		pg.draw.line(self.screen, DECORATION_COLOR, (0, 0), (0, GAME_SIZE[1]), width = DECOR_WIDTH)		
		pg.draw.line(self.screen, DECORATION_COLOR, (GAME_SIZE[0], 0), (GAME_SIZE[0], GAME_SIZE[1]), width = DECOR_WIDTH)		
		pg.draw .line(self.screen, DECORATION_COLOR, (0, GAME_SIZE[1]), (GAME_SIZE[0], GAME_SIZE[1]), width = DECOR_WIDTH)		
		pg.draw.line(self.screen, DECORATION_COLOR, (GAME_SIZE[0] / 2, 0), (GAME_SIZE[0] / 2, GAME_SIZE[1]), width = DECOR_WIDTH)

	def draw_player(self):
		pg.draw.rect(self.screen, 'white', (self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT))
		pg.draw.rect(self.screen, PLAYER_COLOR, (self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT), width = DECOR_WIDTH)

	def get_usr_input(self):
		keys = pg.key .get_pressed()
		if keys[pg.K_UP]:
			if self.player_y > 0:
				self.player_y -= PLAYER_SPEED
		if keys[pg.K_DOWN]:
			if self.player_y + PLAYER_HEIGHT < GAME_SIZE[1]:
				self.player_y += PLAYER_SPEED

	def display_score(self):
		font_surf = self.font.render(f'Score : {self.score}', False, 'purple')
		font_rect = font_surf.get_rect(midtop = (GAME_SIZE[0] / 2, 0))
		self.screen.blit(font_surf, font_rect)

	def display_credit(self):
		self.display_score()
		msg_surf = self.font.render('Press Space To Continue', False, 'purple')
		msg_rect = msg_surf.get_rect(midtop = (GAME_SIZE[0] / 2, GAME_SIZE[1] / 2))
		self.screen.blit(msg_surf, msg_rect)

	def draw_ball(self):
		pg.draw.circle(self.screen, BALL_COLOR, (self.ball_x, self.ball_y), BALL_RADIUS)
		pg.draw.circle(self.screen, BALL_BD_COLOR, (self.ball_x, self.ball_y), BALL_RADIUS, width = BALL_BD)

	def reset(self):
		self.ball_x = ball_x
		self.ball_y = ball_y

	def move_ball(self):
		if self.BALL_UP:
			if self.ball_y > 0:
				self.ball_y -= BALL_SPEED
			else:
				self.BALL_UP = False
				self.BALL_DOWN = True
		if self.BALL_DOWN:
			if self.ball_y < GAME_SIZE[1]:
				self.ball_y += BALL_SPEED
			else:
				self.BALL_UP = True
				self.BALL_DOWN = False
		if self.BALL_LEFT:
			if self.ball_x > 0:
				self.ball_x -= BALL_SPEED
			if self.ball_x <= 0:
				self.running_game = False
		if self.BALL_RIGHT:
			if self.ball_x < GAME_SIZE[0]:
				self.ball_x += BALL_SPEED
			else:
				self.BALL_RIGHT = False
				self.BALL_LEFT = True

	def check_collision(self):
		ball_point1 = (self.ball_x - BALL_RADIUS, self.ball_y - BALL_RADIUS)
		ball_point2 = (self.ball_x - BALL_RADIUS, self.ball_y + BALL_RADIUS)
		if ball_point1[0] <= self.player_x + PLAYER_WIDTH:
			if ball_point1[1] >= self.player_y and ball_point1[1] <= self.player_y + PLAYER_HEIGHT:
				self.BALL_LEFT = False
				self.BALL_RIGHT = True
				self.score += 1
		if ball_point2[0] <= self.player_x + PLAYER_WIDTH:
			if ball_point2[1] >= self.player_y and ball_point2[1] <= self.player_y + PLAYER_HEIGHT:
				self.BALL_LEFT = False
				self.BALL_RIGHT = True
				self.score += 1

	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()
				if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
					if not self.running_game:
						self.running_game = True
						self.reset()

			self.screen.fill(GAME_BG)

			if self.running_game:
				self.decorate()	
				self.get_usr_input()
				self.move_ball()
				self.check_collision()
				self.draw_player()
				self.draw_ball()
				self.display_score()
			else:
				self.display_credit()

			self.clock.tick(FPS)
			pg.display.flip()


if __name__ == '__main__':
	Game()