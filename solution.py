import sys
import argparse
from collections import defaultdict
import json
import string

symbols_list = list()
symbols_dict = defaultdict(int)
index = 0
for char in string.ascii_letters:
    symbols_dict[char] = index
    symbols_list.append(char)
    index += 1


def shift(symbol, shift_size) -> str:
    if symbol in symbols_dict:
        return symbols_list[(symbols_dict[symbol] + shift_size) % len(symbols_list)]
    else:
        return symbol


def caesar_encryption(line, step) -> str:
    return "".join([shift(char, step) for char in line])


def caesar_decryption(line, step) -> str:
    step %= len(symbols_list)
    return "".join([shift(char, len(symbols_list) - step) for char in line])


def vig_encryption(line, key_word) -> str:
    return "".join([shift(line[i], symbols_dict[key_word[i % len(key_word)]]) for i in range(len(line))])


def vig_decryption(line, key_word) -> str:
    return "".join([shift(line[i], len(symbols_list) -
                          symbols_dict[key_word[i % len(key_word)]]) for i in range(len(line))])


def open_messages_and_output():
    _in_file = sys.stdin
    if args.input_file is not None:
        _in_file = open(args.input_file, "r")
    _out_file = sys.stdout
    if args.output_file is not None:
        _out_file = open(args.output_file, "w")
    _messages = _in_file.read()
    return _in_file, _messages, _out_file


def close_in_and_out_files(_input, _output):
    if args.input_file is not None:
        _input.close()
    if args.output_file is not None:
        _output.close()


def encode(args):
    in_file, messages, out_file = open_messages_and_output()
    if args.cipher == "caesar":
        out_file.write(caesar_encryption(messages, int(args.key)))
    elif args.cipher == "vigenere":
        out_file.write(vig_encryption(messages, args.key))
    close_in_and_out_files(in_file, out_file)


def decode(args):
    in_file, messages, out_file = open_messages_and_output()
    if args.cipher == "caesar":
        out_file.write(caesar_decryption(messages, int(args.key)))
    elif args.cipher == "vigenere":
        out_file.write(vig_decryption(messages, args.key))
    close_in_and_out_files(in_file, out_file)


def count_symbol_frequency(args):
    # тк входной текст большой, то нет смысла вводить/выводить его через консоль,
    # поэтому сделаем только ввод из файла(и вывод тоже)
    symbols_freq = defaultdict(int)
    with open(args.input_file, "r") as in_file:
        strings = in_file.read()
        for char in strings:
            if char in symbols_dict:
                symbols_freq[char] += 1
        with open(args.output_file, "w") as write_file:
            json.dump(symbols_freq, write_file)


def caesar_breaking(args):
    in_file, messages, out_file = open_messages_and_output()
    with open(args.file_with_symbols_frequency, "r") as freq_file:
        symbols_freq = json.load(freq_file)
    near_symbols_freq = defaultdict(int)
    for char in messages:
        if char in symbols_dict:
            near_symbols_freq[char] += 1
    min_check = 0
    best_step = 0
    for char in symbols_dict:
        min_check += (near_symbols_freq[char] - symbols_freq[char]) ** 2
    for step in range(1, len(symbols_list)):
        check = 0
        for char in symbols_dict:
            check += (near_symbols_freq[char] -
                      symbols_freq[symbols_list[(symbols_dict[char] + step) % len(symbols_list)]]) ** 2
        if check < min_check:
            min_check = check
            best_step = step
    out_file.write(caesar_encryption(messages, best_step))
    close_in_and_out_files(in_file, out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_encode = subparsers.add_parser('encode')
    parser_encode.add_argument("--input_file")
    parser_encode.add_argument("--output_file")
    parser_encode.add_argument("--cipher", choices=["caesar", "vigenere"])
    parser_encode.add_argument("--key", help="step(int) if Caesar cipher "
                               "or key_word(str) if Vigenere cipher")
    parser_encode.set_defaults(func=encode)

    parser_decode = subparsers.add_parser('decode')
    parser_decode.add_argument("--input_file")
    parser_decode.add_argument("--output_file")
    parser_decode.add_argument("--cipher", choices=["caesar", "vigenere"])
    parser_decode.add_argument("--key", help="step(int) if Caesar cipher "
                               "or key_word(str) if Vigenere cipher")
    parser_decode.set_defaults(func=decode)

    parser_symbol_frequency = subparsers.add_parser('count_symbol_frequency')
    parser_symbol_frequency.add_argument("--input_file")
    parser_symbol_frequency.add_argument("--output_file")
    parser_symbol_frequency.set_defaults(func=count_symbol_frequency)

    parser_caesar_breaking = subparsers.add_parser('caesar_breaking')
    parser_caesar_breaking.add_argument("--input_file")
    parser_caesar_breaking.add_argument("--output_file")
    parser_caesar_breaking.add_argument("--file_with_symbols_frequency")
    parser_caesar_breaking.set_defaults(func=caesar_breaking)

    args = parser.parse_args()
    args.func(args)
