from collections import Counter
import csv
def count_character_frequency(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        frequency_counter = Counter(text)
        return frequency_counter
def save_frequency_to_csv(counter, output_file_path):
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Character', 'Frequency'])
        sorted_counter = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
        for char, freq in sorted_counter:
            writer.writerow([char, freq])
file_path = 'bible_wordsonly.txt'
output_file_path = 'freq.csv'
counter = count_character_frequency(file_path)
save_frequency_to_csv(counter, output_file_path)