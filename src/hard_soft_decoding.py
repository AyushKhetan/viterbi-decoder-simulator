import random
import math
import matplotlib.pyplot as plt

# ---------------- TRELLIS ----------------
trellis = {
    (0, 0): (0, (0, 0)),
    (0, 1): (2, (1, 1)),
    (1, 0): (0, (0, 1)),
    (1, 1): (2, (1, 0)),
    (2, 0): (1, (1, 1)),
    (2, 1): (3, (0, 0)),
    (3, 0): (1, (1, 0)),
    (3, 1): (3, (0, 1)),
}

# ---------------- ENCODER ----------------
def encode(bits):
    state = [0, 0]
    output = []
    for b in bits:
        g1 = b ^ state[0]
        g2 = b ^ state[0] ^ state[1]
        output.append((g1, g2))
        state = [b] + state[:-1]
    return output

# ---------------- HARD CHANNEL ----------------
def add_bsc_noise(encoded, p):
    noisy = []
    for b1, b2 in encoded:
        nb1 = b1 ^ (random.random() < p)
        nb2 = b2 ^ (random.random() < p)
        noisy.append((int(nb1), int(nb2)))
    return noisy

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

# ---------------- SOFT CHANNEL ----------------
def map_to_signal(encoded):
    return [(1 if b1 == 0 else -1, 1 if b2 == 0 else -1) for b1, b2 in encoded]

def add_awgn(signal, sigma):
    noisy = []
    for s1, s2 in signal:
        r1 = s1 + random.gauss(0, sigma)
        r2 = s2 + random.gauss(0, sigma)
        noisy.append((r1, r2))
    return noisy

def euclidean(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

# ---------------- SIGMA FROM p ----------------
def Q(x):
    return 0.5 * math.erfc(x / math.sqrt(2))

def sigma_from_p(p):
    """
    Solve p = Q(1/sigma) numerically using binary search
    """
    low, high = 0.01, 5.0

    for _ in range(50):  # sufficient precision
        mid = (low + high) / 2
        val = Q(1 / mid)

        if val > p:
            high = mid
        else:
            low = mid

    return (low + high) / 2

# ---------------- VITERBI HARD ----------------
def viterbi_hard(received):
    PM = {0: 0, 1: float('inf'), 2: float('inf'), 3: float('inf')}
    paths = {0: [], 1: [], 2: [], 3: []}

    for t in range(len(received)):
        new_PM = {s: float('inf') for s in range(4)}
        new_paths = {s: [] for s in range(4)}

        for s in range(4):
            if PM[s] == float('inf'):
                continue
            for inp in [0,1]:
                ns, out = trellis[(s, inp)]
                metric = PM[s] + hamming(out, received[t])
                if metric < new_PM[ns]:
                    new_PM[ns] = metric
                    new_paths[ns] = paths[s] + [inp]

        PM, paths = new_PM, new_paths

    return paths[min(PM, key=PM.get)]

# ---------------- VITERBI SOFT ----------------
def viterbi_soft(received):
    PM = {0: 0, 1: float('inf'), 2: float('inf'), 3: float('inf')}
    paths = {0: [], 1: [], 2: [], 3: []}

    for t in range(len(received)):
        new_PM = {s: float('inf') for s in range(4)}
        new_paths = {s: [] for s in range(4)}

        for s in range(4):
            if PM[s] == float('inf'):
                continue
            for inp in [0,1]:
                ns, out = trellis[(s, inp)]

                expected = (1 if out[0]==0 else -1,
                            1 if out[1]==0 else -1)

                metric = PM[s] + euclidean(received[t], expected)

                if metric < new_PM[ns]:
                    new_PM[ns] = metric
                    new_paths[ns] = paths[s] + [inp]

        PM, paths = new_PM, new_paths

    return paths[min(PM, key=PM.get)]

# ---------------- EXPERIMENT ----------------
p = 0.15
def run_experiment():
    lengths = [10, 25, 50, 100, 200, 500, 1000]
    total_bits = 100000

    sigma = sigma_from_p(p)

    print(f"\nUsing p = {p} → sigma ≈ {sigma:.3f}")

    hard_res = []
    soft_res = []

    for L in lengths:
        trials = total_bits // L

        err_h, err_s = 0, 0
        bits = 0

        for _ in range(trials):
            msg = [random.randint(0,1) for _ in range(L)]
            enc = encode(msg)

            # HARD
            r_h = add_bsc_noise(enc, p)
            dec_h = viterbi_hard(r_h)

            # SOFT
            sig = map_to_signal(enc)
            r_s = add_awgn(sig, sigma)
            dec_s = viterbi_soft(r_s)

            err_h += sum(m != d for m,d in zip(msg, dec_h))
            err_s += sum(m != d for m,d in zip(msg, dec_s))
            bits += L

        hard_res.append(100 * err_h / bits)
        soft_res.append(100 * err_s / bits)

        print(f"L={L} | Hard={hard_res[-1]:.2f}% | Soft={soft_res[-1]:.2f}%")

    return lengths, hard_res, soft_res

# ---------------- PLOT ----------------
def plot_results(lengths, hard, soft):
    plt.plot(lengths, hard, marker='o', label="Hard")
    plt.plot(lengths, soft, marker='o', label="Soft")

    plt.xscale('log')
    plt.xlabel("Message Length")
    plt.ylabel("BER (%)")
    plt.title(f"Hard vs Soft Viterbi Decoding ({p*100:.0f}% channel error)")
    plt.legend()
    plt.grid(True)
    plt.show()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    L, hard, soft = run_experiment()
    plot_results(L, hard, soft)
