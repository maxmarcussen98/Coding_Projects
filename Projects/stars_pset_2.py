import matplotlib.pyplot as plt

coin = {"H": 1, "T": -1}
a = "T H T T T H T T T T T H T T T H H H T T T T T H T T H T H T T T H T T H H H H H T H H H T H T H T T T T H T H T H H T H T H T H T H T H H T H H H T T T H T T H H T T H T H H H H H H H T T H T T H H H".split(" ")
b = []
for i in a:
    b.append(coin[i])
plt.plot(b)
plt.show()
