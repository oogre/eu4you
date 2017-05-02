#!/usr/bin/python

import time
from pygame import mixer # Load the required library


class soundPlayer:
	def __init__(self, name, filename):
		self.name = name
		self.exitFlag = True
		self.filename = filename
		self.mixer = mixer
		self.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
	def start(self):
		self.exitFlag = False
		self.mixer.music.load(self.filename)
		self.mixer.music.play()

	def stop(self):
		self.exitFlag = True
		self.mixer.quit()