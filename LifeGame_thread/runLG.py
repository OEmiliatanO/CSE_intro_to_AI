import tkinter
import random
import sys
import threading
from Cell import Cell

shift = [(-1,-1),(-1,0),(-1,1),(0,-1), (0,1),(1,-1),(1,0),(1,1)]

def check(Game, row, height, width):
	for i in range(min(row[0], height), min(row[1], height)):
		for j in range(width):
			n = 0
			for di, dj in shift:
				nexi = i + di
				nexj = j + dj
				if nexi < 0 or nexi >= height:
					continue
				if nexj < 0 or nexj >= width:
					continue
				if Game[nexi][nexj].isalive:
					n += 1
			Game[i][j].detect(n)

threadn = 5
def run(Game, canv, width, height, dt = 0.01):
	heightd = height // threadn
	threads = []
	for n in range(threadn+1):
		threads.append(threading.Thread(target = check, args = (Game, (heightd * n, heightd * (n + 1)), height, width)))
		threads[n].start()
	for n in range(threadn+1):
		threads[n].join()

	for i in range(height):
		for j in range(width):
			Game[i][j].transform(canv)

	canv.after(int(dt * 1000), run, Game, canv, width, height)

def main():
	screen_size = (1920, 1080)
	scale = 10
	width = screen_size[0] // scale - 1
	height = screen_size[1] // scale - 1
	window = tkinter.Tk()
	window.title('life game')
	scrollbar = tkinter.Scrollbar(window)
	scrollbar.pack(side = 'right', fill = 'y')
	canv = tkinter.Canvas(window, bg = "black", width = screen_size[0], height = screen_size[1])
	canv.pack()

	Game = []
	if sys.argv[1] == "random":
		for i in range(height):
			Game.append([])
			for j in range(width):
				Game[i].append(Cell(j, i))
				if random.randint(0, 100) > 50:
					Game[i][j].isalive = True
	else:
		f = open(sys.argv[1], 'r')
		for i in range(height):
			Game.append([])
			s = f.readline()
			for j in range(width):
				Game[i].append(Cell(j, i))
				if j >= len(s):
					continue
				if s[j] == '1':
					Game[i][j].isalive = True
		f.close()

	for i in range(height):
		for j in range(width):
			Game[i][j].draw(canv)
	"""
	for i in range(height):
		for j in range(width):
			n = 0
			for di, dj in shift:
				nexi = i + di
				nexj = j + dj
				if nexi < 0 or nexi >= height:
					continue
				if nexj < 0 or nexj >= width:
					continue
				if Game[nexi][nexj].isalive:
					n += 1
			Game[i][j].detect(n)
			if Game[i][j].isalive:
				print(i, j, n)
				print(i, j, Game[i][j].nexAlive)
	"""
	run(Game, canv, width, height)
	window.mainloop()


if __name__ == "__main__":
	main()
