import pygame
import random
import math
from os import path

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
backgroundparts = pygame.sprite.Group()
near_player = pygame.sprite.Group()
static_objs = pygame.sprite.Group()
kinematic_objs = pygame.sprite.Group()
interface_objs = pygame.sprite.Group()

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
	def __init__(self, pers):
		self.triggerz = []

		self.pers = pers

		uo_manager.objs.append(self)

		l1 = create_lvl_matrix(lvl_width, lvl_hight)
		l1 = create_board_of_lvl_matrix(l1)
		l1 = create_plates_of_matrix(l1)
		#l1 = test_lvl

		l2 = create_lvl_matrix(lvl_width, lvl_hight)
		l2 = create_board_of_lvl_matrix(l2)
		l2 = create_plates_of_matrix(l2)

		l3 = create_lvl_matrix(lvl_width, lvl_hight)
		l3 = create_board_of_lvl_matrix(l3)
		l3 = create_plates_of_matrix(l3)

		lvl_bild(l1, block_size_var)

		global p
		p = self.pers()
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
		#draw_text(game_surface, str(self.lvl_now), 20, 100, 100, (255,255,255))

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
						lvl_bild(self.lvlz[self.lvl_now], block_size_var)

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

						for i in i_manager.slotz:
							all_sprites.add(i)
						for i in i_manager.itemz:
							all_sprites.add(i)
						all_sprites.add(m)

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

						lvl_bild(self.lvlz[self.lvl_now], block_size_var)

						all_sprites.add(p)
						kinematic_objs.add(p)
						p.speedx = 0
						p.speedy = 0

						for i in all_sprites:
							if type(i) == exit_point_for_lvl:
								p.rect.right = i.rect.left - 2
								p.rect.bottom = i.rect.bottom

						for i in all_sprites:
							if i != p:
								i.kill()
								all_sprites.add(i)

						self.cc = camera_control(p)

						for i in i_manager.slotz:
							all_sprites.add(i)
						for i in i_manager.itemz:
							all_sprites.add(i)
						all_sprites.add(m)


						for i in all_sprites:
							if type(i) == spawn_point_for_lvl or type(i) == exit_point_for_lvl:
								self.triggerz.append(i)



test_lvl = [[0,0,0,0,0,0,0,0,101],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0],
			[0,0,0,0,0,1,0,0],
			[0,0,0,0,0,1,1,0],
			[0,0,0,0,0,0,0,0],
			[2,0,0,0,0,0,0,0,0],
			[1,0,0,0,1,0,0,0,0],
			[1,0,0,0,1,0,0,1,1,1],
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
						y += random.randint(1, 3)
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

			if element == 101:
				mob1_1(x, y)

class background_manager():
	def __init__(self, images):
		self.images = images

		self.left_max = 0
		self.right_max = width - 0
		self.top_max = 0
		self.bottom_max = height - 0

		self.max_left_detected = width
		self.max_right_detected = 0
		self.max_top_detected = height
		self.max_bottom_detected = 0

		self.part_width = res_lvl.lvl_backgroundparts[0].get_width()
		self.part_height = res_lvl.lvl_backgroundparts[0].get_height()

		self.plates_per_width = math.ceil(width / self.part_width) + 2
		self.plates_per_height = math.ceil(height / self.part_height) + 2

		x = 0
		y = 0

		for i in range(self.plates_per_height):
			for i in range(self.plates_per_width):
				backgroundpart_img(x, y)
				x += self.part_width
			y += self.part_height
			x = 0

		uo_manager.objs.append(self)

	def update(self):

		if backgroundparts:
			for i in backgroundparts:
				if i.rect.left < self.max_left_detected:
					self.max_left_detected = i.rect.left
				if i.rect.right > self.max_right_detected:
					self.max_right_detected = i.rect.right

				if i.rect.top < self.max_top_detected:
					self.max_top_detected = i.rect.top

				if i.rect.bottom > self.max_bottom_detected:
					self.max_bottom_detected = i.rect.bottom

			for i in backgroundparts:
				if i.rect.right < 0 - self.part_width:
					i.rect.left = self.max_right_detected
					#i.change_img()
				if i.rect.left > width + self.part_width:
					i.rect.right = self.max_left_detected
					#i.change_img()

			for i in backgroundparts:
				if i.rect.bottom < 0 - self.part_height:
					i.rect.top = self.max_bottom_detected
					#i.change_img()
				if i.rect.top > height + self.part_height:
					i.rect.bottom = self.max_top_detected
					#i.change_img()


			#print(self.max_left_detected)
			#print(self.max_right_detected)

		self.max_left_detected = width
		self.max_right_detected = 0
		self.max_top_detected = width
		self.max_bottom_detected = 0

class backgroundpart_img(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = random.choice(res_lvl.lvl_backgroundparts)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		backgroundparts.add(self)
	def update(self):
		pass
		"""if self.rect.right < 0:
			self.kill()
		if self.rect.left > width - 0:
			self.kill()
		if self.rect.bottom < 0:
			self.kill()
		if self.rect.top > height - 0:
			self.kill()"""

	def change_img(self):
		self.image = random.choice(res_lvl.lvl_backgroundparts)




		



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
		self.image = random.choice(res.lvl_blockz)
		#self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		static_objs.add(self)
		all_sprites.add(self)
	def update(self):
		mouse_pressed = pygame.mouse.get_pressed()
		collide_m = self.rect.colliderect(m)
		if collide_m and mouse_pressed[2]:
			self.kill()

		for i in kinematic_objs:
			if near_player.has(i):

				if i.rect.bottom > self.rect.top and i.rect.top < self.rect.top and self.rect.left < i.rect.left < self.rect.right or i.rect.bottom > self.rect.top and i.rect.top < self.rect.top and self.rect.left < i.rect.right < self.rect.right or i.rect.bottom > self.rect.top and i.rect.top < self.rect.top and self.rect.left < i.rect.centerx < self.rect.right:
					#if i.fall == True:
					i.rect.bottom = self.rect.top
					i.fall = False
					i.fall_time = 0
					i.fall_sieed = 0

				if i.rect.top < self.rect.bottom and i.rect.bottom > self.rect.bottom and self.rect.left < i.rect.left < self.rect.right or i.rect.top < self.rect.bottom and i.rect.bottom > self.rect.bottom and self.rect.left < i.rect.right < self.rect.right:
					#if i.jumi == True:
					i.jump_init()
					i.rect.top = self.rect.bottom
					i.fall = True
					print("here3")

				if self.rect.bottom > i.rect.top + 1 > self.rect.top and i.rect.left < self.rect.right and i.rect.right > self.rect.right:
					i.rect.left = self.rect.right
					i.fall = True
					i.jump_init()
					print("here5")

				if self.rect.top < i.rect.bottom - 1 < self.rect.bottom and i.rect.left < self.rect.right and i.rect.right > self.rect.right:
					print("here1")
					i.rect.left = self.rect.right
					i.fall = True
					i.jump_init()

				if self.rect.bottom > i.rect.top + 1 > self.rect.top and i.rect.right > self.rect.left and i.rect.left < self.rect.left:
					i.rect.right = self.rect.left
					i.fall = True
					i.jump_init()
					print("here2")

				if self.rect.top < i.rect.bottom - 1 < self.rect.bottom and i.rect.right > self.rect.left and i.rect.left < self.rect.left:
					i.rect.right = self.rect.left
					i.fall = True
					i.jump_init()
					print("here4")

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

		self.image_default_move_way_x1 = pygame.Surface((16, 16))
		self.image_default_move_way_x1.fill(RED)
		self.image_default_move_way_x0 = pygame.transform.flip(self.image_default_move_way_x1, True, False)

		self.image_hand_move_way_x1 = pygame.Surface((16, 16))
		self.image_hand_move_way_x0 = pygame.transform.flip(self.image_hand_move_way_x1, True, False)

		self.image_move_way_x1 = self.image_default_move_way_x1
		self.image_move_way_x0 = pygame.transform.flip(self.image_move_way_x1, True, False)


		self.sword_in_hand = False

		self.image = self.image_move_way_x1
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
		self.speedx = 6

		self.sword = None

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

		#if self.jump == False:
			#self.fall = True

		trig = False
		for i in near_player:
			if type(i) == block:
				if i.rect.left < self.rect.left < i.rect.right or i.rect.left < self.rect.right < i.rect.right: 

					left_fall_collide = i.rect.collidepoint(self.rect.left, self.rect.bottom)
					center_fall_collide = i.rect.collidepoint(self.rect.centerx, self.rect.bottom)
					right_fall_collide = i.rect.collidepoint(self.rect.right, self.rect.bottom)

					left_side_collide_bottom = i.rect.collidepoint(self.rect.right, self.rect.bottom)
					left_side_collide_centery = i.rect.collidepoint(self.rect.right, self.rect.centery)
					left_side_collide_top = i.rect.collidepoint(self.rect.right, self.rect.top)

					right_side_collide_bottom = i.rect.collidepoint(self.rect.left, self.rect.bottom)
					right_side_collide_centery = i.rect.collidepoint(self.rect.left, self.rect.centery)
					right_side_collide_top = i.rect.collidepoint(self.rect.left, self.rect.top)

					if left_fall_collide == True or right_fall_collide == True or center_fall_collide == True:
						trig = True 
						self.fall = False
					elif trig == False and self.jump == False:
						self.fall = True


					if left_side_collide_top or left_side_collide_centery or left_side_collide_bottom or right_side_collide_top or right_side_collide_centery or right_side_collide_bottom:
						self.jump_init()
		trig = False


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

		elif self.jump == True and self.jump_power <= 0:
			self.jump = False
			self.fall = True

		draw_text(game_surface, str(self.fall), 20, 10, 10, (255,255,255))

		self.move_left = False
		self.move_right = False

		if i_manager.slot_for_sword.free == False:
			self.sword_in_hand = True
		else:
			self.sword_in_hand = False

		if self.sword_in_hand:
			self.image_move_way_x1 = self.image_hand_move_way_x1
			self.image_move_way_x0 = pygame.transform.flip(self.image_move_way_x1, True, False)
		else:
			self.image_move_way_x1 = self.image_default_move_way_x1
			self.image_move_way_x0 = pygame.transform.flip(self.image_move_way_x1, True, False)




		if self.move_way_x == 0:
			self.image = self.image_move_way_x0
		if self.move_way_x == 1:
			self.image = self.image_move_way_x1

		self.sword_in_hand = False




	def jump_init(self):
		self.jump = False
		self.jump_power = 11

class pers1(player):
	def __init__(self):
		player.__init__(self)
		self.image_default_move_way_x1 = res.pers1
		self.image_move_way_x0 = pygame.transform.flip(self.image_move_way_x1, True, False)

		self.image_hand_move_way_x1 = res.pers1_hand
		self.image_hand_move_way_x0 = pygame.transform.flip(self.image_hand_move_way_x1, True, False)


		self.image = self.image_default_move_way_x1

		self.rect = self.image.get_rect()



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
		if self.centrated_obj.rect.centerx > width / 2 + width / 7 and self.centrated_obj.move_way_x == 2:
			self.centringx = True
			self.speedx -= 1

		if self.centrated_obj.rect.centerx < width / 2 - width / 7 and self.centrated_obj.move_way_x == 2:
			self.speedx += 1
			self.centringx = True


		if self.centrated_obj.rect.centery > height - (height / 4):# and self.centrated_obj.move_way_y == 2:
			self.speedy -= 1
			self.centringy = True

		if self.centrated_obj.rect.centery < height / 4:# and self.centrated_obj.move_way_y == 2:
			self.speedy += 1
			self.centringy = True

		for i in all_sprites:
			i.rect.x += self.speedx
			i.rect.y += self.speedy

		for i in backgroundparts:
			i.rect.x += math.ceil(self.speedx / 2)
			i.rect.y += math.ceil(self.speedy / 2)

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

######################inventory<
		
class mouse(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10, 10))
		self.rect = self.image.get_rect()
		self.image.fill((255,0,0))
		self.rect.centerx = width / 2
		self.rect.centery = height / 2
		self.mouse_busy = False
		self.x = self.rect.x
		self.y = self.rect.y
		pygame.mouse.set_visible(False)
		interface_objs.add(self)
	def update(self):
		#interface_objs.remove(self)
		#interface_objs.add(self)
		self.rect.x = self.x
		self.rect.y = self.y
		mouse_rel = pygame.mouse.get_rel()
		self.rect.x += int(mouse_rel[0] / 2.5)
		self.rect.y += int(mouse_rel[1] / 2.5)
		if self.rect.bottom > height:
			self.rect.bottom = height
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > width:
			self.rect.right = width
		if self.rect.top < 0:
			self.rect.top = 0
		self.x = self.rect.x
		self.y = self.rect.y

class inventory_slot(pygame.sprite.Sprite):
	def __init__(self, x, y, manager):
		pygame.sprite.Sprite.__init__(self)
		self.manager = manager
		self.image = pygame.Surface((16 + 16 / 2, 16 + 16 / 2))
		self.rect = self.image.get_rect()
		self.image.fill(YELLOW)
		self.x = x
		self.y = y
		self.rect.x = self.x
		self.rect.y = self.y
		self.destination = 0 #any

		self.free = True
		self.item = None

		#all_sprites.add(self)
		interface_objs.add(self)

	def update(self):
		#all_sprites.remove(self)
		#all_sprites.add(self)
		self.rect.x = self.x
		self.rect.y = self.y
		self.image.fill(YELLOW)
		#draw_text(self.image, str(self.free), 16, self.rect.width / 2, self.rect.height / 2, WHITE)
		if self.item == None:
			self.free = True
		else:
			self.free = False

class inventory_slot_for_sword(pygame.sprite.Sprite):
	def __init__(self, x, y, manager):
		pygame.sprite.Sprite.__init__(self)
		self.manager = manager
		self.image = pygame.Surface((16 + 16 / 2, 16 + 16 / 2))
		self.rect = self.image.get_rect()
		self.image.fill(YELLOW)
		self.x = x
		self.y = y
		self.rect.x = self.x
		self.rect.y = self.y
		self.destination = 1 #sword

		self.free = True
		self.item = None

		#all_sprites.add(self)
		interface_objs.add(self)

	def update(self):
		#all_sprites.remove(self)
		#all_sprites.add(self)
		self.rect.x = self.x
		self.rect.y = self.y
		self.image.fill(YELLOW)
		#draw_text(self.image, str(self.free), 16, self.rect.width / 2, self.rect.height / 2, WHITE)
		if self.item == None:
			self.free = True
		else:
			self.free = False

class inventory_slot_for_armor(pygame.sprite.Sprite):
	def __init__(self, x, y, manager):
		pygame.sprite.Sprite.__init__(self)
		self.manager = manager
		self.image = pygame.Surface((16 + 16 / 2, 16 + 16 / 2))
		self.rect = self.image.get_rect()
		self.image.fill(YELLOW)
		self.x = x
		self.y = y
		self.rect.x = self.x
		self.rect.y = self.y
		self.destination = 2 #armor

		self.free = True
		self.item = None

		#all_sprites.add(self)
		interface_objs.add(self)

	def update(self):
		#all_sprites.remove(self)
		#all_sprites.add(self)
		self.rect.x = self.x
		self.rect.y = self.y
		self.image.fill(YELLOW)
		#draw_text(self.image, str(self.free), 16, self.rect.width / 2, self.rect.height / 2, WHITE)
		if self.item == None:
			self.free = True
		else:
			self.free = False

class inventory_slot_for_artefact(pygame.sprite.Sprite):
	def __init__(self, x, y, manager):
		pygame.sprite.Sprite.__init__(self)
		self.manager = manager
		self.image = pygame.Surface((16 + 16 / 2, 16 + 16 / 2))
		self.rect = self.image.get_rect()
		self.image.fill(YELLOW)
		self.x = x
		self.y = y
		self.rect.x = self.x
		self.rect.y = self.y
		self.destination = 3 #artefact

		self.free = True
		self.item = None

		#all_sprites.add(self)
		interface_objs.add(self)

	def update(self):
		#all_sprites.remove(self)
		#all_sprites.add(self)
		self.rect.x = self.x
		self.rect.y = self.y
		self.image.fill(YELLOW)
		#draw_text(self.image, str(self.free), 16, self.rect.width / 2, self.rect.height / 2, WHITE)
		if self.item == None:
			self.free = True
		else:
			self.free = False

class inventory_manager():
	def __init__(self, itemz):
		self.slotz = []
		self.itemz = []

		if itemz != []:
			for i in itemz:
				all_sprites.add(i)
				i.slot = None
				i.in_inventory = False

				i.rect.centerx = p.rect.centerx
				i.rect.centerx = p.rect.centerx

		slot1 = inventory_slot(width - 100, 10, self)
		slot2 = inventory_slot(10 + slot1.rect.right, 10, self)
		slot3 = inventory_slot(10 + slot2.rect.right, 10, self)
		slot4 = inventory_slot(width - 100, slot1.rect.bottom + 10, self)
		slot5 = inventory_slot(10 + slot4.rect.right, slot4.rect.y, self)
		slot6 = inventory_slot(10 + slot5.rect.right, slot4.rect.y, self)

		self.slot_for_sword = inventory_slot_for_sword(width - 100, slot6.rect.bottom + 10, self)
		self.slot_for_armor = inventory_slot_for_armor(self.slot_for_sword.rect.right + 10, self.slot_for_sword.rect.y, self)
		self.slot_for_artefact = inventory_slot_for_artefact(self.slot_for_armor.rect.right + 10, self.slot_for_sword.rect.y, self)


		self.slotz = [slot1, slot2, slot3, slot4, slot5, slot6, self.slot_for_sword, self.slot_for_armor, self.slot_for_artefact]
		global m
		m = mouse()

		uo_manager.objs.append(self)

		#item1(300, 0)
		#item1(300, 100)
		#item2(300, 100, 15)
		item2(300, 0, 12)
		sword1(400, 0)
		#sword2(500, 0)

	def update(self):
		pass
		#print(self.itemz)

class item1(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((16, 16))
		self.rect = self.image.get_rect()
		self.image.fill(BLUE)
		self.rect.centerx = x
		self.rect.centery = y

		self.stackeble = False
		self.in_inventory = False
		self.slot = None
		self.mouse_move = False

		self.fall = True
		self.fall_time = 0
		self.gravitation_var = 4
		self.fall_speed = 0

		self.destination = 0

		kinematic_objs.add(self)
		all_sprites.add(self)

	def update(self):
		if self.in_inventory == False:
			self.fall = True
			#all_sprites.remove(self)
			#all_sprites.add(self)
			if self.fall == True:
				for i in near_player:
					if type(i) == block:
						if i.rect.left < self.rect.left < i.rect.right or i.rect.left < self.rect.right < i.rect.right: 

							left_fall_collide = i.rect.collidepoint(self.rect.left, self.rect.bottom)
							center_fall_collide = i.rect.collidepoint(self.rect.centerx, self.rect.bottom)
							right_fall_collide = i.rect.collidepoint(self.rect.right, self.rect.bottom)

							left_side_collide_bottom = i.rect.collidepoint(self.rect.right, self.rect.bottom)
							left_side_collide_centery = i.rect.collidepoint(self.rect.right, self.rect.centery)
							left_side_collide_top = i.rect.collidepoint(self.rect.right, self.rect.top)

							right_side_collide_bottom = i.rect.collidepoint(self.rect.left, self.rect.bottom)
							right_side_collide_centery = i.rect.collidepoint(self.rect.left, self.rect.centery)
							right_side_collide_top = i.rect.collidepoint(self.rect.left, self.rect.top)

							if left_fall_collide == True and self.fall == True or right_fall_collide == True and self.fall == True or center_fall_collide == True and self.fall == True:
								self.fall = False
								kinematic_objs.remove(self)

							#if left_side_collide_top or left_side_collide_centery or left_side_collide_bottom or right_side_collide_top or right_side_collide_centery or right_side_collide_bottom:
							#	self.jump_init()

			if self.fall == True:
				if self.fall_speed + self.gravitation_var * self.fall_time < block_size_var:
					self.fall_speed = self.fall_speed + self.gravitation_var * self.fall_time
				self.fall_time += 1
				self.rect.y += self.fall_speed


			collide_p = self.rect.colliderect(p)
			if collide_p:
				for i in i_manager.slotz:
					if i.free and i.destination == self.destination:
						self.slot = i
						i.item = self
						self.slot.free = False
						self.in_inventory = True
						i_manager.itemz.append(self)
						kinematic_objs.remove(self)
						all_sprites.remove(self)
						interface_objs.add(self)
						break

		if self.in_inventory == True:
			#all_sprites.remove(self)
			#all_sprites.add(self)
			mouse_pressed = pygame.mouse.get_pressed()
			collide_m = self.rect.colliderect(m)
			if collide_m and mouse_pressed[0] == True and m.mouse_busy == False:
				self.mouse_move = True
				m.mouse_busy = True
			if self.mouse_move == True:
				self.rect.centerx = m.rect.centerx
				self.rect.centery = m.rect.centery
				if mouse_pressed[0] == False:
					self.mouse_move = False
					m.mouse_busy = False
					collide = False
					for i in i_manager.slotz:
						if self.rect.colliderect(i) and i.free == True and i.destination == self.destination:
							self.slot.item = None
							self.slot = i
							i.item = self
							collide = True
							interface_objs.add(self)
							all_sprites.remove(self)
							break

						elif self.rect.colliderect(i) and i.free == False and i.destination == self.destination:
							i.item.slot = self.slot
							self.slot.item = i.item
							i.item = self
							self.slot = i
							collide = True
							interface_objs.add(self)
							all_sprites.remove(self)
							break

						elif self.rect.colliderect(i) and i.free == True and i.destination != 0 or self.rect.colliderect(i) and i.free == False and i.destination != self.destination:
							collide = True
							#interface_objs.add(self)
							#all_sprites.remove(self)
							break

					if collide == False:
						self.slot.item = None
						self.in_inventory = False
						for x in i_manager.itemz:
							if x == self:
								i_manager.itemz.remove(self)
						kinematic_objs.add(self)
						interface_objs.remove(self)
						all_sprites.add(self)

						if p.rect.centerx >= m.rect.centerx:
							self.rect.right = p.rect.left - 10
							self.rect.bottom = p.rect.top
						if p.rect.centerx <= m.rect.centerx:
							self.rect.left = p.rect.right + 10
							self.rect.bottom = p.rect.top

			else:
				self.rect.centerx = self.slot.rect.centerx
				self.rect.centery = self.slot.rect.centery

	def jump_init(self):
		pass


class item2(pygame.sprite.Sprite):
	def __init__(self, x, y, in_stack):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((16, 16))
		self.rect = self.image.get_rect()
		self.image.fill(RED)
		self.rect.centerx = x
		self.rect.centery = y

		self.stackeble = True
		self.in_stack = in_stack
		self.max_in_stack = 16

		if self.in_stack > self.max_in_stack:
			self.in_stack = self.max_in_stack
			print("in_stack wrong var")
		self.in_inventory = False
		self.slot = None
		self.mouse_move = False

		self.fall = True
		self.fall_time = 0
		self.gravitation_var = 4
		self.fall_speed = 0

		self.destination = 0

		kinematic_objs.add(self)
		all_sprites.add(self)

	def update(self):
		if self.in_inventory == False:
			self.fall = True
			self.image.fill(RED)
			draw_text(self.image, str(self.in_stack), 16, self.rect.width / 2, self.rect.height / 2, WHITE)

			if self.fall == True:
				for i in near_player:
					if type(i) == block:
						if i.rect.left < self.rect.left < i.rect.right or i.rect.left < self.rect.right < i.rect.right: 
		
							left_fall_collide = i.rect.collidepoint(self.rect.left, self.rect.bottom)
							center_fall_collide = i.rect.collidepoint(self.rect.centerx, self.rect.bottom)
							right_fall_collide = i.rect.collidepoint(self.rect.right, self.rect.bottom)

							left_side_collide_bottom = i.rect.collidepoint(self.rect.right, self.rect.bottom)
							left_side_collide_centery = i.rect.collidepoint(self.rect.right, self.rect.centery)
							left_side_collide_top = i.rect.collidepoint(self.rect.right, self.rect.top)

							right_side_collide_bottom = i.rect.collidepoint(self.rect.left, self.rect.bottom)
							right_side_collide_centery = i.rect.collidepoint(self.rect.left, self.rect.centery)
							right_side_collide_top = i.rect.collidepoint(self.rect.left, self.rect.top)

							if left_fall_collide == True and self.fall == True or right_fall_collide == True and self.fall == True or center_fall_collide == True and self.fall == True:
								self.fall = False
								kinematic_objs.remove(self)

						#if left_side_collide_top or left_side_collide_centery or left_side_collide_bottom or right_side_collide_top or right_side_collide_centery or right_side_collide_bottom:
						#	self.jump_init()
			if self.fall == True:
				if self.fall_speed + self.gravitation_var * self.fall_time < block_size_var:
					self.fall_speed = self.fall_speed + self.gravitation_var * self.fall_time
				self.fall_time += 1
				self.rect.y += self.fall_speed


			collide_p = self.rect.colliderect(p)
			if collide_p:
				for i in i_manager.slotz:
					if type(i.item) == type(self):
						if i.item.in_stack + self.in_stack < self.max_in_stack:
							i.item.in_stack += self.in_stack
							self.kill()
							break

						elif i.item.in_stack + self.in_stack > self.max_in_stack:
							in_stack_difference = self.max_in_stack - i.item.in_stack
							i.item.in_stack = self.max_in_stack
							self.in_stack -= in_stack_difference
							for x in i_manager.slotz:
								if x.free and x.destination == self.destination:
									self.slot = x
									x.item = self
									self.slot.free = False
									self.in_inventory = True
									i_manager.itemz.append(self)
									kinematic_objs.remove(self)
									all_sprites.remove(self)
									interface_objs.add(self)
									break
							break
				else:
					for i in i_manager.slotz:
						if i.free and i.destination == self.destination:

							self.slot = i
							i.item = self
							self.slot.free = False
							self.in_inventory = True
							i_manager.itemz.append(self)
							kinematic_objs.remove(self)
							all_sprites.remove(self)
							interface_objs.add(self)
							break

		if self.in_inventory == True:
			self.image.fill(RED)
			draw_text(self.image, str(self.in_stack), 16, self.rect.width / 2, self.rect.height / 2, WHITE)
			mouse_pressed = pygame.mouse.get_pressed()
			collide_m = self.rect.colliderect(m)
			if collide_m and mouse_pressed[0] == True and m.mouse_busy == False:
				self.mouse_move = True
				m.mouse_busy = True
			if self.mouse_move == True:
				self.rect.centerx = m.rect.centerx
				self.rect.centery = m.rect.centery
				if mouse_pressed[0] == False:
					self.mouse_move = False
					m.mouse_busy = False
					collide = False
					#self.slot.item = None
					#self.slot = None
					for i in i_manager.slotz:
						if self.rect.colliderect(i) and i.item == None and i.destination == self.destination or self.rect.colliderect(i) and i.item == self:
							self.slot.item = None
							self.slot = i
							i.item = self
							collide = True
							break

						elif self.rect.colliderect(i) and i.item != None and type(i.item) == type(self):
							if i.item.in_stack + self.in_stack < self.max_in_stack:
								i.item.in_stack += self.in_stack
								self.slot.item = None
								for i in i_manager.itemz:
									if i == self:
										i_manager.itemz.remove(self)
								self.kill()
								collide = True
								break
							elif i.item.in_stack + self.in_stack > self.max_in_stack:
								in_stack_difference = self.max_in_stack - i.item.in_stack
								i.item.in_stack = self.max_in_stack
								self.in_stack -= in_stack_difference
								collide = True
								break

						elif self.rect.colliderect(i) and i.free == True and i.destination != self.destination or self.rect.colliderect(i) and i.free == False and i.destination != self.destination:
							collide = True
							#interface_objs.add(self)
							#all_sprites.remove(self)
							break


						elif self.rect.colliderect(i) and i.item != None and i.destination == self.destination:
							i.item.slot = self.slot
							self.slot.item = i.item
							i.item = self
							self.slot = i
							collide = True
							break

					if collide == False:
						self.slot.item = None
						self.in_inventory = False
						for i in i_manager.itemz:
							if i == self:
								i_manager.itemz.remove(self)

						kinematic_objs.add(self)
						interface_objs.remove(self)
						all_sprites.add(self)
						if p.rect.centerx >= m.rect.centerx:
							self.rect.right = p.rect.left - 10
							self.rect.bottom = p.rect.top
						if p.rect.centerx <= m.rect.centerx:
							self.rect.left = p.rect.right + 10
							self.rect.bottom = p.rect.top
			else:
				self.rect.centerx = self.slot.rect.centerx
				self.rect.centery = self.slot.rect.centery

	def jump_init(self):
		pass

class sword1(item1):
	def __init__(self, x, y):
		item1.__init__(self, x, y)
		self.destination = 1
		self.image = res.sword1_icon

	def update(self):
		item1.update(self)
		if self.in_inventory == True:
			if p.sword == None:
				p.sword = sword1_in_hand()

		if self.in_inventory == False:
			if type(p.sword) == sword1_in_hand:
				p.sword.kill()
				p.sword = None

class sword1_in_hand(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_move_way_x0 = pygame.transform.flip(res.sword1, True, False)
		self.image_move_way_x1 = res.sword1
		self.image = self.image_move_way_x1
		self.rect = self.image.get_rect()
		self.move_way_x = 0
		all_sprites.add(self)

	def update(self):
		p.sword_in_hand = True
		if p.move_way_x == 0:
			self.move_way_x = 0
		if self.move_way_x == 0:
			self.image = self.image_move_way_x0
			self.rect.bottom = p.rect.centery + 3
			self.rect.right = p.rect.left + 3

		if p.move_way_x == 1:
			self.move_way_x = 1
		if self.move_way_x == 1:
			self.image = self.image_move_way_x1
			self.rect.bottom = p.rect.centery + 3
			self.rect.left = p.rect.right - 3

class sword2(item1):
	def __init__(self, x, y):
		item1.__init__(self, x, y)
		self.destination = 1

######################inventory>

######################mobz<
class mob1_1(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((16,16))
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.jump = False
		self.fall = False
		self.last_jump_time = 0
		self.fall_speed = 0
		self.gravitation_var = 3
		self.fall_time = 0

		self.move_left = False
		self.move_right = False
		self.speedx = 0
		self.max_speedx = 2

		self.passive_walk = False
		self.pw_move_left = False
		self.pw_move_right = False
		self.pw_left_fall = False
		self.pw_right_fall = False
		self.pw_time = 0

		self.player_detected = False



		all_sprites.add(self)
		kinematic_objs.add(self)


	def update(self):
		kinematic_objs.add(self)
		self.fall = True
		self.pw_left_fall = False
		self.pw_right_fall = False

		self.move_left = False
		self.move_right = False


		for i in all_sprites:
			if type(i) == block:
				if i.rect.left <= self.rect.left <= i.rect.right or i.rect.left <= self.rect.right <= i.rect.right:
					left_fall_collide = i.rect.collidepoint(self.rect.left + 1, self.rect.bottom + 1)
					center_fall_collide = i.rect.collidepoint(self.rect.centerx, self.rect.bottom + 1)
					right_fall_collide = i.rect.collidepoint(self.rect.right - 1, self.rect.bottom + 1)

					left_side_collide_bottom = i.rect.collidepoint(self.rect.right, self.rect.bottom)
					left_side_collide_centery = i.rect.collidepoint(self.rect.right , self.rect.centery)
					left_side_collide_top = i.rect.collidepoint(self.rect.right, self.rect.top)

					right_side_collide_bottom = i.rect.collidepoint(self.rect.left, self.rect.bottom)
					right_side_collide_centery = i.rect.collidepoint(self.rect.left, self.rect.centery)
					right_side_collide_top = i.rect.collidepoint(self.rect.left, self.rect.top)

					if left_fall_collide == True or right_fall_collide == True or center_fall_collide == True:
						self.fall = False
					if left_fall_collide == True:
						self.pw_left_fall = True
					if right_fall_collide == True:
						self.pw_right_fall = True

		#if self.fall == False and self.jump == False and self.last_jump_time > 15:
		#	self.jump = True
		#	self.jump_power = 11
		#	self.last_jump_time = 0
		#else:
		#	self.last_jump_time += 1


		if self.fall == True:
			if self.fall_speed + self.gravitation_var * self.fall_time < block_size_var:
				self.fall_speed = self.fall_speed + self.gravitation_var * self.fall_time
			self.fall_time += 1
			self.rect.y += self.fall_speed

		#if self.jump == True and self.jump_power > 0:
			#self.rect.y -= self.jump_power
			#self.jump_power -= 1


		if self.passive_walk and self.pw_time > 0:
			if self.pw_move_right and self.pw_right_fall:
				self.move_right = True

			#elif self.pw_right_fall == False and self.pw_move_left:
				#self.pw_move_right = False

			if self.pw_move_left and self.pw_left_fall:
				self.move_left = True
				
			#elif self.pw_left_fall == False and self.pw_move_right:
				#self.pw_move_left = False

			self.pw_time -= 1

		elif self.pw_time <= 0 and self.passive_walk:
			self.pw_move_right = False
			self.pw_move_left = False
			self.pw_time = 10
			r = random.randint(0, 1)
			if r == 1:
				print("move_left")
				self.pw_move_left = True
			if r == 0:
				print("move_right")
				self.pw_move_right = True

		if self.move_right == True and self.speedx < self.max_speedx:
			self.speedx += 1

		if self.move_left == True and self.speedx > -self.max_speedx:
			self.speedx -= 1

		if self.move_left == False and self.move_right == False and self.speedx != 0:
			if self.speedx > 0:
				self.speedx -= 1
			if self.speedx < 0:
				self.speedx += 1


		if self.speedx > self.max_speedx:
			self.speedx = self.max_speedx
		if self.speedx < -self.max_speedx:
			self.speedx = -self.max_speedx

		self.rect.x += self.speedx

		if self.player_detected == True:
			self.passive_walk = False
		else:
			self.passive_walk = True



	def jump_init(self):
		pass











######################mobz>







class game_procces_manager():
	def __init__(self, pers):

		global res_lvl
		res_lvl = res_lvl1()#random.choice([res_lvl1, res_lvl2])()


		global uo_manager
		uo_manager = updateble_objects()

		global l_manager
		l_manager = lvl_manager(pers)

		global i_manager
		i_manager = inventory_manager([])

		background_manager(res_lvl.lvl_backgroundparts)

		self.for_crossing_lvl_inventory_save = []

		uo_manager.objs.append(self)
	def update(self):
		pass

class updateble_objects():
	def __init__(self):
		self.objs = []
	def update(self):
		for i in self.objs:
			i.update()

class res_load():
	def __init__(self):
		self.block = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block.png")).convert_alpha()
		self.block1 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block1.png")).convert_alpha()
		self.block2 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block2.png")).convert_alpha()
		self.block3 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block3.png")).convert_alpha()
		self.block4 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block4.png")).convert_alpha()
		self.lvl_blockz = [self.block1, self.block2, self.block3, self.block4]

		self.pers1 = pygame.image.load(path.join(this_directory, "res\\persz\\pers1\\pers.png")).convert_alpha()
		self.pers1_hand = pygame.image.load(path.join(this_directory, "res\\persz\\pers1\\pers_hand.png")).convert_alpha()

		self.sword1 = pygame.image.load(path.join(this_directory, "res\\itemz\\swordz\\sword1\\sword1.png")).convert_alpha()
		self.sword1_icon = pygame.image.load(path.join(this_directory, "res\\itemz\\swordz\\sword1\\sword1_icon.png")).convert_alpha()
		self.sword1_anim1_1 = pygame.image.load(path.join(this_directory, "res\\itemz\\swordz\\sword1\\sword1_anim1_1.png")).convert_alpha()
		self.sword1_anim1_2 = pygame.image.load(path.join(this_directory, "res\\itemz\\swordz\\sword1\\sword1_anim1_2.png")).convert_alpha()
		self.sword1_anim1_3 = pygame.image.load(path.join(this_directory, "res\\itemz\\swordz\\sword1\\sword1_anim1_3.png")).convert_alpha()
		self.sword1_anim1_4 = pygame.image.load(path.join(this_directory, "res\\itemz\\swordz\\sword1\\sword1_anim1_4.png")).convert_alpha()


class res_lvl1():
	def __init__(self):
		self.block = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block.png")).convert_alpha()
		self.block1 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block1.png")).convert_alpha()
		self.block2 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block2.png")).convert_alpha()
		self.block3 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block3.png")).convert_alpha()
		self.block4 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\block4.png")).convert_alpha()
		self.lvl_blockz = [self.block1, self.block2, self.block3, self.block4]

		self.backgroundpart1 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\backgroundpart1.png")).convert_alpha()
		self.backgroundpart2 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\backgroundpart2.png")).convert_alpha()
		self.backgroundpart3 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\backgroundpart3.png")).convert_alpha()
		self.backgroundpart4 = pygame.image.load(path.join(this_directory, "res\\lvlz\\lvl_1\\backgroundpart4.png")).convert_alpha()
		self.lvl_backgroundparts = [self.backgroundpart1, self.backgroundpart2, self.backgroundpart3, self.backgroundpart4]

class res_lvl2():
	def __init__(self):
		pass




this_directory = path.join(path.dirname(__file__))

res = res_load()



#p = test_obj()

lvl_width = 70
lvl_hight = 40

block_size_var = 16

gp_manager = game_procces_manager(pers1)

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

		if absolute_number(absolute_number(i.rect.centerx) - absolute_number(p.rect.centerx)) < 300 and absolute_number(absolute_number(i.rect.centery) - absolute_number(p.rect.centery)) < 200:
			if not interface_objs.has(i):
				near_player.add(i)

	backgroundparts.update()
	backgroundparts.draw(game_surface)
	near_player.update()
	near_player.draw(game_surface)
	interface_objs.update()
	interface_objs.draw(game_surface)

	#all_sprites.update()
	#all_sprites.draw(game_surface)

	fullscreen_with_ratio()

	get_fps = clock.get_fps()
	draw_text(window, str(int(get_fps)), 20, 1200, 100, (255,255,255))


	pygame.display.flip()

	near_player = pygame.sprite.Group()
