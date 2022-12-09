from Slime import Slime
from Slime import random_pick_gene
import tkinter
import random
import numpy
import math
import matplotlib.pyplot as plt
import os

def sep(this, dx, dy, sepW = 0.08):
	if this == None: return
	this.vx += dx * sepW
	this.vy += dy * sepW

def alig(this, avg_vx, avg_vy, aligW = 0.2):
	if this == None: return
	this.vx += (avg_vx - this.vx) * aligW
	this.vy += (avg_vy - this.vy) * aligW

def cohen(this, avg_x, avg_y, cohenW = 0.03):
	if this == None: return
	this.vx += (avg_x - this.x) * cohenW
	this.vy += (avg_y - this.y) * cohenW

def bias(this, bias_v = 0.04):
	if this == None: return
	if numpy.random.randint(0, 100) >= 50:
		this.vx = (1 - bias_v) * this.vx + bias_v * random.choice([-1, 1])
		this.vy = (1 - bias_v) * this.vy + bias_v * random.choice([-1, 1])

def atk(this, atklist, slimes):
	global num
	global scope
	global screen_size
	global canv
	if this == None: return
	newslimes = slimes.copy()
	for i in atklist:
		this.attack(slimes[i])
		if slimes[i].hp <= 0:
			this.reproduction += 1
			slimes[i].destroy()
			
			for j in range(min(2, slimes[i].L//2)):
				new_slime = Slime("S" + str(num), scope, canv, screen_size)
				num += 1
				new_slime.L = slimes[i].L//(min(2, slimes[i].L//2))
				new_slime.gene = random_pick_gene([slimes[i]], new_slime.L)
				new_slime.calattr()
				new_slime.fill_attr_color()
			slimes.append(new_slime)
			
			slimes[i] = None

def merge(this, mergelist, slimes):
	global num
	global scope
	global screen_size
	global canv
	if this == None: return
	newsl = Slime("S" + str(num), scope, canv, screen_size)
	num += 1
	newL = 0
	for i in mergelist:
		newL += slimes[i].L
	newsl.L = newL
	newsl.gene = random_pick_gene([*map(lambda i: slimes[i], mergelist)], newL)
	newsl.calattr()
	newsl.fill_attr_color()
	for i in mergelist:
		slimes[i].destroy()
		slimes[i] = None

	slimes.append(newsl)

def reproduce(this, slimes):
	global num
	global scope
	global screen_size
	global canv
	if this == None: return
	if this.reproduction >= this.L:
		this.reproduction -= this.L
		new_slime = Slime("S"+str(num), scope, canv, screen_size)
		num += 1
		new_slime.L = this.L
		new_slime.gene = this.gene
		new_slime.calattr()
		new_slime.fill_attr_color()
		slimes.append(new_slime)

iter_cnt = 0
def run(slimes, canv, dt, field, turn_v = 40, margin = 100, sepDist = 30):
	global iter_cnt
	global flog
	iter_cnt += 1
	An = Dn = Hn = 0
	sumL = 0
	sums = ""

	for i, this in enumerate(slimes):
		if this == None: continue
		An += this.gene.count('A')
		Dn += this.gene.count('D')
		Hn += this.gene.count('H')
		sumL += this.L
		sums += this.gene
		avg_vx, avg_vy, avg_x, avg_y, dx, dy, cnt = 0, 0, 0, 0, 0, 0, 0
		atklist = []
		mergelist = []
		for j, other in enumerate(slimes):
			if other == None: continue
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
				if sepDist - 25 <= dist <= sepDist - 10:
					atklist.append(j)
				if dist < sepDist - 25 and this.hp >= other.hp:
					mergelist.append(j)

		if cnt == 0:
			this.vx = this.vx * 0.99
			this.vy = this.vy * 0.99
		else:
			avg_vx /= cnt
			avg_vy /= cnt
			avg_x /= cnt
			avg_y /= cnt

			sep(this, dx, dy, sepW = 1)
			#alig(this, avg_vx, avg_vy)
			#cohen(this, avg_x, avg_y, cohenW = 0.03)
			atk(this, random.sample(atklist, min(random.randint(0, 10), len(atklist))), slimes)
			mergelist.append(i)
			merge(this, mergelist, slimes)
			#reproduce(this, slimes)
			bias(this, bias_v = 0.1)
			if this == None: continue
			if this.x < margin:
				this.vx += turn_v
			if this.y < margin:
				this.vy += turn_v
			if this.x > field[0] - margin:
				this.vx -= turn_v
			if this.y > field[1] - margin:
				this.vy -= turn_v
	
	slimes = list(filter(lambda x: x!=None, slimes))
	for this in slimes:
		this.fly(dt, field[0], field[1])
	#plt.clf()
	#hist = plt.hist([*sums])
	#plt.pause(1e-9)
	print("\033[F\033[F\033[F", end = '')
	print(f'     A      H      D')
	print(f'{An:6d} {Hn:6d} {Dn:6d}     {(sumL/len(slimes)):6.3f}     {(len(slimes)):4d}             ')
	print(f'{(An/sumL):6.3f} {(Hn/sumL):6.3f} {(Dn/sumL):6.3f} {iter_cnt:6d}                                       ')

	if iter_cnt % 100 == 0:
		flog.write(f"{(An/sumL):6.3f} {(Hn/sumL):6.3f} {(Dn/sumL):6.3f} {iter_cnt:6d} {(len(slimes)):4d}\n")
	if iter_cnt >= 10**5:
		quit_win(None)

	canv.after(int(dt * 1000), run, slimes, canv, dt, field)

def quit_win(event):
	global flog
	print("quit")
	flog.close()
	exit(0)

def main():
	global screen_size
	global scope
	global num
	global canv
	global flog
	logn = 1
	log = "log"
	while os.path.isfile(log + str(logn)):
		logn += 1
	log += str(logn)
	flog = open(log, 'w+')

	screen_size = (1900, 1000)
	scope = 65
	n = 100
	num = n
	dt = 0.01#s
	window = tkinter.Tk()
	window.title("Slimes")
	window.bind("<Control-c>", quit_win)
	
	canv = tkinter.Canvas(window, bg = "black", width = screen_size[0], height = screen_size[1])
	canv.pack()
	
	slimes = [Slime("S" + str(i), scope, canv, screen_size) for i in range(n)]
	"""
	ss = ""
	for s in slimes:
		ss += s.gene
	plt.hist([*ss])
	plt.show()
	"""
	print('\n\n')
	run(slimes, canv, dt, screen_size)
	window.mainloop()

if __name__ == "__main__":
	main()
