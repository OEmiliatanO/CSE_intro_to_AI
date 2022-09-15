from Bird import Bird
import tkinter
import random
import numpy
import math

def sep(this, others):
	"""
	d = 1000000000
	nearest = None
	for other in others:
		if this.dist(other) < d:
			nearest = other
	if nearest != None:
		dangle = math.atan2(nearest.y - this.y, nearest.x - this.x)
		this.angle -= 0.013 * dangle
	"""
	avg_x = 0
	avg_y = 0
	for other in others:
		avg_x += other.x
		avg_y += other.y
	avg_x /= len(others)
	avg_y /= len(others)
	this.angle -= 0.013 * math.atan2(avg_y - this.y, avg_x - this.x)

def alig(this, others):
	avg_ang = 0
	for other in others:
		avg_ang += other.angle
	avg_ang /= len(others)
	this.angle += 0.5 * (avg_ang - this.angle)

def cohen(this, others):
	avg_x = 0
	avg_y = 0
	for other in others:
		avg_x += other.x
		avg_y += other.y
	avg_x /= len(others)
	avg_y /= len(others)
	this.angle -= 0.07 * math.atan2(avg_y, avg_x)

def run(birds, canv, dt, field):
	for this in birds:
		insight = []
		for other in birds:
			if this == other:
				continue
			elif 0 < this.dist(other) < this.scope:
				insight.append(other)

		if insight == None or len(insight) == 0:
			this.ax = -this.vx * 0.8
			this.ay = -this.vy * 0.8
		else:
			sep(this, insight)
			alig(this, insight)
			cohen(this, insight)

	for this in birds:
		this.fly(canv, dt, field[0], field[1])

	canv.after(int(dt * 1000), run, birds, canv, dt, field)

def main():
	screen_size = (1900, 1000)
	n = 100
	scope = 30
	dt = 0.01#s
	window = tkinter.Tk()
	window.title("Boids")
	
	canv = tkinter.Canvas(window, bg = "black", width = screen_size[0], height = screen_size[1])
	canv.pack()
	
	birds = [Bird("B" + str(i), scope, screen_size) for i in range(n)]
	run(birds, canv, dt, screen_size)
	window.mainloop()

if __name__ == "__main__":
	main()
