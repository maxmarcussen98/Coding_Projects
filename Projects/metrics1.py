import numpy as np

x = [1, 2, 3]

probs = [0.2, 0.5, 0.3]

mean_list = []
naive_var_list = []
sample_var_list = []

n=1000

np.random.seed(1)

for i in range(0, 100):
    rand_list = np.random.choice(x, n, p=list(probs))
    mean = np.mean(rand_list)
    naive_var = 0
    sample_var = 0
    for i in range(0, n):
        sample_var += (rand_list[i] - mean) ** 2
        naive_var += (rand_list[i] - mean) ** 2
    naive_var = naive_var / n
    sample_var = sample_var / (n-1)
    mean_list.append(mean)
    naive_var_list.append(naive_var)
    sample_var_list.append(sample_var)

print("Sample average across 100 draws: " + str(np.mean(mean_list)))
print("Naive variance across 100 draws: " + str(np.mean(naive_var_list)))
print("Sample variance across 100 draws: " + str(np.mean(sample_var_list)))