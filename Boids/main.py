from Bird import Bird
import tkinter
import random
import numpy
import math

def sep(this, avg_x, avg_y):
	this.angle -= 0.014 * math.atan2(avg_y - this.y, avg_x - this.x)

def alig(this, avg_ang):
	this.angle += 0.86 * (avg_ang - this.angle)

def cohen(this, avg_x, avg_y):
	this.angle -= 0.034 * (math.atan2(avg_y - this.y, avg_x - this.x))

def bias(this):
	bias_v = 0.07
	if random.randint(0, 100) > 80:
		this.angle += bias_v * random.choice([-1, 1])

def run(birds, canv, dt, field):
	for this in birds:
		cnt = 0
		avg_x = 0
		avg_y = 0
		avg_ang = 0
		for other in birds:
			if this == other:
				continue
			elif 0 < this.dist(other) < this.scope:
				cnt += 1
				avg_x += other.x
				avg_y += other.y
				avg_ang += other.angle

		if cnt > 0:
			avg_x /= cnt
			avg_y /= cnt
			avg_ang /= cnt
			sep(this, avg_x, avg_y)
			alig(this, avg_ang)
			cohen(this, avg_x, avg_y)
			bias(this)
	
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
