import os
import threading
import time
import RPi.GPIO as GPIO
import requests
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
from voice_service import Voice_Service
from color_selector import Color_Selector
from language_selector import Language_Selector
cs = Color_Selector()
ls = Language_Selector()
vs = Voice_Service(True) #initialize w 'running=True'
language = ls.get_language()
ctrl_btn = 12 #start and stop voice service
GPIO.setup(ctrl_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
scrolling = False
path = '/home/translator/app/' #full path needed for running as root
timeout = 1 #for connection request

def clean_logs():
	global path
	files = ['buffer.txt','op.txt','translator.log','print.txt','translated.txt','missing.txt']
	"""
	buffer.txt = single string to translate-shell
	op.txt = translated output from translate-shell
	translator.log = terminal output from session
	print.txt = appended strings to scroll
	translated.txt = full transcript (Eng target langs) of session
	missing.txt = any characters missing from font sets (no longer used?)
	"""
	for file in files:
		if file == 'translator.log':
			text = []
			# copy contents of translator.log to translator_old.log
			try:
				with open(path + file, 'r') as rf:
					text = rf.readlines()
				open(path + file, 'w').close()
			except IOError as e:
				print(e)
			try:
				with open(path + 'translator_old.log', 'w') as wf:
					wf.writelines(text)
			except IOError as e:
				print(e)
		elif file == 'translated.txt':
			text = []
			# copy contents of translated.txt to translated_old.txt
			try:
				with open(path + file, 'r') as rf:
					text = rf.readlines()
				open(path + file, 'w').close()
			except IOError as e:
				print(e)
			try:
				with open(path + 'translated_old.txt', 'w') as wf:
					wf.writelines(text)
			except IOError as e:
				print(e)
		else:
			# overwrite contents of remaining files
			try:
				open(path + file, 'w').close()
			except IOError as e:
				print(e)

def scroll_text(name):
	global scrolling, path
	scrolling = True
	language = ""
	message = ""
	rgb_color = "255,0,0"
	font_path = ""
	speed = "3" #default speed
	temp_text= []
	try:
		# read lines from print, 1st line is language, 2nd is text
		with open(path + 'print.txt', 'r') as rf:
			temp_text = rf.readlines()
			if len(temp_text) > 1:
				language = temp_text[0].strip('\n')
				message = temp_text[1].strip('\n')
				message = message.replace("'", "\\'") #escape single quotes in string
	except IOError as e:
		print(e)
	try:
		# write back everything except 1st 2 lines to print
		with open(path + 'print.txt', 'w') as wf:
			wf.writelines(temp_text[2:])
	except IOError as e:
		print(e)
	#set font to use for each language, and adjust speed if needed
	if language == "es":
		font_path = "/home/translator/app/rpi-rgb-led-matrix/fonts/ABeeZee.bdf"
	elif language == "ru":
		font_path = "/home/translator/app/rpi-rgb-led-matrix/fonts/Arimo.bdf"
	elif language == "uz":
		font_path = "/home/translator/app/rpi-rgb-led-matrix/fonts/9x15.bdf"
		speed = "5"
	elif language == "bn":
		font_path = "/home/translator/app/rpi-rgb-led-matrix/fonts/Bengali.bdf"
	# system call to rpi-rgb-led-matrix command with flags, this is where the scrolling happens
	function_call_path = "/home/translator/app/rpi-rgb-led-matrix/examples-api-use/scrolling-text-example"
	if not font_path == "" and not message == "":
		system_call = "sudo " + function_call_path + " --led-rows=16 --led-chain=3 --led-slowdown-gpio=2 -l 1 -s " + speed + " -f " + font_path + " -C " + rgb_color + " " + message
		os.system(system_call)
	scrolling = False

def is_cnx_active(timeout):
    try:
        requests.head("http://www.google.com/", timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
	
if __name__ == "__main__":
	clean_logs()
	cs.event_detect() #detect yellow button press
	# check internet connection
	while True:
		if is_cnx_active(timeout) == True:
			cs.set_led_color(2)
			break
		else:
			# blink red if not active connection
			cs.set_led_color(1)
			time.sleep(0.5)
			cs.led_off()
			time.sleep(0.5)
	# connection successful, start run loop
	while vs.running:
		if GPIO.input(ctrl_btn) == GPIO.HIGH: # if green control button is down 
			ls.set_language()
			language = ls.get_language()
			cs.set_led_color(2)
			# if not listening, start listening
			if not vs.get_listening_state():
				vs.listen(language)
			# if not scrolling start scrolling (as thread)
			if not scrolling:
				scroll = threading.Thread(target=scroll_text, args=(1,), daemon=True)
				scroll.start()
		else:
			#if control button is up wait from scrolling to finish and stop listening & scrollign
			cs.set_led_color(1)
	# can say "shut down" to end run loop
	cs.led_off()
	print("shutting down")
