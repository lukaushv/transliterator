import csv
from itertools import product

def transliterate_georgian(word):
    transliterations = {
        'ხ': ['kh', 'x'],
        'ძ': ['z', 'dz'],
        'ჭ': ['w', 'ch'],
        'წ': ['w', 'c'],
        'ჟ': ['j', 'zh'],
        'ღ': ['gh', 'g'],
        'ფ': ['f', 'p'],
        'ყ': ['y', 'k'],
        'ა': ['a'],
        'ბ': ['b'],
        'გ': ['g'],
        'დ': ['d'],
        'ე': ['e'],
        'ვ': ['v'],
        'ზ': ['z'],
        'თ': ['t'],
        'ი': ['i'],
        'კ': ['k'],
        'ლ': ['l'],
        'მ': ['m'],
        'ნ': ['n'],
        'ო': ['o'],
        'პ': ['p'],
        'რ': ['r'],
        'ს': ['s'],
        'ტ': ['t'],
        'უ': ['u'],
        'ქ': ['k', 'q'],
        'ც': ['ts', 'c'],
        'ჯ': ['j'],
        'ჰ': ['h'],
        'შ': ['sh'],
        'ჩ': ['ch']
    }

    possible_transliterations = [transliterations.get(char, [char]) for char in word]
    all_combinations = [''.join(combination) for combination in product(*possible_transliterations)]

    return all_combinations


def is_swear_word(word, swear_words):
    return any(word.lower() in swear.lower() for swear in swear_words)


def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file]

    return words


def write_to_csv(georgian_words, swear_words, is_swear_value):
    output_file = 'output.csv'

    existing_georgian_words = set()

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['word', 'binary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for is_swear, georgian_word in zip(is_swear_value, georgian_words):
            if georgian_word not in existing_georgian_words:

                writer.writerow({'word': georgian_word, 'binary': '1' if is_swear else '0'})
                existing_georgian_words.add(georgian_word)


                transliterations = transliterate_georgian(georgian_word)
                for transliteration in transliterations:
                    writer.writerow({'word': transliteration, 'binary': '1' if is_swear else '0'})
                    existing_georgian_words.add(transliteration)


        for swear_word in swear_words:
            if swear_word not in existing_georgian_words:

                writer.writerow({'word': swear_word, 'binary': '1'})
                existing_georgian_words.add(swear_word)


                swear_transliterations = transliterate_georgian(swear_word)
                for transliteration in swear_transliterations:
                    writer.writerow({'word': transliteration, 'binary': '1'})
                    existing_georgian_words.add(transliteration)

    print(f"Results written to {output_file}")



georgian_words_file_path = 'sitkvebi.txt'
swear_words_file_path = 'ginebebi.txt'

georgian_words = read_words_from_file(georgian_words_file_path)
swear_words = read_words_from_file(swear_words_file_path)


is_swear_values = [False] * len(georgian_words)
swear_set = set(swear_words)
for i, word in enumerate(georgian_words):
    if word in swear_set:
        is_swear_values[i] = True

write_to_csv(georgian_words, swear_words, is_swear_values)