import sys
import argparse
from collections import defaultdict
import json
import string
import math


russian_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
symbols_list = russian_alphabet + string.ascii_letters + string.punctuation + " "
symbols_dict = {char: index for index, char in enumerate(symbols_list)}


def shift(symbol, shift_size) -> str:
    index = symbols_dict.get(symbol)
    if index is not None:
        return symbols_list[(index + shift_size) % len(symbols_list)]
    else:
        return symbol


def caesar_encryption(line, step, sign) -> str:
    return "".join([shift(char, sign * step) for char in line])


def vig_shift(symbol, key_symbol, sign):
    return shift(symbol, sign * symbols_dict[key_symbol])


def vig_encryption(line, key_word, sign) -> str:
    return "".join([vig_shift(line[i], key_word[i % len(key_word)], sign) for i in range(len(line))])


def encode(args):
    messages = args.input_file.read()
    if args.cipher == "caesar":
        args.output_file.write(caesar_encryption(messages, int(args.key), 1))
    elif args.cipher == "vigenere":
        args.output_file.write(vig_encryption(messages, args.key, 1))


def decode(args):
    messages = args.input_file.read()
    if args.cipher == "caesar":
        args.output_file.write(caesar_encryption(messages, int(args.key), -1))
    elif args.cipher == "vigenere":
        args.output_file.write(vig_encryption(messages, args.key, -1))


def count_freq(some_text):
    _symbols_freq = defaultdict(int)
    for char in some_text:
        if char in symbols_dict:
            _symbols_freq[char] += 1
    return _symbols_freq


def count_symbol_frequency(args):
    # тк входной текст большой, то нет смысла вводить/выводить его через консоль,
    # поэтому сделаем только ввод из файла(и вывод тоже)
    with open(args.input_file, "r") as in_file:
        symbols_freq = count_freq(in_file.read())
        with open(args.output_file, "w") as write_file:
            json.dump(symbols_freq, write_file)


def caesar_breaking(args):
    messages = args.input_file.read()
    with open(args.file_with_symbols_frequency, "r") as freq_file:
        symbols_freq = json.load(freq_file)
    near_symbols_freq = count_freq(messages)
    min_check = math.inf
    best_step = 0
    for step in range(0, len(symbols_list)):
        check = 0
        for char in symbols_dict:
            check += (near_symbols_freq[char] - symbols_freq[shift(char, step)]) ** 2
        if check < min_check:
            min_check = check
            best_step = step
    args.output_file.write(caesar_encryption(messages, best_step, 1))


def argparser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_encode = subparsers.add_parser('encode')
    parser_encode.add_argument("--input_file", type=argparse.FileType('r'), nargs="?", default=sys.stdin)
    parser_encode.add_argument("--output_file", type=argparse.FileType('w'), nargs="?", default=sys.stdout)
    parser_encode.add_argument("--cipher", choices=["caesar", "vigenere"])
    parser_encode.add_argument("--key", help="step(int) if Caesar cipher "
                               "or key_word(str) if Vigenere cipher")
    parser_encode.set_defaults(func=encode)

    parser_decode = subparsers.add_parser('decode')
    parser_decode.add_argument("--input_file", type=argparse.FileType('r'), nargs="?", default=sys.stdin)
    parser_decode.add_argument("--output_file", type=argparse.FileType('w'), nargs="?", default=sys.stdout)
    parser_decode.add_argument("--cipher", choices=["caesar", "vigenere"])
    parser_decode.add_argument("--key", help="step(int) if Caesar cipher "
                               "or key_word(str) if Vigenere cipher")
    parser_decode.set_defaults(func=decode)

    parser_symbol_frequency = subparsers.add_parser('count_symbol_frequency')
    parser_symbol_frequency.add_argument("--input_file", type=argparse.FileType('r'), nargs="?", default=sys.stdin)
    parser_symbol_frequency.add_argument("--output_file", type=argparse.FileType('w'), nargs="?", default=sys.stdout)
    parser_symbol_frequency.set_defaults(func=count_symbol_frequency)

    parser_caesar_breaking = subparsers.add_parser('caesar_breaking')
    parser_caesar_breaking.add_argument("--input_file", type=argparse.FileType('r'), nargs="?", default=sys.stdin)
    parser_caesar_breaking.add_argument("--output_file", type=argparse.FileType('w'), nargs="?", default=sys.stdout)
    parser_caesar_breaking.add_argument("--file_with_symbols_frequency")
    parser_caesar_breaking.set_defaults(func=caesar_breaking)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    argparser()
