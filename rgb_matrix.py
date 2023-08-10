import RPi.GPIO as GPIO
import time
import threading
from chars_bn import letter_bitmaps_bn, letters_bn
from chars_es import letter_bitmaps_es, letters_es
from chars_ru import letter_bitmaps_ru, letters_ru
from chars_uz import letter_bitmaps_uz, letters_uz
from color_selector import Color_Selector
from voice_service import Voice_Service
vs = Voice_Service(True)
cs = Color_Selector()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
class RGB_MATRIX:
	def __init__(self):
		self.delay = 0.000001
		self.red1_pin = 17
		self.green1_pin = 18
		self.blue1_pin = 22
		self.red2_pin = 23
		self.green2_pin = 24
		self.blue2_pin = 25
		self.clock_pin = 3
		self.a_pin = 7
		self.b_pin = 8
		self.c_pin = 9
		self.latch_pin = 4
		self.oe_pin = 2
		GPIO.setup(self.red1_pin, GPIO.OUT)
		GPIO.setup(self.green1_pin, GPIO.OUT)
		GPIO.setup(self.blue1_pin, GPIO.OUT)
		GPIO.setup(self.red2_pin, GPIO.OUT)
		GPIO.setup(self.green2_pin, GPIO.OUT)
		GPIO.setup(self.blue2_pin, GPIO.OUT)
		GPIO.setup(self.clock_pin, GPIO.OUT)
		GPIO.setup(self.a_pin, GPIO.OUT)
		GPIO.setup(self.b_pin, GPIO.OUT)
		GPIO.setup(self.c_pin, GPIO.OUT)
		GPIO.setup(self.latch_pin, GPIO.OUT)
		GPIO.setup(self.oe_pin, GPIO.OUT)
		self.MATRIX_W = 96
		self.MATRIX_H = 16
		self.screen = [[0 for x in range(self.MATRIX_W)] for x in range(self.MATRIX_H)]
		self.font_margins_es = []
		self.font_margins_ru = []
		self.font_margins_uz = []
		self.font_margins_bn = []
		self.FONT_W = 12
		#scroll timing
		self.scrolling = False
		self.start = time.time()
		self.elapse = 0.01
		self.init_font_margin_lists()
		self.get_font_margins("es")
		self.get_font_margins("ru")
		self.get_font_margins("uz")
		self.get_font_margins("bn")

	def init_font_margin_lists(self):
		for i in range(len(letter_bitmaps_es)):
			self.font_margins_es.append(0)
		for i in range(len(letter_bitmaps_ru)):
			self.font_margins_ru.append(0)
		for i in range(len(letter_bitmaps_uz)):
			self.font_margins_uz.append(0)
		for i in range(len(letter_bitmaps_bn)):
			self.font_margins_bn.append(0)

	def get_font_margins(self, language):
		if language == "es":
			bitmaps = letter_bitmaps_es
			margins = self.font_margins_es
		elif language == "ru":
			bitmaps = letter_bitmaps_ru
			margins = self.font_margins_ru
		elif language == "uz":
			bitmaps = letter_bitmaps_uz
			margins = self.font_margins_uz
		elif language == "bn":
			bitmaps = letter_bitmaps_bn
			margins = self.font_margins_bn
		if language == "bn":
			for i in range(len(bitmaps)):
				index = 0
				min = 8
				for row in range(16):
					for col in range(16):
						if col < min and bitmaps[i][index] == 1:
							min = col
						index += 1
				margins[i] = min
		else:
			for i in range(len(bitmaps)):
				index = 0
				min = 8
				for row in range(16):
					for col in range(12):
						if col < min and bitmaps[i][index] == 1:
							min = col
						index += 1
				margins[i] = min

	def clock(self):
		GPIO.output(self.clock_pin, 1)
		GPIO.output(self.clock_pin, 0)

	def latch(self):
		GPIO.output(self.latch_pin, 1)
		GPIO.output(self.latch_pin, 0)

	def bits_from_int(self,x):
		a_bit = x & 1
		b_bit = x & 2
		c_bit = x & 4
		return (a_bit, b_bit, c_bit)

	def set_row(self,row):
		#time.sleep(self.delay)
		a_bit, b_bit, c_bit = self.bits_from_int(row)
		GPIO.output(self.a_pin, a_bit)
		GPIO.output(self.b_pin, b_bit)
		GPIO.output(self.c_pin, c_bit)
		#time.sleep(delay)

	def set_color_top(self,color):
		#time.sleep(self.delay)
		red, green, blue = self.bits_from_int(color)
		GPIO.output(self.red1_pin, red)
		GPIO.output(self.green1_pin, green)
		GPIO.output(self.blue1_pin, blue)
		#time.sleep(delay)

	def set_color_bottom(self,color):
		#time.sleep(self.delay)
		red, green, blue = self.bits_from_int(color)
		GPIO.output(self.red2_pin, red)
		GPIO.output(self.green2_pin, green)
		GPIO.output(self.blue2_pin, blue)
		#time.sleep(delay)

	def refresh(self):
		for row in range(8):
			GPIO.output(self.oe_pin, 1)
			self.set_color_top(0)
			self.set_row(row)
			#time.sleep(self.delay)
			for col in range(self.MATRIX_W):
				self.set_color_top(self.screen[row][col])
				self.set_color_bottom(self.screen[row+8][col])
				self.clock()
			#GPIO.output(self.oe_pin, 0)
			self.latch()
			GPIO.output(self.oe_pin, 0)
			time.sleep(self.delay*500) #increasing delay reduces middle line

	def fill_rectangle(self,x1, y1, x2, y2, color):
		for x in range(x1, x2):
			for y in range(y1, y2):
				self.screen[y][x] = color

	def set_pixel(self,x, y, color):
		self.screen[y][x] = color

	def clear(self):
		self.fill_rectangle(0, 0, self.MATRIX_W, self.MATRIX_H, 0)

	def show_letter(self,x, which_letter,color, language):
		which_bitmap = 0
		letters = ""
		letter_bitmaps = ""
		if language == "es":
			letters = letters_es
			letter_bitmaps = letter_bitmaps_es
			self.FONT_W = 12
		elif language == "ru":
			letters = letters_ru
			letter_bitmaps = letter_bitmaps_ru
			self.FONT_W = 12
		elif language == "uz":
			letters = letters_uz
			letter_bitmaps = letter_bitmaps_uz
			self.FONT_W = 12
		elif language == "bn":
			letters = letters_bn
			letter_bitmaps = letter_bitmaps_bn
			self.FONT_W = 16

		for key in letters:
			if which_letter == letters[key]:
				which_bitmap = key
				break
		index = 0
		for row in range(self.MATRIX_H):
			for col in range(x, x + self.FONT_W):
				if letter_bitmaps[which_bitmap][index]:
					if col < self.MATRIX_W and col >= 0:
						self.set_pixel(col, row, color)
				index += 1

	def scroll_text(self,name,color):
		language = ""
		self.scrolling = True
		xpos = self.MATRIX_W
		new_text= []
		message = ""
		try:
			with open('print.txt', 'r') as rf:
				new_text = rf.readlines()
				if len(new_text) > 0:
					language = new_text[0].strip('\n')
					message = new_text[1].strip('\n')
		except IOError:
			print("Error: read print inaccessible.")
		try:
			with open('print.txt', 'w') as wf:
				wf.writelines(new_text[2:])
		except IOError:
			print("Error: write print inaccessible")

		grid_width = self.FONT_W * len(message)
		margins = 0
		margins_list = []
		letters = ""
		font_margins = ""
		if language == "es":
			letters = letters_es
			font_margins = self.font_margins_es
			self.FONT_W = 12
		elif language == "ru":
			letters = letters_ru
			font_margins = self.font_margins_ru
			self.FONT_W = 12
		elif language == "uz":
			letters = letters_uz
			font_margins = self.font_margins_uz
			self.FONT_W = 12
		elif language == "bn":
			letters = letters_bn
			font_margins = self.font_margins_bn
			self.FONT_W = 16
		for char in message:
			for key in letters:
				if char == letters[key]:
					margins += font_margins[key]
					margins_list.append(font_margins[key])
					break
		message_width = grid_width - margins
		if len(message) > 0:
			while xpos >= -message_width - self.FONT_W:
				self.clear()
				x = xpos
				index = 0
				for char in message:
					self.show_letter(x, char, color, language)
					if language == "bn":
						x += self.FONT_W - margins_list[index] * 2
					else:
						x += self.FONT_W - margins_list[index]
				if time.time() > self.start + self.elapse:
					xpos -= 1
					self.start = time.time()
				self.refresh()
			self.clear()
		self.scrolling = False

	def scroll_text_test(self,color,language,message):
		self.scrolling = True
		xpos = self.MATRIX_W
		grid_width = self.FONT_W * len(message)
		margins = 0
		margins_list = []
		letters = ""
		font_margins = ""
		if language == "es":
			letters = letters_es
			font_margins = self.font_margins_es
			self.FONT_W = 12
		elif language == "ru":
			letters = letters_ru
			font_margins = self.font_margins_ru
			self.FONT_W = 12
		elif language == "uz":
			letters = letters_uz
			font_margins = self.font_margins_uz
			self.FONT_W = 12
		elif language == "bn":
			letters = letters_bn
			font_margins = self.font_margins_bn
			self.FONT_W = 16
		for char in message:
			for key in letters:
				if char == letters[key]:
					margins += font_margins[key]
					margins_list.append(font_margins[key])
					break
		message_width = grid_width - margins
		while xpos >= -message_width - self.FONT_W:
			self.clear()
			x = xpos
			index = 0
			for char in message:
				self.show_letter(x, char, color, language)
				if language == "bn":
					x += self.FONT_W - margins_list[index] * 2
				else:
					x += self.FONT_W - margins_list[index]
				index += 1
			if time.time() > self.start + self.elapse:
				xpos -= 1
				self.start = time.time()
				self.refresh()
		self.clear()
		self.scrolling = False

	def get_scrolling_state(self):
		return self.scrolling
