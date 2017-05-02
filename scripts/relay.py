#!/usr/bin/python

class relay:
	def __init__(self, name, pin, grovepi):
		self.name = name
		self.pin = pin
		self.grovepi = grovepi
		self.exitFlag = True
		self.grovepi.pinMode(self.pin,"OUTPUT")

	def start(self):
		self.grovepi.digitalWrite(self.pin,1)

	def stop(self):
		self.grovepi.digitalWrite(self.pin,0)
	