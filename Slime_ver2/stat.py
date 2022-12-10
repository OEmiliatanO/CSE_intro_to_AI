import matplotlib.pyplot as plt
import sys

def main():
    for num in range(1, 15):
        print(f"processing log{num}...")
        f = open(f"log{num}", "r")

        A = []
        H = []
        D = []
        X = []
        while True:
            l = [*f.readline().split()]
            l = [float(x) for x in l]
            A.append(l[0])
            H.append(l[1])
            D.append(l[2])
            X.append(l[3])
            if X[-1] >= 100000:
                break

        plt.figure()
        plt.plot(X, A, label = 'A', color = 'red')
        plt.plot(X, H, label = 'H', color = 'green')
        plt.plot(X, D, label = 'D', color = 'blue')
        plt.legend(loc = 'best')
        plt.savefig(f"log{num}.fig.png")
        print("saved the fig.\n")
        f.close()

if __name__ == "__main__":
    main()
