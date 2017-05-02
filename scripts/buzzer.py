#!/usr/bin/python

import time


class buzzer:
	def __init__(self, name, pin, grovepi):
		self.name = name
		self.pin = pin
		self.grovepi = grovepi
		self.exitFlag = True
		self.OnTime = 2
		self.OffTime = 1
		self.grovepi.pinMode(self.pin,"OUTPUT")

	def start(self):
		self.exitFlag = False

	def stop(self):
		self.exitFlag = True
		self.grovepi.digitalWrite(self.pin,0)
	
	def buzzLoop(self):
		if not self.exitFlag :
			t = time.time()
			if self.OnTime < t and self.OffTime < self.OnTime: 
				self.grovepi.digitalWrite(self.pin,1)
				self.OffTime = t + 0.2

			if self.OffTime < t and self.OnTime < self.OffTime: 
				self.grovepi.digitalWrite(self.pin,0)
				self.OnTime = t + 0.2
		else :
			self.grovepi.digitalWrite(self.pin,0)