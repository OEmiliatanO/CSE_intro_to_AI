from Slime import Slime
from Slime import random_pick_gene
from Slime import E
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
	global wlim
	global w
	global val
	if this == None: return
	newslimes = slimes.copy()
	for i in atklist:
		this.attack(slimes[i])
		if slimes[i].hp <= 0:
			this.reproduction += 1
			slimes[i].destroy()
			for j in range(min(3, slimes[i].L//4)):
				new_slime = Slime("S" + str(num), scope, canv, wlim, w, val, screen_size)
				num += 1
				new_slime.L = slimes[i].L
				new_slime.gene = random_pick_gene([slimes[i]], new_slime.L)
				new_slime.calattr(wlim, w, val)
				new_slime.fill_attr_color()
			slimes.append(new_slime)
			slimes[i] = None

def merge(this, mergelist, slimes):
	global num
	global scope
	global screen_size
	global canv
	global wlim
	global w
	global val
	if this == None: return
	newsl = Slime("S" + str(num), scope, canv, wlim, w, val, screen_size)
	num += 1
	newL = 0
	for i in mergelist:
		newL += slimes[i].L
	newsl.L = newL
	newsl.gene = random_pick_gene([*map(lambda i: slimes[i], mergelist)], newL)
	newsl.calattr(wlim, w, val)
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
	global wlim
	global w
	global val
	if this == None: return
	if this.reproduction >= this.L:
		this.reproduction -= this.L
		new_slime = Slime("S"+str(num), scope, canv, wlim, w, val, screen_size)
		num += 1
		new_slime.L = this.L
		new_slime.gene = this.gene
		new_slime.calattr(wlim, w, val)
		new_slime.fill_attr_color()
		slimes.append(new_slime)

def mutation(this):
	global wlim, w, val
	if this == None: return
	# translocation
	if random.randint(0, 10000) < 20:
		random.shuffle((L:=[*this.gene]))
		this.gene = "".join(L)
		this.calattr(wlim, w, val)
	
	# point mutation
	"""
	for i in range(len(this.gene)):
		if random.randint(0, 10000) < 20:
			this.gene = this.gene[:i] + ("1" if this.gene[i] == "0" else "0") + this.gene[i+1:]
	"""

	# inversion mutation
	"""
	a = random.randint(0, 65532) % len(this.gene)
	b = random.randint(0, 65532) % len(this.gene)
	if a > b: a,b = b,a
	this.gene = this.gene[:a] + "".join(reversed([*this.gene[a:b+1]])) + this.gene[b+1:]
	"""

iter_cnt = 0
bestV, bestS = 0, ""
def run(slimes, canv, dt, field, turn_v = 40, margin = 100, sepDist = 30):
	global iter_cnt
	global bestV, bestS
	global flog
	global wlim
	global w
	global val
	iter_cnt += 1
	An = Dn = Hn = 0
	sumL = 0

	for i, this in enumerate(slimes):
		if this == None: continue
		An += this.atk
		Dn += this.defen
		Hn += this.hp
		sumL += this.L
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
			reproduce(this, slimes)
			mutation(this)
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
	for slime in slimes:
		totval = sum([(val[i] if slime.gene[i] == '1' else 0) for i in range(0, len(val))])
		if bestV < totval and sum([(w[i] if slime.gene[i] == '1' else 0) for i in range(0, len(w))]) <= wlim:
			bestV = totval
			bestS = slime.gene
	for this in slimes:
		this.fly(dt, field[0], field[1])
	#plt.clf()
	#hist = plt.hist([*sums])
	#plt.pause(1e-9)
	print("\033[F\033[F", end = '')
	print('best select   best val    iter_cnt')
	print(f'{bestS[:len(w)]}  {bestV:10d}         {iter_cnt:6d}')
	if iter_cnt % 100 == 0:
		flog.write(f'{bestS[:len(w)]} {bestV:10d}\n')
	if iter_cnt >= 10**5:
		print(f"\n\nthe best solution is {bestS[:len(w)]}, and the value is {bestV:10d}")
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
	global w
	global val
	global wlim
	n, wlim = input().split()
	n, wlim = int(n), int(wlim)
	w, val = [], []
	for x in input().split():
		w.append(int(x))
	for x in input().split():
		val.append(int(x))
	print(n, wlim)
	print(w)
	print(val)
	"""
	no mutation
	log 1 test1
	log 2 test2
	log 3 test3
	log 4 test4
	translocation mutation
	log 5 test1
	log 6 test2
	log 7 test3
	log 8 test4
	point mutation
	log 9  test1
	log 10 test2
	log 11 test3
	log 12 test4
	inversion mutation
	log 13 test1
	log 14 test2
	log 15 test3
	log 16 test4
	"""
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
	
	slimes = [Slime("S" + str(i), scope, canv, wlim, w, val, screen_size) for i in range(n)]
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
