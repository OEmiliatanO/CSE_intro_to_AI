from Bird import Bird
import tkinter
import random
import numpy
import math

def sep(this, others, minidist = 30):
	avg_x = 0
	avg_y = 0
	n = 0
	for other in others:
		if this.dist(other) < minidist:
			avg_x += other.x
			avg_y += other.y
			n += 1
	if n == 0: return
	avg_x /= n
	avg_y /= n
	dd = math.atan2(avg_y - this.y, avg_x - this.x)
	if dd < 0: dd += 2*math.pi
	d = this.angle - dd
	#print(this.name, "sep d:", d)
	this.angle += 0.005 * d

def alig(this, others):
	avg_ang = 0
	for other in others:
		avg_ang += other.angle
	avg_ang /= len(others)
	#print(this.name, "avg_ang:", avg_ang)
	this.angle -= 0.07 * (this.angle - avg_ang)

def cohen(this, others):
	avg_x = 0
	avg_y = 0
	for other in others:
		avg_x += other.x
		avg_y += other.y
	avg_x /= len(others)
	avg_y /= len(others)
	#print("avg_x, avg_y: ", avg_x, avg_y)
	#print(this.name, "angle(before):", this.angle)
	dd = math.atan2(avg_y - this.y, avg_x -this.x)
	if dd < 0: dd += 2*math.pi
	#print("dd:", dd)
	d = this.angle - dd
	#print(this.name, "x:", this.x, ", y", this.y)
	#print(this.name, "cohen d:", d)
	this.angle -= 0.015 * d
	#print(this.name, "angle:", this.angle)

def run(birds, canv, dt, field):
	#print(birds[0].angle)
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
	scope = 70
	dt = 0.01#s
	window = tkinter.Tk()
	window.title("Boids")
	
	canv = tkinter.Canvas(window, bg = "black", width = screen_size[0], height = screen_size[1])
	canv.pack()
	
	birds = [Bird("B" + str(i), scope, 300, screen_size) for i in range(n)]
	run(birds, canv, dt, screen_size)
	window.mainloop()

if __name__ == "__main__":
	main()
