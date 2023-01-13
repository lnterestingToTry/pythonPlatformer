import random
import math
"""test_list = [0,0,0,0,0,0,0,0,0,0,0]
print(test_list)


def func(elemnt, index, list_):
	list_.remove(list_[index])
	list_.insert(3, elemnt)

	return list_

test_list = func(3, 5, test_list)

print (test_list)"""
def revers_matrix(lvl_matrix):
	list_ = []
	for i in lvl_matrix:
		list_.insert(0, i)

	return list_

def remove_insert_element(elemnt, index, list_):
	list_.remove(list_[index])
	list_.insert(index, elemnt)

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

	random_number_for_spawnpoint = random.randint(4, lvl_hight - 2)
	lvl[random_number_for_spawnpoint][1] = 2

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
	return lvl

def create_plates_of_matrix(lvl_matrix):
	lvl = lvl_matrix
	for i in lvl:
		for element in i:
			if element == 2:
				lvl[lvl.index(i) + 1][1] = 1
				lvl[lvl.index(i) + 1][2] = 1

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
					y += random.randint(1, 2)
					plate_created = True

		if randomx_previous_step + randomx_step < lvl_width - 2:
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
						lvl[y][x + num] = 1
		y += 1

	lvl = revers_matrix(lvl)

	return lvl



lvl_width = 24
lvl_hight = 20

l1 = create_lvl_matrix(lvl_width, lvl_hight)
l2 = create_board_of_lvl_matrix(l1)
l3 = create_plates_of_matrix(l2)

for i in l3:
	print(i)

