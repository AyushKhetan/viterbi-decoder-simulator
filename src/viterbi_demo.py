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

# ---------------- HAMMING DISTANCE ----------------
def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))

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

# ---------------- NOISE ----------------
def add_noise(encoded, p):
    noisy = []
    for b1, b2 in encoded:
        nb1 = b1 ^ (random.random() < p)
        nb2 = b2 ^ (random.random() < p)
        noisy.append((int(nb1), int(nb2)))
    return noisy

# ---------------- VITERBI ----------------
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

# ---------------- TRELLIS VISUALIZATION ----------------
def visualize_trellis(received, best_path):
    state_y = {0: 0, 1: 1, 2: 2, 3: 3}
    n = len(received)

    plt.figure(figsize=(12, 6))

    for t in range(n + 1):
        for s in range(4):
            plt.scatter(t, state_y[s])
            plt.text(t, state_y[s] + 0.1, str(s), ha='center', fontsize=8)

    for t in range(n):
        for s in range(4):
            for inp in [0, 1]:
                next_s, _ = trellis[(s, inp)]
                plt.plot([t, t+1], [state_y[s], state_y[next_s]],
                         linewidth=0.8, alpha=0.3)

    state = 0
    for t in range(n):
        inp = best_path[t]
        next_s, _ = trellis[(state, inp)]
        plt.plot([t, t+1], [state_y[state], state_y[next_s]],
                 linewidth=3)
        state = next_s

    for t in range(n):
        plt.text(t + 0.5, 3.5, str(received[t]), ha='center')

    plt.title("Trellis Diagram with Best Path")
    plt.xlabel("Time Step")
    plt.ylabel("State")
    plt.yticks([0,1,2,3], ['00','01','10','11'])
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.show()

# ---------------- MAIN ----------------
if __name__ == "__main__":

    length = int(input("Enter message length: "))
    error_percent = float(input("Enter error percentage: "))
    trials = int(input("Enter number of trials: "))

    p = error_percent / 100

    total_errors = 0
    total_bits = 0

    best_case = float('inf')
    worst_case = 0

    sample_data = None

    for t in range(trials):
        message = [random.randint(0,1) for _ in range(length)]
        encoded = encode(message)
        received = add_noise(encoded, p)
        decoded = viterbi_decode(received)

        errors = sum(m != d for m, d in zip(message, decoded))

        total_errors += errors
        total_bits += length

        best_case = min(best_case, errors)
        worst_case = max(worst_case, errors)

        # store one sample run for display
        if t == 0:
            sample_data = (message, encoded, received, decoded)

    # ---------------- RESULTS ----------------
    ber = total_errors / total_bits

    print("\n===== SUMMARY =====")
    print(f"Trials: {trials}")
    print(f"Average BER: {ber:.4f}")
    print(f"Best Case Errors: {best_case}")
    print(f"Worst Case Errors: {worst_case}")

    # ---------------- SAMPLE OUTPUT ----------------
    message, encoded, received, decoded = sample_data

    print("\n===== SAMPLE RUN =====")

    print("\nOriginal Message:")
    print(" ".join(map(str, message)))

    print("\nEncoded Parity Bits:")
    print(" ".join(f"{b1}{b2}" for b1, b2 in encoded))

    print("\nReceived Bits:")
    print(" ".join(f"{b1}{b2}" for b1, b2 in received))

    print("\nDecoded Message:")
    print(" ".join(map(str, decoded)))

    # Trellis visualization
    visualize_trellis(received, decoded)
