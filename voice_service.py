import os
import speech_recognition as sr
import threading
from language_selector import Language_Selector
ls = Language_Selector()
r = sr.Recognizer()
r.pause_threshold = 0.8
r.energy_threshold = 4000
r.dynamic_energy_threshold = True
#r.operation_timeout = 2.0
mic = sr.Microphone(device_index=0)
class Voice_Service:
	def __init__(self,running):
		self.index = 0
		self.running = running
		self.audio = ""
		self.transcription = []
		self.buffer = ""
		self.listening = False

	def get_listening_state(self):
		return self.listening

	def listen(self,language):
		self.listening = True
		try:
			with mic as source:
				r.adjust_for_ambient_noise(source, duration = 0.5)
				self.audio = r.listen(source, timeout = 1.0)
			translate = threading.Thread(target=self.transcribe, args=(1,language), daemon=True)
			translate.start()
			# self.transcribe(language)
		except sr.WaitTimeoutError as e:
			print(e)
		self.listening = False

	def transcribe(self,name,language):
		text = "..."
		try:
#			text = r.recognize_google_cloud(self.audio, credentials_json="/home/translator/app/application_default_credentials.json")
			text = r.recognize_google(self.audio)
			if text == "shut down":
				self.running = False
		except sr.UnknownValueError:
			text = "could not recognize"
		finally:
			print(text)
		if text != "could not recognize":
			self.transcription.append(text)
			try:
				with open('translated.txt', 'a') as af:
					af.writelines(self.transcription[self.index])
					af.write("\n")
				self.line_to_buffer(language)
			except IOError as e:
				print(e)

	def line_to_buffer(self,language):
		self.buffer = self.transcription[self.index]
		try:
			with open('buffer.txt', 'w') as wf:
				wf.write(self.buffer)
		except IOError as e:
			print(e)
		self.translate_to_output(language)

	def translate_to_output(self,language):
		lines = []
		if language == "es":
			os.system("trans :es file://buffer.txt -o op.txt")
		elif language == "ru":
			os.system("trans :ru file://buffer.txt -o op.txt")
		elif language == "uz":
			os.system("trans :uz file://buffer.txt -o op.txt")
		elif language == "bn":
			os.system("trans :bn file://buffer.txt -o op.txt")

		self.index += 1
		try:
			with open('op.txt', 'r') as rf:
				lines = rf.readlines()
				print(lines)
			with open('translated.txt', 'a') as af:
				af.writelines(lines)
		except IOError as e:
			print(e)
		try:
			with open('print.txt', 'a') as af:
				af.write(language)
				af.write('\n')
				af.writelines(lines)
		except IOError as e:
			print(e)
