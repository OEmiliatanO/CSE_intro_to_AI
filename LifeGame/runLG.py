import tkinter
import random
from Cell import Cell

shift = [(-1,-1),(-1,0),(-1,1),(0,-1), (0,1),(1,-1),(1,0),(1,1)]

def run(Game, canv, width, height, dt = 0.001):
	for x in range(width):
		for y in range(height):
			n = 0
			for dx, dy in shift:
				nexx = x + dx
				nexy = y + dy
				if nexx < 0 or nexx >= width:
					continue
				if nexy < 0 or nexy >= height:
					continue
				if Game[nexx][nexy].isalive:
					n += 1
			Game[x][y].detect(n)

	for x in range(width):
		for y in range(height):
			Game[x][y].transform(canv)
	"""
	for x in range(width):
		for y in range(height):
			n = 0
			for (dx, dy) in shift:
				nexx = x + dx
				print(x, nexx, "nx, dx =", dx)
				nexy = y + dy
				print(y, nexy, "ny, dy =", dy)
				if nexx < 0 or nexx >= width:
					continue
				if nexy < 0 or nexy >= height:
					continue
				if Game[nexx][nexy].isalive:
					print("nearby", x, y, nexx, nexy, "isalive, n=", n)
					n += 1
			print(x, y, " nearby:", n, " isalive:", Game[x][y].isalive)
	"""

	canv.after(int(dt * 1000), run, Game, canv, width, height)

def main():
	screen_size = (1000, 1000)
	scale = 10
	width = screen_size[0] // scale - 1
	height = screen_size[1] // scale - 1
	window = tkinter.Tk()
	window.title('life game')
	canv = tkinter.Canvas(window, bg = "black", width = screen_size[0], height = screen_size[1])
	canv.pack()

	Game = []
	for x in range(width):
		Game.append([])
		for y in range(height):
			Game[x].append(Cell(x, y))
			if random.randint(0, 100) > 50:
				Game[x][y].isalive = True

	run(Game, canv, width, height)
	window.mainloop()


if __name__ == "__main__":
	main()
