import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
class Color_Selector:
	def __init__(self):
		self.red_pin = 13
		self.green_pin = 19
		self.blue_pin = 26
		self.button = 16
		GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.red_pin, GPIO.OUT)
		GPIO.setup(self.green_pin, GPIO.OUT)
		GPIO.setup(self.blue_pin, GPIO.OUT)
		self.color = 1
		self.set_led_color(self.color)
	def get_led_color(self):
		return self.color
	def set_led_color(self,color):
		if color == 1:
			GPIO.output(self.red_pin, 0)
			GPIO.output(self.green_pin, 1)
			GPIO.output(self.blue_pin, 1)
		elif color == 2:
			GPIO.output(self.red_pin, 1)
			GPIO.output(self.green_pin, 0)
			GPIO.output(self.blue_pin, 1)
		elif color == 3:
			GPIO.output(self.red_pin, 0)
			GPIO.output(self.green_pin, 0)
			GPIO.output(self.blue_pin, 1)
		elif color == 4:
			GPIO.output(self.red_pin, 1)
			GPIO.output(self.green_pin, 1)
			GPIO.output(self.blue_pin, 0)
		elif color == 5:
			GPIO.output(self.red_pin, 0)
			GPIO.output(self.green_pin, 1)
			GPIO.output(self.blue_pin, 0)
		elif color == 6:
			GPIO.output(self.red_pin, 1)
			GPIO.output(self.green_pin, 0)
			GPIO.output(self.blue_pin, 0)
		elif color == 7:
			GPIO.output(self.red_pin, 0)
			GPIO.output(self.green_pin, 0)
			GPIO.output(self.blue_pin, 0)
	def change_color(self, channel):
		self.color += 1
		if self.color > 7: self.color = 1
		self.set_led_color(self.color)
	def led_off(self):
		GPIO.output(self.red_pin, 1)
		GPIO.output(self.green_pin, 1)
		GPIO.output(self.blue_pin, 1)
	def event_detect(self):
		GPIO.add_event_detect(self.button,GPIO.FALLING,callback=self.change_color, bouncetime=500)

