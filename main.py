import os
import threading
import time
from rgb_matrix import RGB_MATRIX
from voice_service import Voice_Service
from color_selector import Color_Selector
from language_selector import Language_Selector
cs = Color_Selector()
ls = Language_Selector()
matrix = RGB_MATRIX()
vs = Voice_Service(True) #initialize w 'running=True'
language = ls.get_language()

def clean_logs():
	try:
		os.remove('buffer.txt')
		os.remove('op.txt')
	except OSError:
		pass
	with open('transcribe.txt','w') as wf:
		wf.write("")
	with open('print.txt','w') as wf:
		wf.write("")
	with open('translated.txt', 'w') as wf:
		wf.write("")

if __name__ == "__main__":
	clean_logs()
	cs.event_detect()
	ls.event_detect()
	while vs.running:
		language = ls.get_language()
		if not vs.get_listening_state():
			vs.listen(language)
		if not matrix.get_scrolling_state():
			scroll = threading.Thread(target=matrix.scroll_text, args=(1,cs.get_led_color()), daemon=True)
			scroll.start()
	matrix.clear()
	cs.led_off()
	print("shutting down")
