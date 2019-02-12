from Huffman_code import encode_huf, decode_huf    									# Подключение модуля кода Хаффмана
from Hamming_code import *															# Подключение модуля кода Хемминга
import random																		# Подключение модуля генератора псевдослучайных чисел

def encode_XOR(source):																# Кодирование данных шифра XOR
	encoded = ""
	for i in source:
		encoded += chr(ord(i)^key)
	return encoded

def decode_XOR(encoded):															# Декодирование данных Шифра XOR
	decoded = ""
	for i in encoded:
		decoded += chr(ord(i)^key)
	return decoded


if __name__ == "__main__": 
	source = input("Ваше сообщение: ")												# Ввод сообщения
	#key = int(input("Enter the key: "))
	keyr = random.randint(1, 10000)													# Генерация чисел
	key = keyr														
	print("Ключ:", key)
	#Кодировка
	print("\n\t\t\t------Процесс кодирования сообщения------")
	
	# XOR
	encoded_XOR = encode_XOR(source)												# Кодирование сообщения шифром XOR
	print("\nЗакодированное сообщение с шифром 'XOR':", encoded_XOR, "\n")
	
	# Huffman_code
	code_huf = encode_huf(encoded_XOR)												# Кодирование сообщения алгоритмом Хаффмана				
	encoded_huf = "".join(code_huf[ch] for ch in encoded_XOR)
	print(len(code_huf), len(encoded_huf))
	for ch in sorted(code_huf):
		print("{chars}: {codes}".format(chars=ch, codes=code_huf[ch]))
	print("\nЗакодированное сообщение с алгоритмом 'Хаффмана':", encoded_huf)
	
	# Hamming_code
	encoded_ham = encode_ham(encoded_huf)											# Кодирование сообщения кодом Хеминга
	print("\nЗакодированное сообщение с кодированием 'Хемминга':", encoded_ham)

	# Декодировка
	print("\n\t\t\t------Процесс декодирования сообщения------")

	# Hamming_code																	# Декодирование сообщения кодом Хемминга
	encoded_with_error = set_errors(encoded_ham)									# Допуск ошибки в блоке									
	print("\nОшибки в закодированном сообщении:", encoded_with_error)
	diff_index_list = get_diff_index_list(encoded_ham, encoded_with_error)			# Получение списка индексов с ошибками в битах
	print("Список ошибок в битах:", diff_index_list)
	decoded_ham = decode_ham(encoded_with_error, fix_errors=False)					# Вывод без исправления ошибок
	print("\nДекодирование сообщения без исправления ошибок:", decoded_ham)
	decoded_ham = decode_ham(encoded_with_error)									# Вывод с исправлением ошибок
	print("Декодирование сообщения с исправлением ошибок:", decoded_ham)
	
	# Huffman_code
	decoded_huf = decode_huf(decoded_ham, code_huf)									# Декодирование сообщения алгоритмом Хаффмана
	print("\nДекодированное сообщение с алгоритмом 'Хаффмана:", decoded_huf)			
	# XOR
	decoded_XOR = decode_XOR(decoded_huf)											# Декодирование сообщения шифром XOR
	print("\nДекодированное сообщение с шифром 'XOR':", decoded_XOR)

