import sys
import argparse
from collections import defaultdict
import json
import string
import math


SYMBOLS_LIST = string.ascii_letters + string.punctuation + " "
SYMBOLS_DICT = {char: index for index, char in enumerate(SYMBOLS_LIST)}


def shift_symbol(symbol, shift_size) -> str:
    index = SYMBOLS_DICT.get(symbol)
    if index is not None:
        return SYMBOLS_LIST[(index + shift_size) % len(SYMBOLS_LIST)]
    else:
        return symbol


def caesar_encode(line, step, sign) -> str:
    return "".join([shift_symbol(char, sign * step) for char in line])


def vigenere_shift(symbol, key_symbol, sign):
    return shift_symbol(symbol, sign * SYMBOLS_DICT[key_symbol])


def vigenere_encode(line, key_word, sign) -> str:
    return "".join([vigenere_shift(char, key_word[index % len(key_word)], sign) for index, char in enumerate(line)])


def encode(args):
    messages = args.input_file.read()
    if args.cipher == "caesar":
        args.output_file.write(caesar_encode(messages, int(args.key), args.sign))
    elif args.cipher == "vigenere":
        args.output_file.write(vigenere_encode(messages, args.key, args.sign))


def count_freq(some_text):
    symbols_freq = defaultdict(int)
    for char in some_text:
        if char in SYMBOLS_DICT:
            symbols_freq[char] += 1
    return symbols_freq


def count_symbol_frequency(args):
    # тк входной текст большой, то нет смысла вводить/выводить его через консоль,
    # поэтому сделаем только ввод из файла(и вывод тоже)
    symbols_freq = count_freq(args.input_file.read())
    json.dump(symbols_freq, args.output_file)


def caesar_break(args):
    messages = args.input_file.read()
    with open(args.file_with_symbols_frequency, "r") as freq_file:
        symbols_freq = json.load(freq_file)
    near_symbols_freq = count_freq(messages)
    min_difference = math.inf
    best_shift = 0
    for shift in range(len(SYMBOLS_LIST)):
        difference = 0
        for char in SYMBOLS_DICT:
            main_freq = symbols_freq.get(shift_symbol(char, shift))
            if main_freq is not None:
                difference += (near_symbols_freq[char] - main_freq) ** 2
        if difference < min_difference:
            min_difference = difference
            best_shift = shift
    args.output_file.write(caesar_encode(messages, best_shift, 1))


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_encode = subparsers.add_parser('encode')
    parser_encode.add_argument("--input_file", type=argparse.FileType('r'), default=sys.stdin)
    parser_encode.add_argument("--output_file", type=argparse.FileType('w'), default=sys.stdout)
    parser_encode.add_argument("--cipher", choices=["caesar", "vigenere"], required=True)
    parser_encode.add_argument("--key", help="step(int) if Caesar cipher "
                               "or key_word(str) if vigenere cipher", required=True)
    parser_encode.set_defaults(sign=1)
    parser_encode.set_defaults(func=encode)

    parser_decode = subparsers.add_parser('decode')
    parser_decode.add_argument("--input_file", type=argparse.FileType('r'), default=sys.stdin)
    parser_decode.add_argument("--output_file", type=argparse.FileType('w'), default=sys.stdout)
    parser_decode.add_argument("--cipher", choices=["caesar", "vigenere"], required=True)
    parser_decode.add_argument("--key", help="step(int) if Caesar cipher "
                               "or key_word(str) if vigenere cipher", required=True)
    parser_decode.set_defaults(sign=-1)
    parser_decode.set_defaults(func=encode)

    parser_symbol_frequency = subparsers.add_parser('count_symbol_frequency')
    parser_symbol_frequency.add_argument("--input_file", type=argparse.FileType('r'), required=True)
    parser_symbol_frequency.add_argument("--output_file", type=argparse.FileType('w'), required=True)
    parser_symbol_frequency.set_defaults(func=count_symbol_frequency)

    parser_caesar_breaking = subparsers.add_parser('caesar_breaking')
    parser_caesar_breaking.add_argument("--input_file", type=argparse.FileType('r'), default=sys.stdin)
    parser_caesar_breaking.add_argument("--output_file", type=argparse.FileType('w'), default=sys.stdout)
    parser_caesar_breaking.add_argument("--file_with_symbols_frequency", required=True)
    parser_caesar_breaking.set_defaults(func=caesar_break)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    args.func(args)
