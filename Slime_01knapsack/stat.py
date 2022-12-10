import matplotlib.pyplot as plt
import sys

def main():
	for num in range(5, 9):
		print(f"processing log{num}...")
		f = open(f"log{num}", "r")
		ansf = open(f"ans{(num-4)}", "r")
		
		S = []
		val = []
		X = []
		ans = int(ansf.readline())
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
		ans = [ans] * len(X)
		plt.figure()
		plt.plot(X, val, label = 'A', color = 'red')
		plt.plot(X, ans, label = 'ans', color = 'blue')
		plt.legend(loc = 'best')
		plt.savefig(f"log{num}.fig.png")
		print("saved the fig.\n")
		f.close()

if __name__ == "__main__":
	main()
