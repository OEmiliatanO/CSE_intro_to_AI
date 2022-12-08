import math
import tkinter
import numpy
import random
import time

genome = "01"

def random_pick_gene(slist, L):
	s = ""
	for slime in slist:
		s += slime.gene * 2
	#print(s)
	#print(len(s), L)
	return ''.join(random.sample(s, L))

def rand_string(n):
	s = ""
	for i in range(n):
		s += genome[random.randint(0, 65532) % len(genome)]
	return s

def E(wlim, w, val, gene):
	return sum([(val[i] if gene[i] == '1' else 0) for i in range(0, len(val))]) - (sum([(w[i] if gene[i] == '1' else 0) for i in range(0, len(w))]) - wlim)

class Slime:
	def __init__(self, name, scope, canv:tkinter.Canvas, wlim, w, val, field = (900, 900)):
		random.seed(time.time())
		self.x = random.randint(10, field[0] - 10)
		self.y = random.randint(10, field[1] - 10)
		self.vx = random.choice([-1, 1]) * 300
		self.vy = random.choice([-1, 1]) * 300
		self.angle = math.atan2(self.vy, self.vx)
		self.scope = scope
		
		self.name = name
		self.canv = canv
		
		self.L = random.randint(26, 100)
		self.gene = rand_string(self.L)
		self.reproduction = 0
		self.calattr(wlim, w, val)
		self.fill_attr_color()

	def draw(self, scale = 11):
		self.angle = math.atan2(self.vy, self.vx)
		arx = self.x + scale * math.cos(self.angle)
		ary = self.y + scale * math.sin(self.angle)
		self.canv.create_line(self.x, self.y, arx, ary, fill = self.color, arrow='last', tag = self.name)

	def fly(self, dt, boundaryx, boundaryy):
		speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
		minspeed = 400
		maxspeed = 600
		if speed > maxspeed:
			self.vx = (self.vx / speed) * maxspeed
			self.vy = (self.vy / speed) * maxspeed
		if speed < minspeed:
			self.vx = (self.vx / speed) * minspeed
			self.vy = (self.vy / speed) * minspeed
		self.x += self.vx * dt
		self.y += self.vy * dt
		self.x %= boundaryx
		self.y %= boundaryy
		self.canv.delete(self.name)
		self.draw()

	def dist(self, other):
		return math.sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))

	def fill_attr_color(self):
		#self.color = "#" + ("%02x" % int(self.atk/self.L*255)) + ("%02x" % int(self.gene.count('H')/self.L*255)) + ("%02x" % int(self.gene.count('D')/self.L*255))
		self.color = "#" + ("%06x" % random.randint(0, 16777215))
	def attack(self, other):
		#other.hp -= max(self.atk - other.defen, 0)
		if other.defen == 0:
			other.hp -= self.atk
		elif other.defen < 0:
			other.hp -= self.atk * abs(other.defen / (other.defen - 100))
		else:
			other.hp -= self.atk * (other.defen / (other.defen+100))
	def destroy(self):
		self.canv.delete(self.name)
	def calattr(self, wlim, w, val):
		self.hp  = 100 * E(wlim, w, val, self.gene)
		self.atk = 2 * E(wlim, w, val, self.gene)
		self.defen = E(wlim, w, val, self.gene)

"""
"""
