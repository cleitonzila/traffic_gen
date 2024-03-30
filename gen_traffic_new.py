import random
from scipy.stats import poisson, expon
import numpy as np

# Inicialização de parâmetros
N = 12
L = 34
S = 16
H = 10
req_Max = 6
K = 100

M = int(input("Digite o tamnho desejado da simulacao: "))

# Inicialização de listas e matrizes
t_req = [0] * (M + 1)
t_hold = [0] * M
t_exp = [0] * M
hops = np.zeros((N, N))
link = np.zeros((N, N))
lp_size = [0] * M
source = [0] * M
dest = [0] * M

# Sementes e distribuições
seed1 = 123
seed2 = 125
random.seed(seed2)
generator = random.Random(seed1)
mu = 1 / H
hold_time = lambda: int(K * expon.rvs(scale=1/mu, size=1)[0]) + 1
traff_dist = lambda: random.randint(1, req_Max)

# Solicitação de input do usuário como uma string e conversão para uma lista de inteiros
input_str = input("Digite os valores de tráfego desejados: ")
traffs = [int(x) for x in input_str.split(", ")]

for traff in traffs:
    inter_arr = H / traff
    next_arr = lambda: poisson.rvs(K * inter_arr, size=1)[0] + 1

    with open(f"traffic_jpn12_testing_slicing{traff}.txt", "w") as ofs1:
        max_hold = 0
        t_req[0] = 0

        for i in range(M):
            temp1 = hold_time()
            t_hold[i] = temp1
            if max_hold < t_hold[i]:
                max_hold = t_hold[i]

            arr_int = next_arr()
            lp_size[i] = traff_dist()
            source[i] = random.randint(0, N-1)
            dest[i] = random.randint(0, N-1)

            while source[i] == dest[i]:
                dest[i] = random.randint(0, N-1)

            t_exp[i] = t_req[i] + t_hold[i]
            ofs1.write(f"{i}: {source[i]} {dest[i]} {lp_size[i]} {t_req[i]} {t_hold[i]}\n")

            t_req[i + 1] = t_req[i] + arr_int
