import pygame
import random
import math

width = 340
height = 192
fps = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

pygame.init()
game_surface = pygame.Surface((width, height))
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("p")
clock = pygame.time.Clock()

window_width = window.get_width()
window_height = window.get_height()

all_sprites = pygame.sprite.Group()
near_player = pygame.sprite.Group()
static_objs = pygame.sprite.Group()
kinematic_objs = pygame.sprite.Group()

for_scale_coefficient = width / height

def fullscreen_with_ratio():
	game_surface_local = pygame.transform.scale(game_surface, (int(window_height * for_scale_coefficient), window_height))
	new_game_width = game_surface_local.get_width()
	window.blit(game_surface_local, ((window_width / 2) - (new_game_width) / 2, 0))

def absolute_number(num): #модуль числа
	if num < 0:
		num = num * (-1)
		return(num)
	else:
		return num

def remove_insert_element(elemnt, index, list_):
	list_.remove(list_[index])
	list_.insert(index, elemnt)

	return list_

def draw_text(surf, text, size, x, y, color):
	font_name = pygame.font.match_font('arial')
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.center = (x, y)
	surf.blit(text_surface, text_rect)

class test_obj(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((14, 14))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.centery = height / 2
		self.rect.centerx = width / 2
		self.move_way_y = 2
		self.move_way_x = 2
		self.jump = False
		self.fall = False
		self.max_speedx = 3
		all_sprites.add(self)
	def update(self):
		#self.rect.x += 0.1
		keyboard = pygame.key.get_pressed()
		if keyboard[pygame.K_a]:
			self.rect.x -= 10
		if keyboard[pygame.K_d]:
			self.rect.x += 10
		if keyboard[pygame.K_s]:
			self.rect.y += 10
		if keyboard[pygame.K_w]:
			self.rect.y -= 10
	def jump_init(self):
		pass

class lvl_manager():
	def __init__(self):
		self.triggerz = []

		uo_manager.objs.append(self)

		l1 = create_lvl_matrix(lvl_width, lvl_hight)
		l1 = create_board_of_lvl_matrix(l1)
		l1 = create_plates_of_matrix(l1)

		l2 = create_lvl_matrix(lvl_width, lvl_hight)
		l2 = create_board_of_lvl_matrix(l2)
		l2 = create_plates_of_matrix(l2)

		l3 = create_lvl_matrix(lvl_width, lvl_hight)
		l3 = create_board_of_lvl_matrix(l3)
		l3 = create_plates_of_matrix(l3)

		lvl_bild(l1, block_size_var)

		global p
		p = player()
		kinematic_objs.add(p)
		#p = test_obj()

		for i in all_sprites:
			if i != p:
				i.kill()
				all_sprites.add(i)

		for i in all_sprites:
			if type(i) == spawn_point_for_lvl:
				p.rect.left = i.rect.right + 2
				p.rect.bottom = i.rect.bottom

		self.cc = camera_control(p)

		self.lvlz = [l1, l2, l3]
		self.lvl_now = 0

		for i in all_sprites:
			if type(i) == spawn_point_for_lvl or type(i) == exit_point_for_lvl:
				self.triggerz.append(i)

	def update(self):
		draw_text(game_surface, str(self.lvl_now), 20, 100, 100, (255,255,255))

		for i in self.triggerz:
			if type(i) == exit_point_for_lvl:
				if i.triggered == True:
					self.lvl_now += 1
					if self.lvl_now >= len(self.lvlz):
						global running
						running = False
					else:
						for i in all_sprites:
							i.kill()
						self.triggerz = []
						uo_manager.objs.remove(self.cc)

						print(self.lvl_now)
						lvl_bild(self.lvlz[self.lvl_now - 1], block_size_var)

						all_sprites.add(p)
						kinematic_objs.add(p)
						p.speedx = 0
						p.speedy = 0
						for i in all_sprites:
							if type(i) == spawn_point_for_lvl:
								p.rect.left = i.rect.right + 2
								p.rect.bottom = i.rect.bottom

						for i in all_sprites:
							if i != p:
								i.kill()
								all_sprites.add(i)

						self.cc = camera_control(p)

						for i in all_sprites:
							if type(i) == spawn_point_for_lvl or type(i) == exit_point_for_lvl:
								self.triggerz.append(i)

			if type(i) == spawn_point_for_lvl:
				if i.triggered == True:
					self.lvl_now -= 1
					if self.lvl_now < 0:
						self.lvl_now = 0
					else:
						for i in all_sprites:
							i.kill()
						self.triggerz = []
						uo_manager.objs.remove(self.cc)

						lvl_bild(self.lvlz[self.lvl_now - 1], block_size_var)

						all_sprites.add(p)
						kinematic_objs.add(p)
						for i in all_sprites:
							if type(i) == exit_point_for_lvl:
								p.rect.right = i.rect.left - 2
								p.rect.bottom = i.rect.bottom

						for i in all_sprites:
							if i != p:
								i.kill()
								all_sprites.add(i)

						self.cc = camera_control(p)

						for i in all_sprites:
							if type(i) == spawn_point_for_lvl or type(i) == exit_point_for_lvl:
								self.triggerz.append(i)



test_lvl = [[0,0,0,0,0,0,0,0],
			[2,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0],
			[0,0,0,0,0,1,0,0],
			[0,0,0,0,0,1,1,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[1,0,0,0,1,0,0,0],
			[1,0,0,0,1,0,0,0],
			[1,0,0,1,1,0,0,0],
			[1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

def revers_matrix(lvl_matrix):
	list_ = []
	for i in lvl_matrix:
		list_.insert(0, i)

	return list_

def create_lvl_matrix(size_x, size_y):
	lvl = []
	for i in range(size_y):
		line = []
		lvl.append(line)
		for i in range(size_x):
			line.append(0)
	return lvl

def create_board_of_lvl_matrix(lvl_matrix):
	lvl = lvl_matrix

	for i in lvl:

		if lvl.index(i) == 0:
			for x in lvl[0]:
				lvl[0][lvl[0].index(x)] = 1


		if lvl.index(i) == lvl.index(lvl[-1]):
			for x in lvl[-1]:
				lvl[-1][lvl[-1].index(x)] = 1

		if i != lvl[-1] and i != lvl[0]:
			for x in lvl[lvl.index(i)]:
				lvl[lvl.index(i)][0] = 1
				lvl[lvl.index(i)][-1] = 1


	random_number_for_spawnpoint = random.randint(4, lvl_hight - 2)
	lvl[random_number_for_spawnpoint][0] = 2

	random_number_for_exitpoint = random.randint(4, lvl_hight - 2)
	lvl[random_number_for_exitpoint][lvl_width - 1] = 4
	return lvl


def create_plates_of_matrix(lvl_matrix):
	lvl = lvl_matrix
	for i in lvl:
		for element in i:
			if element == 2:
				lvl[lvl.index(i) + 1][1] = 1
				lvl[lvl.index(i) + 1][2] = 1

			if element == 4:
				lvl[lvl.index(i) + 1][lvl_width - 2] = 1
				lvl[lvl.index(i) + 1][lvl_width - 3] = 1


	lvl = revers_matrix(lvl)


	x = -1
	y = 0

	randomx_previous_step = 1
	randomx_step = 14
	randomx = random.randint(randomx_previous_step, randomx_step)
	plate_created = False


	iterarions = math.ceil(lvl_width / randomx_step)

	for i in range(0, iterarions):
		for i in lvl:
			y += 1
			x = -1

			if randomx_previous_step + randomx_step > lvl_width - 2 and plate_created == True:
				randomx = random.randint(randomx_previous_step, lvl_width - 4)
				plate_created = False
			elif plate_created == True:
				randomx = random.randint(randomx_previous_step, randomx_previous_step + randomx_step)
				plate_created = False
			#randomx = random.randint(randomx_previous_step, randomx_previous_step + randomx_step)
			for element in i:
				x += 1
				if x == randomx and lvl_hight - 3 > y > 2 and element == 0:
					lvl[y][x] = 3
					if randomx_previous_step + randomx_step > lvl_width - 2:
						y += random.randint(4, 5)
					else:
						y += random.randint(2, 3)
					plate_created = True

		if randomx_previous_step + randomx_step < lvl_width - 4:
			randomx_previous_step += randomx_step
		y = 0

	x = -1
	y = 0

	for i in lvl:
		x = - 1
		for element in i:
			x += 1
			if element == 3:
				plate_size = random.randint(4, 6)
				for num in range(plate_size):
					if x + num > lvl_width - 2:
						pass
					else:
						if lvl[y+1][x + num] == 0 and lvl[y-1][x + num] == 0:
							lvl[y][x + num] = 1
		y += 1

	lvl = revers_matrix(lvl)

	return lvl


def lvl_bild(lvl_matrix, block_size):
	block_width = block_size
	block_height = block_size
	x = -block_width
	y = -block_height

	for line in lvl_matrix:
		x = -block_width
		y += block_height

		for element in line:
			x += block_width

			if element == 0:
				pass
			if element == 1:
				block(x, y, block_size)
			if element == 2:
				spawn_point_for_lvl(x, y, block_size)

			if element == 4:
				exit_point_for_lvl(x, y, block_size)


class spawn_point_for_lvl(pygame.sprite.Sprite): #2 in lvl_bild
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((size, size))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.triggered = False
		#p.rect.x = self.rect.x
		#p.rect.bottom = self.rect.y
		#l_manager.triggerz.append(self)
		all_sprites.add(self)
	def update(self):
		self.triggered = False
		if self.rect.colliderect(p):
			self.triggered = True


class exit_point_for_lvl(pygame.sprite.Sprite): #4 in lvl_bild
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((size, size))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.triggered = False
		#l_manager.triggerz.append(self)
		all_sprites.add(self)
	def update(self):
		self.triggered = False
		if self.rect.colliderect(p):
			self.triggered = True


class block(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((size, size))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		all_sprites.add(self)
	def update(self):
		for i in kinematic_objs:
			if i.rect.bottom >= self.rect.top and i.rect.top <= self.rect.top and self.rect.left < i.rect.left < self.rect.right or i.rect.bottom > self.rect.top and i.rect.top < self.rect.top and self.rect.left < i.rect.right < self.rect.right:
				#if i.fall == True:
				i.rect.bottom = self.rect.top - 1
				i.fall = False
				i.fall_time = 0
				i.fall_sieed = 0

			if i.rect.top <= self.rect.bottom and i.rect.bottom >= self.rect.bottom and self.rect.left < i.rect.left < self.rect.right or i.rect.top < self.rect.bottom and i.rect.bottom > self.rect.bottom and self.rect.left < i.rect.right < self.rect.right:
				#if i.jumi == True:
				i.jump_init()
				i.rect.top = self.rect.bottom + 1

			if self.rect.bottom > i.rect.top > self.rect.top and i.rect.left < self.rect.right and i.rect.right > self.rect.right:
				i.rect.left = self.rect.right
				i.fall = True
				i.jump_init()

			if self.rect.top < i.rect.bottom < self.rect.bottom and i.rect.left < self.rect.right and i.rect.right > self.rect.right:
				i.rect.left = self.rect.right
				i.fall = True
				i.jump_init()

			if self.rect.bottom > i.rect.top > self.rect.top and i.rect.right > self.rect.left and i.rect.left < self.rect.left:
				i.rect.right = self.rect.left
				i.fall = True
				i.jump_init()

			if self.rect.top < i.rect.bottom < self.rect.bottom and i.rect.right > self.rect.left and i.rect.left < self.rect.left:
				i.rect.right = self.rect.left
				i.fall = True
				i.jump_init()

"""
class player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((12, 12))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.centery = height / 2
		self.rect.centerx = width / 2

		self.fall = False
		self.fall_time = 0
		self.gravitation_var = 4
		self.fall_speed = 0

		self.cant_jump = False
		self.jump = False
		self.jump_time = 3
		self.jump_speed = 0
		self.last_jump_time = 0

		self.move_way_y = 2
		self.move_way_y__restore_timer = 0

		self.last_move_way_x_change = 0
		self.move_way_x = 2
		self.move_right = False
		self.move_left = False
		self.max_speedx = 3
		self.speedx = 0


		all_sprites.add(self)
	def update(self):
		#self.rect.x += 0.1
		keyboard = pygame.key.get_pressed()

		if keyboard[pygame.K_a] and self.fall == False:
			self.move_left = True
			#self.rect.x -= 3
		if keyboard[pygame.K_d] and self.fall == False:
			self.move_right = True
			#self.rect.x += 3

		if keyboard[pygame.K_s]:
			self.move_way_y = 1
			self.move_way_y__restore_timer = 0
		if keyboard[pygame.K_w]:
			self.move_way_y = 0
			self.move_way_y__restore_timer = 0
		if keyboard[pygame.K_s] and keyboard[pygame.K_w]:
			self.move_way_y = 2
			self.move_way_y__restore_timer = 0

		if self.move_way_y__restore_timer > 100 and self.move_way_y != 2:
			self.move_way_y = 2
			self.move_way_y__restore_timer = 0
		elif self.move_way_y != 2:
			self.move_way_y__restore_timer += 1

		if self.move_right == True and self.speedx < self.max_speedx: #and self.fall == False:
			self.speedx += 1
			if self.move_way_x == 0:
				self.move_way_x = 2
			elif self.move_way_x == 2 and self.speedx > self.max_speedx / 2:
				self.move_way_x = 1

			self.last_move_way_x_change = 0

		if self.move_left == True and self.speedx > -self.max_speedx: #and self.fall == False:
			self.speedx -= 1
			if self.move_way_x == 1:
				self.move_way_x = 2
			elif self.move_way_x == 2 and self.speedx < -self.max_speedx / 2:
				self.move_way_x = 0
			self.last_move_way_x_change = 0

		if self.last_move_way_x_change > 240:
			self.move_way_x = 2
			self.last_move_way_x_change = 0
		else:
			self.last_move_way_x_change += 1

		if self.move_left == False and self.move_right == False and self.speedx != 0 and self.jump == False:
			if self.speedx > 0:
				self.speedx -= 1
			if self.speedx < 0:
				self.speedx += 1

		if self.speedx > self.max_speedx:
			self.speedx = self.max_speedx
		if self.speedx < -self.max_speedx:
			self.speedx = -self.max_speedx


		self.rect.x += self.speedx

		self.max_speedx = 6

		if keyboard[pygame.K_z]:
			self.rect.centerx = width / 2
			self.rect.y = height / 2

		if self.jump == False:
			self.fall = True

		for i in all_sprites:
			if type(i) == block:
				if i.rect.left < self.rect.left < i.rect.right or i.rect.left < self.rect.right < i.rect.right: 

					left_fall_collide = i.rect.collidepoint(self.rect.left, self.rect.bottom + 1)
					center_fall_collide = i.rect.collidepoint(self.rect.centerx, self.rect.bottom + 1)
					right_fall_collide = i.rect.collidepoint(self.rect.right, self.rect.bottom + 1)

					left_side_collide_bottom = i.rect.collidepoint(self.rect.right + 1, self.rect.bottom)
					left_side_collide_centery = i.rect.collidepoint(self.rect.right + 1, self.rect.centery)
					left_side_collide_top = i.rect.collidepoint(self.rect.right + 1, self.rect.top)

					right_side_collide_bottom = i.rect.collidepoint(self.rect.left - 1, self.rect.bottom)
					right_side_collide_centery = i.rect.collidepoint(self.rect.left - 1, self.rect.centery)
					right_side_collide_top = i.rect.collidepoint(self.rect.left - 1, self.rect.top)

					if left_fall_collide == True and self.fall == True or right_fall_collide == True and self.fall == True or center_fall_collide == True and self.fall == True:
						self.fall = False

					if left_side_collide_top or left_side_collide_centery or left_side_collide_bottom or right_side_collide_top or right_side_collide_centery or right_side_collide_bottom:
						self.cant_jump = True
						self.jump_init()
						#print("i work")

		if self.fall == False and keyboard[pygame.K_SPACE] and self.jump == False and self.last_jump_time > 15 and self.cant_jump == False:
			self.jump = True
			self.last_jump_time = 0
		else:
			self.last_jump_time += 1


		if self.fall == True:
			if self.fall_speed + self.gravitation_var * self.fall_time < block_size_var:
				self.fall_speed = self.fall_speed + self.gravitation_var * self.fall_time
			self.fall_time += 1
			self.rect.y += self.fall_speed

		if self.jump == True and self.jump_time > 0:
			self.rect.y -= self.jump_speed
			self.jump_speed = self.jump_time
			self.jump_time -= 1

			if self.speedx > 0:
				self.speedx = self.speedx * self.jump_speed
				
			if self.speedx < 0:
				self.speedx = self.speedx * self.jump_speed
			#self.max_speedx = self.max_speedx * 2

		else:
			self.jump = False
			self.jump_time = 6
			self.jump_speed = 0

		#draw_text(window, str(self.fall), 20, 1200, 200, (255,255,255))
		#draw_text(window, str(self.cant_jump), 20, 1200, 100, (255,255,255))

		self.move_left = False
		self.move_right = False

		self.cant_jump = False """

class player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((12, 12))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		#self.rect.centery = height / 2
		#self.rect.centerx = width / 2

		#for i in all_sprites:
			#if type(i) == spawn_point_for_lvl:
			#	self.rect.bottom = i.rect.bottom - 2
			#	self.rect.left = i.rect.right + 2
			#	break

		self.fall = False
		self.fall_time = 0
		self.gravitation_var = 4
		self.fall_speed = 0


		self.jump = False
		self.last_jump_time = 0
		self.jump_power = 0

		self.move_way_y = 2
		self.move_way_y__restore_timer = 0

		self.last_move_way_x_change = 0
		self.move_way_x = 2
		self.move_right = False
		self.move_left = False
		self.max_speedx = 2
		self.speedx = 0

		all_sprites.add(self)
	def update(self):
		#self.rect.x += 0.1
		keyboard = pygame.key.get_pressed()

		if keyboard[pygame.K_a] and self.fall == False:
			self.move_left = True
			#self.rect.x -= 3
		if keyboard[pygame.K_d] and self.fall == False:
			self.move_right = True
			#self.rect.x += 3

		if keyboard[pygame.K_s]:
			self.move_way_y = 1
			self.move_way_y__restore_timer = 0
		if keyboard[pygame.K_w]:
			self.move_way_y = 0
			self.move_way_y__restore_timer = 0
		if keyboard[pygame.K_s] and keyboard[pygame.K_w]:
			self.move_way_y = 2
			self.move_way_y__restore_timer = 0

		if self.move_way_y__restore_timer > 100 and self.move_way_y != 2:
			self.move_way_y = 2
			self.move_way_y__restore_timer = 0
		elif self.move_way_y != 2:
			self.move_way_y__restore_timer += 1

		if self.move_right == True and self.speedx < self.max_speedx: #and self.fall == False:
			self.speedx += 1
			if self.move_way_x == 0:
				self.move_way_x = 2
			elif self.move_way_x == 2 and self.speedx > self.max_speedx / 2:
				self.move_way_x = 1

			self.last_move_way_x_change = 0

		if self.move_left == True and self.speedx > -self.max_speedx: #and self.fall == False:
			self.speedx -= 1
			if self.move_way_x == 1:
				self.move_way_x = 2
			elif self.move_way_x == 2 and self.speedx < -self.max_speedx / 2:
				self.move_way_x = 0
			self.last_move_way_x_change = 0

		if self.last_move_way_x_change > 240:
			self.move_way_x = 2
			self.last_move_way_x_change = 0
		else:
			self.last_move_way_x_change += 1

		if self.move_left == False and self.move_right == False and self.speedx != 0 and self.jump == False:
			if self.speedx > 0:
				self.speedx -= 1
			if self.speedx < 0:
				self.speedx += 1

		if self.speedx > self.max_speedx:
			self.speedx = self.max_speedx
		if self.speedx < -self.max_speedx:
			self.speedx = -self.max_speedx


		self.rect.x += self.speedx

		self.max_speedx = 6

		if keyboard[pygame.K_z]:
			self.rect.centerx = width / 2
			self.rect.y = height / 2

		if self.jump == False:
			self.fall = True

		for i in near_player:
			if type(i) == block:
				if i.rect.left < self.rect.left < i.rect.right or i.rect.left < self.rect.right < i.rect.right: 

					left_fall_collide = i.rect.collidepoint(self.rect.left, self.rect.bottom + 1)
					center_fall_collide = i.rect.collidepoint(self.rect.centerx, self.rect.bottom + 1)
					right_fall_collide = i.rect.collidepoint(self.rect.right, self.rect.bottom + 1)

					left_side_collide_bottom = i.rect.collidepoint(self.rect.right + 1, self.rect.bottom)
					left_side_collide_centery = i.rect.collidepoint(self.rect.right + 1, self.rect.centery)
					left_side_collide_top = i.rect.collidepoint(self.rect.right + 1, self.rect.top)

					right_side_collide_bottom = i.rect.collidepoint(self.rect.left - 1, self.rect.bottom)
					right_side_collide_centery = i.rect.collidepoint(self.rect.left - 1, self.rect.centery)
					right_side_collide_top = i.rect.collidepoint(self.rect.left - 1, self.rect.top)

					if left_fall_collide == True and self.fall == True or right_fall_collide == True and self.fall == True or center_fall_collide == True and self.fall == True:
						self.fall = False

					if left_side_collide_top or left_side_collide_centery or left_side_collide_bottom or right_side_collide_top or right_side_collide_centery or right_side_collide_bottom:
						self.jump_init()


		if self.fall == False and keyboard[pygame.K_SPACE] and self.jump == False and self.last_jump_time > 15:
			self.jump = True
			self.jump_power = 11
			self.last_jump_time = 0
		else:
			self.last_jump_time += 1


		if self.fall == True:
			if self.fall_speed + self.gravitation_var * self.fall_time < block_size_var:
				self.fall_speed = self.fall_speed + self.gravitation_var * self.fall_time
			self.fall_time += 1
			self.rect.y += self.fall_speed

		if self.jump == True and self.jump_power > 0:
			self.rect.y -= self.jump_power
			self.jump_power -= 1

			#if self.speedx > 0:
				#self.speedx = self.speedx * self.jump_speed
				
			#if self.speedx < 0:
				#self.speedx = self.speedx * self.jump_speed
			#self.max_speedx = self.max_speedx * 2

		else:
			self.jump = False

		#draw_text(window, str(self.fall), 20, 1200, 200, (255,255,255))

		self.move_left = False
		self.move_right = False




	def jump_init(self):
		self.jump = False
		self.jump_power = 11


class camera_control():
	def __init__(self, centrated_obj):
		self.gameplay_procces = False
		self.centrated_obj = centrated_obj
		self.speedx = 0
		self.speedy = 0
		self.centringx = False
		self.centringy = False
		self.is_move_way_x = False
		self.is_move_way_y = False

		self.orig_width_of_game_surface = width
		self.orig_height_of_game_surface = height

		spawn_offset_x = p.rect.centerx - width / 2
		spawn_offset_y = p.rect.centery - height / 2

		for i in all_sprites:
			i.rect.x -= spawn_offset_x
			i.rect.y -= spawn_offset_y


		uo_manager.objs.append(self)

	def update(self):
		if self.centrated_obj.rect.centerx > width / 2 + width / 6 and self.centrated_obj.move_way_x == 2:
			self.centringx = True
			self.speedx -= 1

		if self.centrated_obj.rect.centerx < width / 2 - width / 6 and self.centrated_obj.move_way_x == 2:
			self.speedx += 1
			self.centringx = True


		if self.centrated_obj.rect.centery > height - (height / 3) and self.centrated_obj.move_way_y == 2:
			self.speedy -= 1
			self.centringy = True

		if self.centrated_obj.rect.centery < height / 3 and self.centrated_obj.move_way_y == 2:
			self.speedy += 1
			self.centringy = True

		for i in all_sprites:
			i.rect.x += self.speedx
			i.rect.y += self.speedy

		#if width / 4 < self.centrated_obj.rect.centerx < width - (width / 4) and self.is_move_way_x == False:
		if self.is_move_way_x == False and self.centringx == False:
			if self.speedx > 0:
				self.speedx -= 1

			if self.speedx < 0:
				self.speedx += 1

		if self.is_move_way_y == False and self.centringy == False:
			if self.speedy > 0:
				self.speedy -= 1

			if self.speedy < 0:
				self.speedy += 1


		self.is_move_way_x = False
		self.is_move_way_y = False
		self.centringx = False
		self.centringy = False

		if self.centrated_obj.move_way_y == 0 and self.centrated_obj.rect.centery < height - (height / 3) - height / 6:
			self.speedy += 1
			self.is_move_way_y = True

		if self.centrated_obj.move_way_y == 1 and self.centrated_obj.rect.centery > height / 3 + height / 6:
			self.speedy -= 1
			self.is_move_way_y = True


		if self.centrated_obj.move_way_x == 0 and self.centrated_obj.rect.centerx < width - (width / 3):
			self.is_move_way_x = True
			self.speedx += 1
			#if self.speedx > p.speedx and self.centrated_obj.rect.centerx < width / 2:
				#self.speedx = -p.speedx

		if self.centrated_obj.move_way_x == 1 and self.centrated_obj.rect.centerx > width / 3:
			self.speedx -= 1
			#if self.speedx < p.speedx and self.centrated_obj.rect.centerx > width / 2:
				#self.speedx =  -p.speedx

			self.is_move_way_x = True
		if self.centrated_obj.move_way_x == 2:
			self.speedx += 0
			self.is_move_way_x = False

		if self.speedx > self.centrated_obj.max_speedx:
			self.speedx = self.centrated_obj.max_speedx
		if self.speedx < -self.centrated_obj.max_speedx:
			self.speedx = -self.centrated_obj.max_speedx

		if self.speedy < -10:
			self.speedy = -10
		if self.speedy > 10:
			self.speedy = 10

	def new_centreted_obj(self, obj):
		self.centrated_obj = obj


class updateble_objects():
	def __init__(self):
		self.objs = []
	def update(self):
		for i in self.objs:
			i.update()

#p = test_obj()

lvl_width = 100
lvl_hight = 60

block_size_var = 16

uo_manager = updateble_objects()

l_manager = lvl_manager()

running = True
while running:
	clock.tick(30)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

	game_surface = pygame.Surface((width, height))
	window.fill(BLACK)

	uo_manager.update()

	#all_sprites.update()
	
	for i in all_sprites:
		if absolute_number(absolute_number(i.rect.centerx) - absolute_number(p.rect.centerx)) < 400 and absolute_number(absolute_number(i.rect.centery) - absolute_number(p.rect.centery)) < 300:
			near_player.add(i)

	near_player.update()
	near_player.draw(game_surface)

	#all_sprites.update()
	#all_sprites.draw(game_surface)

	fullscreen_with_ratio()

	get_fps = clock.get_fps()
	draw_text(window, str(int(get_fps)), 20, 1200, 100, (255,255,255))


	pygame.display.flip()

	near_player = pygame.sprite.Group()
