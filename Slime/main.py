from Slime import Slime
import tkinter
import random
import numpy
import math

def sep(this, dx, dy, sepW = 0.08):
	this.vx += dx * sepW
	this.vy += dy * sepW

def alig(this, avg_vx, avg_vy, aligW = 0.2):
	this.vx += (avg_vx - this.vx) * aligW
	this.vy += (avg_vy - this.vy) * aligW

def cohen(this, avg_x, avg_y, cohenW = 0.04):
	this.vx += (avg_x - this.x) * cohenW
	this.vy += (avg_y - this.y) * cohenW

def bias(this, bias_v = 0.04):
	if numpy.random.randint(0, 100) >= 80:
		this.vx = (1 - bias_v) * this.vx + bias_v * random.choice([-1, 1])
		this.vy = (1 - bias_v) * this.vy + bias_v * random.choice([-1, 1])

def run(slimes, canv, dt, field, turn_v = 40, margin = 100, sepDist = 30):
	for this in slimes:
		avg_vx, avg_vy, avg_x, avg_y, dx, dy, cnt = 0, 0, 0, 0, 0, 0, 0
		for other in slimes:
			dist = this.dist(other)
			if 0 < dist < this.scope:
				avg_vx += other.vx
				avg_vy += other.vy
				avg_x += other.x
				avg_y += other.y
				cnt += 1
				if dist <= sepDist:
					dx += (this.x - other.x)
					dy += (this.y - other.y)

		if cnt == 0:
			this.vx = this.vx * 0.99
			this.vy = this.vy * 0.99
		else:
			avg_vx /= cnt
			avg_vy /= cnt
			avg_x /= cnt
			avg_y /= cnt

			sep(this, dx, dy, sepW = 0.4)
			alig(this, avg_vx, avg_vy)
			cohen(this, avg_x, avg_y, cohenW = 0.03)
			bias(this, bias_v = 0.1)
			if this.x < margin:
				this.vx += turn_v
			if this.y < margin:
				this.vy += turn_v
			if this.x > field[0] - margin:
				this.vx -= turn_v
			if this.y > field[1] - margin:
				this.vy -= turn_v

	for this in slimes:
		this.fly(canv, dt, field[0], field[1])

	canv.after(int(dt * 1000), run, slimes, canv, dt, field)

def main():
	screen_size = (1900, 1000)
	n = 200
	scope = 65
	dt = 0.01#s
	window = tkinter.Tk()
	window.title("Boids")
	
	canv = tkinter.Canvas(window, bg = "black", width = screen_size[0], height = screen_size[1])
	canv.pack()
	
	slimes = [Slime("B" + str(i), scope, screen_size) for i in range(n)]
	run(slimes, canv, dt, screen_size)
	window.mainloop()

if __name__ == "__main__":
	main()
