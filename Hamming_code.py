import random																# Подключение модуля генератора псевдослучайных чисел

CHUNK_LENGTH = 8 															# Длина блока кодирования
CHECK_BITS = [i for i in range(1, CHUNK_LENGTH + 1) if not i & (i - 1)] 	# Вычисление контрольных бит

def chars_to_bin(chars):													# Преобразование символов в бинарный формат
	return "".join([bin(ord(c))[2:].zfill(8) for c in chars])

def chunk_iterator(text_bin, chunk_size=CHUNK_LENGTH):						# Поблочный вывод бинарных данных
	for i in range(len(text_bin)):
		if not i % chunk_size:
			yield text_bin[i:i + chunk_size]

def get_check_bits_data(value_bin):											# Получение информации о контрольных битах из бинарного блока
	check_bits_count_map = {k: 0 for k in CHECK_BITS}
	for index, value in enumerate(value_bin, 1):
		if int(value):
			bin_char_list = list(bin(index)[2:].zfill(8))
			bin_char_list.reverse()
			for degree in [2 ** int(i) for i, value in enumerate(bin_char_list) if int(value)]:
				check_bits_count_map[degree] += 1
	check_bits_value_map = {}
	for check_bit, count in check_bits_count_map.items():
		check_bits_value_map[check_bit] = 0 if not count % 2 else 1
	return check_bits_value_map

def set_empty_check_bits(value_bin):										# Добавление в бинарный блок "пустые контрольные биты"
	for bit in CHECK_BITS:
		value_bin = value_bin[:bit - 1] + "0" + value_bin[bit - 1:]
	return value_bin

def set_check_bits(value_bin):												# Устрановка значений контрольных бит
	value_bin = set_empty_check_bits(value_bin)
	check_bits_data = get_check_bits_data(value_bin)
	for check_bit, bit_value in check_bits_data.items():
		value_bin = "{0}{1}{2}".format(value_bin[:check_bit - 1], bit_value, value_bin[check_bit:])
	return value_bin

def get_check_bits(value_bin):												# Получение информации о контрольных битах из блока
	check_bits = {}
	for index, value in enumerate(value_bin, 1):
		if index in CHECK_BITS:
			check_bits[index] = int(value)
	return check_bits

def exclude_check_bits(value_bin):											# Исключение информации о контрольных битах из блока
	clean_check_bits = ""
	for index, value in enumerate(list(value_bin), 1):
		if index not in CHECK_BITS:
			clean_check_bits += value
	return clean_check_bits

def check_and_fix_errors(encoded_chunk):									# Проверка и исправление ошибки в блоке
	check_encoded_bits = get_check_bits(encoded_chunk)
	check_item = exclude_check_bits(encoded_chunk)
	check_item = set_check_bits(check_item)
	check_bits = get_check_bits(check_item)
	if check_encoded_bits != check_bits:
		invalid_bits = []
		for check_encoded_bit, value in check_encoded_bits.items():
			if check_bits[check_encoded_bit] != value:
				invalid_bits.append(check_encoded_bit)
		num_bit = sum(invalid_bits)
		encoded_chunk = "{0}{1}{2}".format(encoded_chunk[:num_bit - 1], int(encoded_chunk[num_bit - 1]) ^ 1, encoded_chunk[num_bit:])
	return encoded_chunk

def encode_ham(source):														# Кодирование данных
	encoded = ""
	text_bin = chars_to_bin(source)
	for encoded_chunk in chunk_iterator(text_bin):
		encoded_chunk = set_check_bits(encoded_chunk)
		encoded += encoded_chunk
	return encoded

def decode_ham(encoded, fix_errors=True):									# Декодирование данных
	decoded = ""
	fixed_bits_list = []
	for encoded_chunk in chunk_iterator(encoded, CHUNK_LENGTH + len(CHECK_BITS)):
		if fix_errors:
			encoded_chunk = check_and_fix_errors(encoded_chunk)
		fixed_bits_list.append(encoded_chunk)
	
	clean_bits_list = []
	for encoded_chunk in fixed_bits_list:
		encoded_chunk = exclude_check_bits(encoded_chunk)
		clean_bits_list.append(encoded_chunk)

	for clean_chunk in clean_bits_list:
		for clean_char in [clean_chunk[i:i + 8] for i in range(len(clean_chunk)) if not i % 8]:
			decoded += chr(int(clean_char, 2))
	return decoded

def set_errors(encoded):													# Допуск ошибки в блоке
	result = ""
	for encoded_chunk in chunk_iterator(encoded, CHUNK_LENGTH + len(CHECK_BITS)):
		num_bit = random.randint(1, len(encoded_chunk))
		encoded_chunk = "{0}{1}{2}".format(encoded_chunk[:num_bit - 1], int(encoded_chunk[num_bit - 1]) ^ 1, encoded_chunk[num_bit:])
		result += encoded_chunk
	return result

def get_diff_index_list(value_bin1, value_bin2):							# Получение списка индексов с ошибками в битах
	diff_index_list = []
	for index, value in enumerate(zip(list(value_bin1), list(value_bin2)), 1):
		if value[0] != value[1]:
			diff_index_list.append(index)
	return diff_index_list

def main():
	source = input("Write the text: ")
	print("Length: {0}\nCheck bits: {1}".format(CHUNK_LENGTH, CHECK_BITS))
	encoded = encode_ham(source)
	print("Encoded the text: ", encoded)
	decoded = decode_ham(encoded)
	print("Decoded the text: ", decoded)
	encoded_with_errors = set_errors(encoded)
	print("Errors: ", encoded_with_errors)
	diff_index_list = get_diff_index_list(encoded, encoded_with_errors)
	print("Errors got in the bits: {0}".format(diff_index_list))
	decoded = decode_ham(encoded_with_errors, fix_errors=False)
	print("Encoded without fix errors: ", decoded)
	decoded = decode_ham(encoded_with_errors)
	print("Encoded with fix errors: ", decoded)

if __name__ == "__main__":
	main()