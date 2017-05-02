#!/usr/bin/python


class ultrasonicSensorReader :
	def __init__(self, name, sensor_pins, dist_limit, grovepi):
		self.name = name
		self.sensor_pins = sensor_pins
		self.dist_limit = dist_limit
		self.dists = []
		self.distSmooth = []
		self.isActive = False
		for i in enumerate(sensor_pins):
			self.dists.append(0)
			self.distSmooth.append(0)
		self.exitFlag = True
		self.grovepi = grovepi
	
	def start(self):
		self.exitFlag = False
	
	def stop(self):
		self.exitFlag = True
	
	def readLoop(self):
		if not self.exitFlag :
			active = False
			for i, pin in enumerate(self.sensor_pins):
				self.dists[i] = self.grovepi.ultrasonicRead(pin)
				if self.dists[i] is not False :
					self.distSmooth[i] = int(round(self.dists[i]*0.5 + self.distSmooth[i]*0.5))
					active |= self.distSmooth[i] <= self.dist_limit
			self.isActive = active
	
	def readStatus(self):
		return self.isActive