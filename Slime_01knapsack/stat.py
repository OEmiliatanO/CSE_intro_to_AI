import matplotlib.pyplot as plt
import sys

def main():
	for num in range(1, 9):
		print(f"processing log{num}...")
		f = open(f"log{num}", "r")
		
		S = []
		val = []
		X = []
		while True:
			l = [*f.readline().split()]
			if len(l) == 1:
				X.append((len(X) + 1) * 100)
				val.append(int(l[0]))
			elif len(l) == 2:
				X.append((len(X) + 1) * 100)
				S.append(l[0])
				val.append(int(l[1]))
			else:
				break

		plt.figure()
		plt.plot(X, val, label = 'A', color = 'red')
		plt.legend(loc = 'best')
		plt.savefig(f"log{num}.fig.png")
		print("saved the fig.\n")
		f.close()

if __name__ == "__main__":
	main()
