import matplotlib.pyplot as plt
import sys

def main():
    for num in range(1, 10):
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
        plt.plot(X, A, label = 'A')
        plt.plot(X, H, label = 'H')
        plt.plot(X, D, label = 'D')
        plt.legend(loc = 'best')
        plt.savefig(f"log{num}.fig.png")
        print("saved the fig.\n")
        f.close()

if __name__ == "__main__":
    main()
