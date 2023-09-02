import os
import threading
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
from voice_service import Voice_Service
from color_selector import Color_Selector
from language_selector import Language_Selector
cs = Color_Selector()
ls = Language_Selector()
vs = Voice_Service(True) #initialize w 'running=True'
language = ls.get_language()
ctrl_btn = 12
GPIO.setup(ctrl_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
scrolling = False

def clean_logs():
	try:
		os.remove('buffer.txt')
		os.remove('op.txt')
		os.remove('translator.log')
	except OSError as e:
		print(e)
	with open('print.txt','w') as wf:
		wf.write("")
	with open('translated.txt', 'w') as wf:
		wf.write("")
	with open('missing.txt', 'w') as wf:
		wf.write("")

def scroll_text(name, color):
	global scrolling
	scrolling = True
	language = ""
	message = ""
	rgb_color = ""
	font_path = ""
	temp_text= []
	try:
		with open('print.txt', 'r') as rf:
			temp_text = rf.readlines()
			if len(temp_text) > 0:
				language = temp_text[0].strip('\n')
				message = temp_text[1].strip('\n')
				message = message.replace("'", "\\'")
	except IOError as e:
		print(e)
	try:
		with open('print.txt', 'w') as wf:
			wf.writelines(temp_text[2:])
	except IOError as e:
		print(e)

	if color == 1:
		rgb_color = "255,0,0"
	elif color == 2:
		rgb_color = "0,255,0"
	elif color == 3:
		rgb_color = "255,255,0"
	elif color == 4:
		rgb_color = "0,0,255"
	elif color == 5:
		rgb_color = "255,0,255"
	elif color == 6:
		rgb_color = "0,255,255"
	elif color == 7:
		rgb_color = "255,255,255"

	if language == "es":
		font_path = "/home/translator/app/rpi-rgb-led-matrix/fonts/ABeeZee.bdf"
	elif language == "ru":
		font_path = "/home/translator/app/rpi-rgb-led-matrix/fonts/Arimo.bdf"
	elif language == "uz":
		font_path = "/home/translator/app/rpi-rgb-led-matrix/fonts/9x15.bdf"
	elif language == "bn":
		font_path = "/home/translator/app/rpi-rgb-led-matrix/fonts/Bengali.bdf"

	function_call_path = "/home/translator/app/rpi-rgb-led-matrix/examples-api-use/scrolling-text-example"
	if not font_path == "" and not message == "":
		system_call = "sudo " + function_call_path + " --led-rows=16 --led-chain=3 --led-slowdown-gpio=2 -l 1 -s 5 -f " + font_path + " -C " + rgb_color + " " + message
		print("start scrolling " + message)
		os.system(system_call)
		print("end scroll")
	scrolling = False

if __name__ == "__main__":
	clean_logs()
	cs.event_detect()
	while vs.running:
		if GPIO.input(ctrl_btn) == GPIO.HIGH:
			ls.set_language()
			cs.set_led_color(cs.color)
			language = ls.get_language()
			if not vs.get_listening_state():
				vs.listen(language)
			if not scrolling:
				scroll = threading.Thread(target=scroll_text, args=(1,cs.get_led_color()), daemon=True)
				scroll.start()
		else:
			if not scrolling:
				cs.led_off()

	cs.led_off()
	print("shutting down")
