import os
import speech_recognition as sr
import threading
import time
r = sr.Recognizer()
r.pause_threshold = 0.8
r.energy_threshold = 4000
r.dynamic_energy_threshold = True
#r.operation_timeout = 1
mic = sr.Microphone(device_index=0)
path = '/home/translator/app/'

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
			#listen until pause
			with mic as source:
				r.adjust_for_ambient_noise(source, duration = 0.5)
				self.audio = r.listen(source, timeout = 0.5)
			#start transcription and translation as thread, go back to listen again
			translate = threading.Thread(target=self.transcribe, args=(1,language), daemon=True)
			translate.start()
		except sr.WaitTimeoutError as e:
			print(e)
		self.listening = False

	def transcribe(self,name,language):
		global path
		text = "..."
		try:
			#recognize_google_cloud supposed to be for production but not as good?
#			text = r.recognize_google_cloud(self.audio, credentials_json="/home/translator/app/application_default_credentials.json")
			text = r.recognize_google(self.audio)
			if text == "shut down":
				self.running = False
		except sr.UnknownValueError:
			text = "could not recognize"
		finally:
			print(text)
		#if speech recognized add to transcription list and full transcription file 
		if text != "could not recognize":
			self.transcription.append(text)
			try:
				with open(path + 'translated.txt', 'a') as af:
					af.writelines(self.transcription[self.index])
					af.write("\n")
				self.line_to_buffer(language)
			except IOError as e:
				print(e)

	def line_to_buffer(self,language):
		global path
		# index keeps track of which transcription line to send to buffer 
		# index increments after translation is done
		self.buffer = self.transcription[self.index]
		try:
			with open(path + 'buffer.txt', 'w') as wf:
				wf.write(self.buffer)
		except IOError as e:
			print(e)
		self.translate_to_output(language)

	def translate_to_output(self,language):
		global path
		lines = []
		#system call to translate-shell; input is buffer.txt, output to op.txt
		if language == "es":
			os.system("trans :es file:///home/translator/app/buffer.txt -o /home/translator/app/op.txt")
		elif language == "ru":
			os.system("trans :ru file:///home/translator/app/buffer.txt -o /home/translator/app/op.txt")
		elif language == "uz":
			os.system("trans :uz file:///home/translator/app/buffer.txt -o /home/translator/app/op.txt")
		elif language == "bn":
			os.system("trans :bn file:///home/translator/app/buffer.txt -o /home/translator/app/op.txt")
		#increment index to get next line to translate on next pass
		self.index += 1
		try:
			#add translation to full transcript
			with open(path + 'op.txt', 'r') as rf:
				lines = rf.readlines()
				print(lines)
			with open(path + 'translated.txt', 'a') as af:
				af.writelines(lines)
		except IOError as e:
			print(e)
		try:
			# add line to be printed to matrix
			with open(path + 'print.txt', 'a') as af:
				af.write(language)
				af.write('\n')
				af.writelines(lines)
		except IOError as e:
			print(e)
