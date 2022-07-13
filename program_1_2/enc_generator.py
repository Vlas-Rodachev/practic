from collections import Counter
import random


def read_file():
    with open('text_shifr.txt') as file:
        text = file.read()
        freq_table = Counter(text)

    return text, freq_table


def encrypt(text):
    available_letters = list(set(text))
    sub_table = {letter: '' for letter in available_letters}
    enc_text = ''

    for letter in sub_table:
        position = random.randint(0, len(available_letters) - 1)
        sub_letter = available_letters.pop(position)
        sub_table[letter] = sub_letter

    for letter in text:
        enc_text += sub_table[letter]

    # test = ''
    # reverse = {v: k for k, v in sub_table.items()}
    # for letter in enc_text:
    #     test += reverse[letter]
    # print(test)

    return enc_text


def main():
    text, freq_table = read_file()
    encrypted = encrypt(text)


if __name__ == '__main__':
    main()
