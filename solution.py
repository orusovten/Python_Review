import argparse


def count_frequency(a, freq_list):
    for i in range(len(a)):
        if "A" <= a[i] <= "Z":
            freq_list[ord(a[i]) - ord("A")] += 1
        elif "a" <= a[i] <= "z":
            freq_list[ord("Z") - ord("A") + 1 + ord(a[i]) - ord("a")] += 1
    return freq_list


def caesar_encryption(a, step) -> str:
    copy = str()
    for i in range(len(a)):
        if "A" <= a[i] <= "Z":
            tmp = ord(a[i]) + step
            if tmp <= ord("Z"):
                copy += chr(tmp)
            else:
                copy += chr(ord("A") + tmp - ord("Z") - 1)
        elif "a" <= a[i] <= "z":
            tmp = ord(a[i]) + step
            if tmp <= ord("z"):
                copy += chr(tmp)
            else:
                copy += chr(ord("a") + tmp - ord("z") - 1)
    return copy


def caesar_decryption(a, step) -> str:
    copy = str()
    for i in range(len(a)):
        if "A" <= a[i] <= "Z":
            tmp = ord(a[i]) - step
            if tmp >= ord("A"):
                copy += chr(tmp)
            else:
                copy += chr(ord("Z") - ord("A") + tmp + 1)
        elif "a" <= a[i] <= "z":
            tmp = ord(a[i]) - step
            if tmp >= ord("a"):
                copy += chr(tmp)
            else:
                copy += chr(ord("z") - ord("a") + tmp + 1)
    return copy


def vig_encryption(a, key_word) -> str:
    copy = str()
    low_key_word = key_word.lower()
    up_key_word = key_word.upper()
    for i in range(len(a)):
        if "A" <= a[i] <= "Z":
            tmp = (ord(up_key_word[i % len(up_key_word)]) + ord(a[i]) - ord("A")) % ord("Z")
            if tmp < ord("A"):
                copy += chr(tmp + ord("A") - 1)
            else:
                copy += chr(tmp)
        elif "a" <= a[i] <= "z":
            tmp = (ord(low_key_word[i % len(low_key_word)]) + ord(a[i]) - ord("a")) % ord("z")
            if tmp < ord("a"):
                copy += chr(tmp + ord("a") - 1)
            else:
                copy += chr(tmp)
    return copy


def vig_decryption(a, key_word) -> str:
    copy = str()
    low_key_word = key_word.lower()
    up_key_word = key_word.upper()
    for i in range(len(a)):
        if "A" <= a[i] <= "Z":
            tmp = ord(a[i]) - ord(up_key_word[i % len(up_key_word)])
            if tmp >= 0:
                copy += chr(tmp + ord("A"))
            else:
                copy += chr(ord("Z") + tmp + 1)
        elif "a" <= a[i] <= "z":
            tmp = ord(a[i]) - ord(low_key_word[i % len(low_key_word)])
            if tmp >= 0:
                copy += chr(tmp + ord("a"))
            else:
                copy += chr(ord("z") + tmp + 1)
    return copy


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", type=str)
    parser.add_argument("--input_file", action="store")
    parser.add_argument("--output_file", action="store")
    parser.add_argument("--cipher", action="store")
    parser.add_argument("--key", action="store")
    parser.add_argument("--file_with_symbols_frequency", action="store")
    args = parser.parse_args()
    if args.operation == "encode":
        # in_file - файл с исходным текстом
        in_file = open(args.input_file, "r")
        # out_file - файл с зашифрованным текстом
        out_file = open(args.output_file, "w")
        messages = in_file.read().split('\n')
        if messages[-1] == '':
            messages = messages[:len(messages) - 1]
        if args.cipher == "caesar":
            for message in messages:
                out_file.write(caesar_encryption(message, int(args.key)))
                out_file.write('\n')
        elif args.cipher == "vigenere":
            for message in messages:
                out_file.write(vig_encryption(message, args.key))
                out_file.write('\n')
        in_file.close()
        out_file.close()
    elif args.operation == "decode":
        # in_file - файл с зашифрованным текстом
        in_file = open(args.input_file, "r")
        # out_file - файл с исходным текстом
        out_file = open(args.output_file, "w")
        message = in_file.readline()
        if args.cipher == "caesar":
            out_file.write(caesar_decryption(message, int(args.key)))
        elif args.cipher == "vigenere":
            out_file.write(vig_decryption(message, args.key))
        in_file.close()
        out_file.close()
    elif args.operation == "count_symbol_frequency":
        # in_file - большой текст
        in_file = open(args.input_file, "r")
        # out_file - файл с частотами символов
        out_file = open(args.output_file, "w")
        lines = in_file.read()
        symbols_freq = [0 for i in range(ord("A"), ord("Z") + 1)]
        for i in range(ord("a"), ord("z") + 1):
            symbols_freq.append(0)
        for line in lines:
            symbols_freq = count_frequency(line, symbols_freq)
        # шаг между "A" и "a"
        step1 = ord("Z") - ord("A") + 1
        # пишем в столбик: заглавная латинская буква - ее число
        for i in range(step1):
            out_file.write(chr(ord("A") + i) + " - " + str(symbols_freq[i]) + '\n')
        # пишем в столбик: строчная латинская буква - ее число
        for i in range(step1, step1 + ord("z") - ord("a") + 1):
            out_file.write(chr(ord("a") + i - step1) + " - " + str(symbols_freq[i]) + '\n')
        in_file.close()
        out_file.close()
    elif args.operation == "caesar_breaking":
        # in_file - файл с зашифрованным текстом
        in_file = open(args.input_file, "r")
        # freq_file - файл с частотами символов
        freq_file = open(args.file_with_symbols_frequency, "r")
        # out_file - файл с исходным текстом
        out_file = open(args.output_file, "w")
        lines = freq_file.read().split('\n')
        if lines[-1] == '':
            lines = lines[:len(lines) - 1]
        symbols_freq = list()
        for i in range(ord("Z") - ord("A") + 1 + ord("z") - ord("a") + 1):
            lines[i] = lines[i].split()
            # тк частота символа находится после него и тире
            symbols_freq.append(int(lines[i][2]))
        # for step in range(ord("Z") - ord("A") + 1):
        messages = in_file.read().split('\n')
        if messages[-1] == '':
            messages = messages[:len(messages) - 1]
        # шаг между "A" и "a"
        step1 = ord("Z") - ord("A") + 1
        # проверим сами строки без изменений
        near_symbols_freq = [0 for i in range((ord("Z") - ord("A") + 1) * 2)]
        for message in messages:
            near_symbols_freq = count_frequency(message, near_symbols_freq)
        # наиболее подходящий шаг расшивровки
        best_step = 0
        # наименьшее отклонение от частот символов
        min_check = 0
        for i in range(len(symbols_freq)):
            min_check += (symbols_freq[i] - near_symbols_freq[i]) ** 2
        # проверим измененные строки
        for try_step in range(1, ord("Z") - ord("A") + 1):
            near_symbols_freq = [0 for i in range((ord("Z") - ord("A") + 1) * 2)]
            for message in messages:
                near_message = caesar_decryption(message, try_step)
                near_symbols_freq = count_frequency(near_message, near_symbols_freq)
            check = 0
            for i in range(len(symbols_freq)):
                check += (symbols_freq[i] - near_symbols_freq[i]) ** 2
            if check < min_check:
                min_check = check
                best_step = try_step
        # теперь знаем лучший шаг
        for message in messages:
            out_file.write(caesar_decryption(message, best_step))
            out_file.write('\n')
        in_file.close()
        freq_file.close()
        out_file.close()
