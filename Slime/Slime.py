import math
import tkinter
import numpy
import random
import time

genome = "ADH"

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
		s += genome[random.randint(0, 56653) % len(genome)]
	return s

class Slime:
	def __init__(self, name, scope, canv:tkinter.Canvas, field = (900, 900)):
		random.seed(time.time())
		self.x = random.randint(10, field[0] - 10)
		self.y = random.randint(10, field[1] - 10)
		self.vx = random.choice([-1, 1]) * 300
		self.vy = random.choice([-1, 1]) * 300
		self.angle = math.atan2(self.vy, self.vx)
		self.scope = scope
		
		self.name = name
		self.canv = canv
		self.color = "#" + ("%06x" % random.randint(0, 16777215))
		
		self.L = random.randint(10, 100)
		self.gene = rand_string(self.L)
		self.calattr()
	
	def calattr(self):
		#self.hp = 10*self.gene.count('H') + 1
		self.hp = 1000//(self.gene.count('H') + 1)
		self.defen = self.gene.count('D') + 1
		self.atk = self.gene.count('A') + 1
		#self.atk = 1000//(self.gene.count('A') + 1)
		#self.atk = 10**self.gene.count('A') if self.gene.count('A') > 50 else self.gene.count('A') + 1

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
	def attack(self, other):
		other.hp -= max(self.atk - other.defen, 0)
	def destroy(self):
		self.canv.delete(self.name)