import os
import threading
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
from rgb_matrix import RGB_MATRIX
from voice_service import Voice_Service
from color_selector import Color_Selector
from language_selector import Language_Selector
cs = Color_Selector()
ls = Language_Selector()
matrix = RGB_MATRIX()
vs = Voice_Service(True) #initialize w 'running=True'
language = ls.get_language()
ctrl_btn = 12
GPIO.setup(ctrl_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def clean_logs():
	matrix.clear()
	matrix.refresh()
	try:
		os.remove('buffer.txt')
		os.remove('op.txt')
	except OSError as e:
		print(e)
	with open('print.txt','w') as wf:
		wf.write("")
	with open('translated.txt', 'w') as wf:
		wf.write("")
	with open('missing.txt', 'w') as wf:
		wf.write("")

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
			if not matrix.get_scrolling_state():
				scroll = threading.Thread(target=matrix.scroll_text, args=(1,cs.get_led_color()), daemon=True)
				scroll.start()
		else:
			cs.led_off()
			matrix.clear()
			matrix.refresh()
	matrix.clear()
	matrix.refresh()
	cs.led_off()
	print("shutting down")
