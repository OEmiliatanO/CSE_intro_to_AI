import math
import tkinter
import numpy
import random

class Bird:
	def __init__(self, name, scope, base_speed, field = (900, 900)):
		self.x = random.randint(10, field[0] - 10)
		self.y = random.randint(10, field[1] - 10)
		self.angle = random.uniform(0.0, 2.0 * math.pi)
		self.vx = math.cos(self.angle)
		self.vy = math.sin(self.angle)
<<<<<<< HEAD
=======
		#self.base_speed = random.randint(200, 500)
		self.base_speed = base_speed
		#self.scope = numpy.random.normal(100, 60)
>>>>>>> ab3e08b4b126bd00275774d0a88c5764508c0b74
		self.scope = scope
		self.name = name
		self.color = "#" + ("%06x" % random.randint(0, 16777215))
		
	def draw(self, canv, scale = 11):
		arx = self.x + scale * math.cos(self.angle)
		ary = self.y + scale * math.sin(self.angle)
		canv.create_line(self.x, self.y, arx, ary, fill = self.color, arrow='last', tag = self.name)

	def fly(self, canv, dt, boundaryx, boundaryy):
		self.vx = self.base_speed * math.cos(self.angle)
		self.vy = self.base_speed * math.sin(self.angle)
		self.x += self.vx * dt
		self.y += self.vy * dt
		self.x %= boundaryx
		self.y %= boundaryy
		canv.delete(self.name)
		self.draw(canv)
	
	def dist(self, other):
		return math.sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))
