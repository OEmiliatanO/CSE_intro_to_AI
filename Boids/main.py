from Bird import Bird
import tkinter
import random
import numpy
import math

def sep(this, others):
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
	this.angle += 0.09 * (avg_ang - this.angle)

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

		if len(insight) > 0:
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
	base_speed = 300
	dt = 0.01#s
	window = tkinter.Tk()
	window.title("Boids")
	
	canv = tkinter.Canvas(window, bg = "black", width = screen_size[0], height = screen_size[1])
	canv.pack()
	
<<<<<<< HEAD
=======
	birds = [Bird("B" + str(i), scope, base_speed, screen_size) for i in range(n)]
>>>>>>> ab3e08b4b126bd00275774d0a88c5764508c0b74
	run(birds, canv, dt, screen_size)
	window.mainloop()

if __name__ == "__main__":
	main()
