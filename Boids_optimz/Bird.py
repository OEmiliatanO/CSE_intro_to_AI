import math
import tkinter
import numpy
import random
import time

class Bird:
	def __init__(self, name, scope, field = (900, 900)):
		random.seed(time.time())
		self.x = random.randint(10, field[0] - 10)
		self.y = random.randint(10, field[1] - 10)
		self.vx = random.choice([-1, 1]) * 300
		self.vy = random.choice([-1, 1]) * 300
		self.angle = math.atan2(self.vy, self.vx)
		self.scope = scope
		self.name = name
		self.color = "#" + ("%06x" % random.randint(0, 16777215))
		
	def draw(self, canv, scale = 11):
		self.angle = math.atan2(self.vy, self.vx)
		arx = self.x + scale * math.cos(self.angle)
		ary = self.y + scale * math.sin(self.angle)
		canv.create_line(self.x, self.y, arx, ary, fill = self.color, arrow='last', tag = self.name)

	def fly(self, canv, dt, boundaryx, boundaryy):
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
		canv.delete(self.name)
		self.draw(canv)
	
	def dist(self, other):
		return math.sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))
