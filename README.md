# Python_Review
Названия всех примеров файлов "говорящие", потому переводить их не будем.
Шифрование Цезаря:
python solution.py encode --input_file caesar_input.txt --output_file caesar_output.txt --cipher caesar --key 1
Шифрование Виженера:
python solution.py encode --input_file vigenere_input.txt --output_file vigenere_output.txt --cipher vigenere --key LEMON
Дешифрование Цезаря:
python solution.py decode --input_file encaesar_input.txt --output_file encaesar_output.txt --cipher caesar --key 1
Дешифрование Виженера:
python solution.py decode --input_file envigenere_input.txt --output_file envigenere_output.txt --cipher vigenere --key LEMON
Подсчет частот букв в тексте:
python solution.py count_symbol_frequency --input_file big_text.txt --output_file file_with_symbols_frequency.txt
Взлом Цезаря:
python solution.py caesar_breaking --input_file breaking_caesar_input.txt --output_file breaking_caesar_output.txt --file_with_symbols_frequency file_with_symbols_frequency.txt
