import pygame

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
window = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
pygame.display.set_caption("p")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

class obj(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 50))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.centery = height / 2
		self.rect.centerx = width / 2
		all_sprites.add(self)
	def update(self):
		keyboard = pygame.key.get_pressed()
		if keyboard[pygame.K_a]:
			self.rect.x -= 10
		if keyboard[pygame.K_d]:
			self.rect.x += 10
		if keyboard[pygame.K_s]:
			self.rect.y += 10
		if keyboard[pygame.K_w]:
			self.rect.y -= 10
		
class mouse(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10, 10))
		self.rect = self.image.get_rect()
		self.image.fill((255,0,0))
		self.rect.centerx = width / 2
		self.rect.centery = height / 2
		self.mouse_busy = False
		pygame.mouse.set_visible(False)
		all_sprites.add(self)
	def update(self):
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

class inventory_slot(pygame.sprite.Sprite):
	def __init__(self, x, y, manager):
		pygame.sprite.Sprite.__init__(self)
		self.manager = manager
		self.image = pygame.Surface((16 + 16 / 2, 16 + 16 / 2))
		self.rect = self.image.get_rect()
		self.image.fill(YELLOW)
		self.rect.x = x
		self.rect.y = y

		self.free = True
		self.item = None

		all_sprites.add(self)

	def update(self):
		self.image.fill(YELLOW)
		draw_text(self.image, str(self.free), 16, self.rect.width / 2, self.rect.height / 2, WHITE)
		if self.item == None:
			self.free = True
		else:
			self.free = False



class inventory_manager():
	def __init__(self):
		self.slots = []
		self.itemz = []

		slot1 = inventory_slot(10, 10, self)
		slot2 = inventory_slot(10 + slot1.rect.right, 10, self)
		slot3 = inventory_slot(10 + slot2.rect.right, 10, self)
		slot4 = inventory_slot(10, slot1.rect.bottom + 10, self)
		slot5 = inventory_slot(10 + slot4.rect.right, slot4.rect.y, self)
		slot6 = inventory_slot(10 + slot5.rect.right, slot4.rect.y, self)

		self.slotz = [slot1, slot2, slot3, slot4, slot5, slot6]

		uo_manager.objs.append(self)

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

		all_sprites.add(self)

	def update(self):
		if self.in_inventory == False:
			collide_p = self.rect.colliderect(p)
			if collide_p:
				for i in i_manager.slotz:
					if i.free:
						self.slot = i
						i.item = self
						self.slot.free = False
						self.in_inventory = True
						i_manager.itemz.append(self)
						break

		if self.in_inventory == True:
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
						if self.rect.colliderect(i) and i.free == True:
							self.slot.item = None
							self.slot = i
							i.item = self
							collide = True
							break

						elif self.rect.colliderect(i) and i.free == False:
							i.item.slot = self.slot
							self.slot.item = i.item
							i.item = self
							self.slot = i
							collide = True
							break
					if collide == False:
						self.slot.item = None
						self.in_inventory = False
						for x in i_manager.itemz:
							if x == self:
								i_manager.itemz.remove(self)

						self.rect.right = p.rect.left
						self.rect.bottom = p.rect.bottom

			else:
				self.rect.centerx = self.slot.rect.centerx
				self.rect.centery = self.slot.rect.centery


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

		all_sprites.add(self)

	def update(self):
		if self.in_inventory == False:
			self.image.fill(RED)
			draw_text(self.image, str(self.in_stack), 16, self.rect.width / 2, self.rect.height / 2, WHITE)
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
								if x.free:
									self.slot = x
									x.item = self
									self.slot.free = False
									self.in_inventory = True
									i_manager.itemz.append(self)
									break
							break
				else:
					for i in i_manager.slotz:
						if i.free:
							self.slot = i
							i.item = self
							self.slot.free = False
							self.in_inventory = True
							i_manager.itemz.append(self)
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
						if self.rect.colliderect(i) and i.item == None or self.rect.colliderect(i) and i.item == self:
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


						elif self.rect.colliderect(i) and i.item != None:
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
						self.rect.right = p.rect.left
						self.rect.bottom = p.rect.bottom
			else:
				self.rect.centerx = self.slot.rect.centerx
				self.rect.centery = self.slot.rect.centery



class item3(pygame.sprite.Sprite):
	def __init__(self, x, y, in_stack):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((16, 16))
		self.rect = self.image.get_rect()
		self.image.fill(WHITE)
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

		all_sprites.add(self)

	def update(self):
		if self.in_inventory == False:
			self.image.fill(WHITE)
			draw_text(self.image, str(self.in_stack), 16, self.rect.width / 2, self.rect.height / 2, RED)
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
								if x.free:
									self.slot = x
									x.item = self
									self.slot.free = False
									self.in_inventory = True
									i_manager.itemz.append(self)
									break
							break
				else:
					for i in i_manager.slotz:
						if i.free:
							self.slot = i
							i.item = self
							self.slot.free = False
							self.in_inventory = True
							i_manager.itemz.append(self)
							break

		if self.in_inventory == True:
			self.image.fill(WHITE)
			draw_text(self.image, str(self.in_stack), 16, self.rect.width / 2, self.rect.height / 2, RED)
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
						if self.rect.colliderect(i) and i.item == None or self.rect.colliderect(i) and i.item == self:
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


						elif self.rect.colliderect(i) and i.item != None:
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
						self.rect.right = p.rect.left
						self.rect.bottom = p.rect.bottom
			else:
				self.rect.centerx = self.slot.rect.centerx
				self.rect.centery = self.slot.rect.centery


class updateble_objects():
	def __init__(self):
		self.objs = []
	def update(self):
		for i in self.objs:
			i.update()

def draw_text(surf, text, size, x, y, color):
	font_name = pygame.font.match_font('arial')
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.center = (x, y)
	surf.blit(text_surface, text_rect)

uo_manager = updateble_objects()

i_manager = inventory_manager()

m = mouse()
p = obj()
item1(0,0)
item1(0, 100)
item2(width - 10, height - 10, 11)
item2(width - 40, height - 10, 4)

item2(width - 10, height - 10, 16)
item2(width - 40, height - 10, 4)

item3(width - 10, height - 100, 12)
item3(width - 70, height - 10, 14)

running = True
while running:
	clock.tick(fps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
		
	window.fill(GREEN)

	uo_manager.update()

	all_sprites.update()
	all_sprites.draw(window)
	
	pygame.display.flip()