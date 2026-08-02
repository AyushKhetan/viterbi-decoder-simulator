import random
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

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))

def encode(bits):
    state = [0, 0]
    output = []
    for b in bits:
        g1 = b ^ state[0]
        g2 = b ^ state[0] ^ state[1]
        output.append((g1, g2))
        state = [b] + state[:-1]
    return output

def add_noise(encoded, p):
    noisy = []
    for b1, b2 in encoded:
        nb1 = b1 ^ (random.random() < p)
        nb2 = b2 ^ (random.random() < p)
        noisy.append((int(nb1), int(nb2)))
    return noisy

def viterbi_decode(received):
    PM = {0: 0, 1: float('inf'), 2: float('inf'), 3: float('inf')}
    paths = {0: [], 1: [], 2: [], 3: []}

    for t in range(len(received)):
        new_PM = {0: float('inf'), 1: float('inf'), 2: float('inf'), 3: float('inf')}
        new_paths = {0: [], 1: [], 2: [], 3: []}

        for state in range(4):
            if PM[state] == float('inf'):
                continue

            for inp in [0, 1]:
                next_state, output = trellis[(state, inp)]
                metric = PM[state] + hamming_distance(output, received[t])

                if metric < new_PM[next_state]:
                    new_PM[next_state] = metric
                    new_paths[next_state] = paths[state] + [inp]

        PM = new_PM
        paths = new_paths

    best_state = min(PM, key=PM.get)
    return paths[best_state]

error_rate = 0.15

# ---------------- EXPERIMENT ----------------
def run_experiment():
    lengths = [10, 15, 25, 40, 65, 100, 160, 250, 400, 1000]

    regimes = {
        "Low (1k bits)": 1000,
        "Medium (10k bits)": 10000,
        "High (100k bits)": 100000
    }

    results = {regime: [] for regime in regimes}

    for regime, total_bits in regimes.items():
        print(f"\n=== Running {regime} ===")

        for L in lengths:
            trials = max(1, total_bits // L)

            total_errors = 0
            total_bits_used = 0

            for _ in range(trials):
                msg = [random.randint(0,1) for _ in range(L)]
                encoded = encode(msg)
                received = add_noise(encoded, error_rate)
                decoded = viterbi_decode(received)

                errors = sum(m != d for m, d in zip(msg, decoded))
                total_errors += errors
                total_bits_used += L

            ber = total_errors / total_bits_used
            ber_percent = ber * 100   # 🔥 conversion

            results[regime].append(ber_percent)

            print(f"L={L}, Trials={trials}, BER={ber_percent:.2f}%")

    return lengths, results

# ---------------- TABLE PRINT ----------------
def print_table(lengths, results):
    print("\n\n===== RESULT TABLE =====")
    print("Length\tLow\tMedium\tHigh")

    for i, L in enumerate(lengths):
        row = [f"{results[regime][i]:.2f}%" for regime in results]
        print(f"{L}\t" + "\t".join(row))

# ---------------- PLOT ----------------
def plot_results(lengths, results):
    for regime, ber_list in results.items():
        plt.plot(lengths, ber_list, marker='o', label=regime)

    plt.xscale('log')
    plt.xlabel("Message Length (log scale)")
    plt.ylabel("Bit Error Rate (%)")   # 🔥 updated label
    plt.title(f"Viterbi Performance vs Message Length ({error_rate*100:.0f}% channel error)")
    plt.legend()
    plt.grid(True)
    plt.show()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    lengths, results = run_experiment()
    print_table(lengths, results)
    plot_results(lengths, results)