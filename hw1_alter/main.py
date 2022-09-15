from Bird import Bird
import tkinter
import random
import numpy
import math

def sep(this, others, miniDist = 60):
	dx, dy = 0, 0
	for other in others:
		if this.dist(other) < miniDist:
			dx += (this.x - other.x)
			dy += (this.y - other.y)
	this.vx += dx * 0.05
	this.vy += dy * 0.05

def alig(this, others):
	avg_vx = 0
	avg_vy = 0
	for other in others:
		avg_vx += other.vx
		avg_vy += other.vy
	avg_vx /= len(others)
	avg_vy /= len(others)
	this.vx += (avg_vx - this.vx) * 0.05
	this.vy += (avg_vy - this.vy) * 0.05

def cohen(this, others):
	avg_x = 0
	avg_y = 0
	for other in others:
		avg_x += other.x
		avg_y += other.y
	avg_x /= len(others)
	avg_y /= len(others)
	this.vx += (avg_x - this.x) * 0.0005
	this.vy += (avg_y - this.y) * 0.0005

def bias(this):
	bias_v = 0.001 + random.uniform(0, 0.01)
	if numpy.random.randint(0, 100) >= 80:
		this.vx = (1 - bias_v) * this.vx + bias_v * random.choice([-1, 1])
		this.vy = (1 - bias_v) * this.vy + bias_v * random.choice([-1, 1])

def run(birds, canv, dt, field):
	for this in birds:
		insight = []
		for other in birds:
			if this.name == other.name:
				continue
			elif 0 < this.dist(other) < this.scope:
				insight.append(other)

		if len(insight) == 0:
			this.vx = this.vx * 0.99
			this.vy = this.vy * 0.99
		else:
			sep(this, insight)
			alig(this, insight)
			cohen(this, insight)
			bias(this)
			turn_v = 100
			margin = 500
			if this.x < margin:
				this.vx += turn_v
				print(this.name + " cross left margin")
				print(this.vx, this.vy)
			if this.y < margin:
				this.vy += turn_v
				print(this.name + " cross top margin")
				print(this.vx, this.vy)
			if this.x > field[0] - margin:
				this.vx -= turn_v
				print(this.name + " cross right margin")
				print(this.vx, this.vy)
			if this.y > field[1] - margin:
				this.vy -= turn_v
				print(this.name + " cross bottom margin")
				print(this.vx, this.vy)

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
