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
		self.language_init()

	def language_init(self):
		if GPIO.input(self.pole0):
			self.language = "es"
		elif GPIO.input(self.pole1):
			self.language = "ru"
		elif GPIO.input(self.pole2):
			self.language = "uz"
		elif GPIO.input(self.pole3):
			self.language = "bn"

	def get_language(self):
		return self.language

	def set_language(self, which_pole):
		if which_pole == 0:
			self.language = "es"
		elif which_pole == 1:
			self.language = "ru"
		elif which_pole == 2:
			self.language = "uz"
		elif which_pole == 3:
			self.language = "bn"

	def event_detect(self):
		GPIO.add_event_detect(self.pole0,GPIO.RISING,callback=lambda x: self.set_language(0))
		GPIO.add_event_detect(self.pole1,GPIO.RISING,callback=lambda x: self.set_language(1))
		GPIO.add_event_detect(self.pole2,GPIO.RISING,callback=lambda x: self.set_language(2))
		GPIO.add_event_detect(self.pole3,GPIO.RISING,callback=lambda x: self.set_language(3))