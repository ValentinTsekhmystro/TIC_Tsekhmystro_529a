import random
import string
import collections
import math
import matplotlib.pyplot as plt

# 1
def generate_sequence_1(N1, N_sequence):
    list1 = ['1'] * N1
    list0 = ['0'] * (N_sequence - N1)
    sequence = list1 + list0
    random.shuffle(sequence)
    original_sequence_1 = ''.join(sequence)
    unique_chars = set(original_sequence_1)
    return original_sequence_1

# 2
def generate_sequence_2(surname, N_sequence):
    list1 = list(surname)
    list0 = ['0'] * (N_sequence - len(surname))
    sequence = list1 + list0
    original_sequence_2 = ''.join(sequence)
    return original_sequence_2

# 3
def generate_sequence_3(surname, N_sequence):
    N1 = len(surname)
    list1 = list(surname)
    list0 = ["0"] * (N_sequence - N1)
    seq = list1 + list0
    random.shuffle(seq)
    original_sequence_3 = ''.join(seq)
    return original_sequence_3

# 4
def generate_sequence_4(surname, N_sequence):
    letters = list(surname + "529a")
    n_letters = len(letters)
    n_repeats = N_sequence // n_letters
    remainder = N_sequence % n_letters
    sequence = letters * n_repeats
    sequence += letters[:remainder]
    original_sequence_4 = ''.join(sequence)
    return original_sequence_4

# 5
def generate_sequence_5(N_sequence):
    alphabet = ['ц', 'е', '5', '2', '9', 'а']
    my_info = ['це', '529а']
    prob = 0.2
    sequence = [random.choices(alphabet, weights=[prob if char in my_info else 1 - prob for char in alphabet])[0] for _
                in range(N_sequence)]
    random.shuffle(sequence)
    original_sequence_5 = ''.join(sequence)
    return original_sequence_5

# 6
def generate_sequence_6():
    surname = 'це'
    group_number = '529а'
    letters = [surname[0], surname[1]]

    digits = list(group_number)
    prob_letters = 0.7
    prob_digits = 0.3
    n_letters = int(prob_letters * 100)
    n_digits = int(prob_digits * 100)
    list_100 = []
    for i in range(n_letters):
        list_100.append(random.choice(letters))
    for i in range(n_digits):
        list_100.append(random.choice(digits))
    random.shuffle(list_100)
    original_sequence_6 = ''.join(list_100)
    return original_sequence_6

# 7
def generate_sequence_7(N_sequence):
    elements = string.ascii_lowercase + string.digits
    list_100 = [random.choice(elements) for _ in range(N_sequence)]
    random.shuffle(list_100)
    original_sequence_7 = ''.join(list_100)
    return original_sequence_7

# 8
def generate_sequence_8(N_sequence):
    original_sequence_8 = '1' * N_sequence
    return original_sequence_8

def save_sequence(original_sequence, original_sequence_size, sequence_alphabet_size, symbol_count, mean_probability,
                  uniformity, entropy, source_excess):
    try:
        with open("results_sequence.txt", "a", encoding="utf8") as file:
            file.write(f"Послідовність: {original_sequence}\n")
            file.write(f"Розмір послідовності: {original_sequence_size} байт\n")
            file.write(f"Розмір алфавіту: {sequence_alphabet_size}\n")
            file.write(f"Ймовірність появи символів: {symbol_count}\n")
            file.write(f"Середнє арифметичне ймовірностей: {mean_probability}\n")
            file.write(f"Ймовірність розподілу символів: {uniformity}\n")
            file.write(f"Ентропія: {entropy}\n")
            file.write(f"Надмірність джерела: {source_excess}\n" + "-" * 100 + "\n")
    except FileNotFoundError:
        with open("results_sequence.txt", "w", encoding="utf8") as file:
            file.write(f"Послідовність: {original_sequence}\n")
            file.write(f"Розмір послідовності: {original_sequence_size} байт\n")
            file.write(f"Розмір алфавіту: {sequence_alphabet_size}\n")
            file.write(f"Ймовірність появи символів: {symbol_count}\n")
            file.write(f"Середнє арифметичне ймовірностей: {mean_probability}\n")
            file.write(f"Ймовірність розподілу символів: {uniformity}\n")
            file.write(f"Ентропія: {entropy}\n")
            file.write(f"Надмірність джерела: {source_excess}\n" + "-" * 100 + "\n")
def sequence_txt(seq):
    try:
        with open("sequence.txt", "a", encoding="utf8") as file:
            file.write(f"{seq}\n")
    except FileNotFoundError:
        with open("sequence.txt", "w", encoding="utf8") as file:
            file.write(f"{seq}\n")

def main():
    N1 = 15
    N_sequence = 100
    surname = "Цехмистро"
    original_sequences = [generate_sequence_1(N1, N_sequence),generate_sequence_2(surname, N_sequence),generate_sequence_3(surname, N_sequence),
                          generate_sequence_4(surname, N_sequence), generate_sequence_5(N_sequence),
                          generate_sequence_6(),generate_sequence_7(N_sequence),generate_sequence_8(N_sequence)]
    results = []
    for sequence in original_sequences:
        counts = collections.Counter(sequence)
        probability = {symbol: count / N_sequence for symbol, count in counts.items()}
        mean_probability = sum(probability.values()) / len(probability)
        equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())
        if equal:
            uniformity = "рівна"
        else:
            uniformity = "нерівна"
        entropy = -sum(p * math.log2(p) for p in probability.values())
        if len(set(sequence)) > 1:
            source_excess = 1 - entropy / math.log2(len(set(sequence)))
        else:
            source_excess = 1
        probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])
        sequence_txt(sequence)
        save_sequence(sequence, len(sequence), len(set(sequence)), probability_str, mean_probability, uniformity,
                      entropy, source_excess)
        results.append([len(set(sequence)), round(entropy, 2), round(source_excess, 2), uniformity])
    fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
    headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
    row = [f'Послідовність {i}' for i in range(1, 9)]
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)
    fig.savefig("Характеристики сформованих послідовностей.png", dpi=600)


if __name__ == "__main__":
    main()

