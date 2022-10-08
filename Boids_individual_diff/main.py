from Bird import Bird
import tkinter
import random
import numpy
import math

def sep(this, dx, dy, sepW = 0.08, offset = 0):
	this.vx += dx * (sepW + offset)
	this.vy += dy * (sepW + offset)

def alig(this, avg_vx, avg_vy, aligW = 0.2, offset = 0):
	this.vx += (avg_vx - this.vx) * (aligW + offset)
	this.vy += (avg_vy - this.vy) * (aligW + offset)

def cohen(this, avg_x, avg_y, cohenW = 0.04, offset = 0):
	this.vx += (avg_x - this.x) * (cohenW + offset)
	this.vy += (avg_y - this.y) * (cohenW + offset)

def bias(this, bias_v = 0.04):
	if numpy.random.randint(0, 100) >= 80:
		this.vx = (1 - bias_v) * this.vx + bias_v * random.choice([-1, 1])
		this.vy = (1 - bias_v) * this.vy + bias_v * random.choice([-1, 1])

def run(birds, canv, dt, field, scale_sep, scale_alig, scale_cohen, turn_v = 40, margin = 100, sepDist = 20):
	for this in birds:
		avg_vx, avg_vy, avg_x, avg_y, dx, dy, cnt = 0, 0, 0, 0, 0, 0, 0
		for other in birds:
			dist = this.dist(other)
			if 0 <= dist < this.scope:
				avg_vx += other.vx
				avg_vy += other.vy
				avg_x += other.x
				avg_y += other.y
				cnt += 1
				if dist <= sepDist and other.name != this.name:
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
			
			#print(scale_sep.get())
			sep(this, dx, dy, sepW = scale_sep.get())
			#sep(this, dx, dy, sepW = 0.4, offset = scale_sep.get())
			alig(this, avg_vx, avg_vy, aligW = scale_alig.get())
			#alig(this, avg_vx, avg_vy, aligW = 0.2, offset = scale_alig.get())
			cohen(this, avg_x, avg_y, cohenW = scale_cohen.get())
			#cohen(this, avg_x, avg_y, cohenW = 0.03, offset = scale_cohen.get())
			bias(this, bias_v = 0.3)
			
			if this.x < margin:
				this.vx += turn_v
			if this.y < margin:
				this.vy += turn_v
			if this.x > field[0] - margin:
				this.vx -= turn_v
			if this.y > field[1] - margin:
				this.vy -= turn_v
			

	for this in birds:
		this.fly(canv, dt, field[0], field[1])

	canv.after(int(dt * 1000), run, birds, canv, dt, field, scale_sep, scale_alig, scale_cohen)

def main():
	screen_size = (1900, 950)
	n = 50
	scope = 70
	minspeed = 400
	maxspeed = 600
	dt = 0.01#s
	window = tkinter.Tk()
	window.title("Boids")
	
	canv = tkinter.Canvas(window, bg = "black", width = screen_size[0], height = screen_size[1])
	canv.pack()
	
	sep_v = tkinter.DoubleVar()
	align_v = tkinter.DoubleVar()
	cohen_v = tkinter.DoubleVar()
	
	scale_sep = tkinter.Scale(window, label = "separation", variable = sep_v, orient = tkinter.HORIZONTAL, length = screen_size[0] // 3 - 30, resolution = 0.01,from_ = 0.0, to = 1.0)
	scale_sep.set(0.08)
	scale_sep.pack(side = tkinter.LEFT)

	scale_alig = tkinter.Scale(window, label = "alignment", variable = align_v, orient = tkinter.HORIZONTAL, length = screen_size[0] // 3 - 30, resolution = 0.01, from_ = 0.0, to = 1.0)
	scale_alig.set(0.2)
	scale_alig.pack(side = tkinter.LEFT)

	scale_cohen = tkinter.Scale(window, label = "coherence", variable = cohen_v, orient = tkinter.HORIZONTAL, length = screen_size[0] // 3 - 30, resolution = 0.01, from_ = 0.0, to = 1.0)
	scale_cohen.set(0.04)
	scale_cohen.pack(side = tkinter.LEFT)
	
	#birds = [Bird("B" + str(i), scope, minspeed, maxspeed, screen_size) for i in range(n)]
	birds = [Bird("B" + str(i), scope = random.randint(40, 100), minspeed = random.randint(200, 250), maxspeed = random.randint(300, 1000), field = screen_size) for i in range(n)]
	run(birds, canv, dt, screen_size, scale_sep, scale_alig, scale_cohen)
	window.mainloop()

if __name__ == "__main__":
	main()
