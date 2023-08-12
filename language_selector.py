import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
class Language_Selector:
	def __init__(self):
		self.pole0 = 5
		self.pole1 = 6
		self.pole2 = 20
		self.pole3 = 21
		GPIO.setup(self.pole0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.pole1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.pole2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.pole3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self.language = "es"
		self.set_language()

	def get_language(self):
		return self.language

	def set_language(self):
		if GPIO.input(self.pole0) == GPIO.HIGH:
			self.language = "es"
		elif GPIO.input(self.pole1) == GPIO.HIGH:
			self.language = "ru"
		elif GPIO.input(self.pole2) == GPIO.HIGH:
			self.language = "uz"
		elif GPIO.input(self.pole3) == GPIO.HIGH:
			self.language = "bn"
