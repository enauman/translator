import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
path = '/home/translator/app/'
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
	# some colors not used, rgb led common positive so 0 is on, 1 is off
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

	def led_off(self):
		GPIO.output(self.red_pin, 1)
		GPIO.output(self.green_pin, 1)
		GPIO.output(self.blue_pin, 1)
	#pushing yellow button purges print file contents to end scrolling for new translations
	def purge(self, channel):
		self.set_led_color(7)
		try:
			open(path + "print.txt", 'w').close()
		except IOError as e:
			print("purge error", e)
		time.sleep(1)
		self.set_led_color(2)

	def event_detect(self):
		GPIO.add_event_detect(self.button,GPIO.FALLING,callback=self.purge, bouncetime=500)
