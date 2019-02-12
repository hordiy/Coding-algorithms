import heapq																# Подключение модуля сортировки кучи
from collections import Counter, namedtuple

class Node(namedtuple("Node", ["left", "right"])):							#  Класс для ветвей дерева - внутренних узлов
	def walk(self, code, acc):
		self.left.walk(code, acc + "0")
		self.right.walk(code, acc + "1")

class Leaf(namedtuple("Leaf", ["char"])):									# Класс для листьев дерева - где есть значение символа
	def walk(self, code, acc):
		code[self.char] = acc or "0"

def encode_huf(source):														# Кодирование данных
	h = []
	for ch, freq in Counter(source).items():
		h.append((freq, len(h), Leaf(ch)))
	heapq.heapify(h)
	count = len(h)
	while len(h) > 1:
		freq1, _count1, left = heapq.heappop(h)
		freq2, _count2, right = heapq.heappop(h)
		heapq.heappush(h, (freq1 + freq2, count, Node(left, right)))
		count += 1
	code = {}
	if h:
		[(_freq, _count, root)] = h
		root.walk(code, "")
	return code

def decode_huf(encoded, code):												# Декодирование данных
	sx = []
	enc_ch = ""
	for ch in encoded:
		enc_ch += ch
		for dec_ch in code:
			if code.get(dec_ch) == enc_ch:
				sx.append(dec_ch)
				enc_ch = ""
				break
	return "".join(sx)

def main():
	source = input("Write the text: ")
	code = encode_huf(source)
	encoded = "".join(code[ch] for ch in source)
	assert decode_huf(encoded, code) == source
	decoded = decode_huf(encoded, code)

	print(len(code), len(encoded))
	for ch in sorted(code):
		print("{0}: {1}".format(ch, code[ch]))
	print(encoded)
	print(decoded)
	print(code)

if __name__ == "__main__":
	main()