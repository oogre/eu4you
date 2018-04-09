#!/usr/bin/python

import ConfigParser
import json
import grovepi
import time
import requests
import logging

from ultrasonicSensorReader import *
from buzzer import *
from soundPlayer import *
from relay import *


logging.basicConfig(filename="../eu4you.log", filemode='a',
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

logging.info("start") 

config = ConfigParser.ConfigParser()
config.readfp(open('../config.cfg'))
config = json.load(open('/home/pi/bitrepublic/Config.json'))                                                    #added by iGor for the post request to create Bitsoils
address = config["requests"]["genBitSoil"]["Address"]                                                           #getting the address from the config

USReader = ultrasonicSensorReader("USReader", json.loads(config.get("sensor", "pins")), config.getint("sensor", "dist_limit"), grovepi)
USReader.start()
isActive = False
wasActive = False

buzz = buzzer("buzz", config.getint("buzzer", "pin"), grovepi)
buzz_start_defered = config.getfloat("buzzer", "activation_time")
buzz_stop_defered = config.getfloat("buzzer", "disactivation_time")
buzz_start_at = 0
buzz_stop_at = 0

sPlayer = soundPlayer("sPlayer", "../"+config.get("soundPlayer", "filename"))
sPlayer_start_defered = config.getfloat("soundPlayer", "activation_time")
sPlayer_start_at = 0

perfume = relay("perfume", config.getint("perfume", "pin"), grovepi)
perfume_start_defered = config.getfloat("perfume", "activation_time") 
perfume_duration = config.getfloat("perfume", "activation_duration") 
perfume_stop_defered = config.getfloat("perfume", "disactivation_time")
perfume_start_at = 0
perfume_stop_at = 0

while True:
	try:
		buzz.buzzLoop()
		USReader.readLoop()
		
		t = time.time()
		isActive = USReader.readStatus()
		if isActive != wasActive:
			if isActive :
				logging.info("activation")
				buzz_start_at = t + buzz_start_defered
				perfume_start_at = t + perfume_start_defered
				if perfume_duration != 0 :
					perfume_stop_at = t + perfume_duration
				sPlayer_start_at = t + sPlayer_start_defered
                
                createBitsoil()
			else :
				logging.info("disactivation")
				buzz_stop_at = t + buzz_stop_defered
				perfume_stop_at = t + perfume_stop_defered

		if buzz_start_at != 0 and buzz_start_at < t :
			buzz_start_at = 0
			buzz.start()

		if buzz_stop_at != 0 and buzz_stop_at < t :
			buzz_stop_at = 0
			buzz.stop()

		if sPlayer_start_at != 0 and sPlayer_start_at < t :
			sPlayer_start_at = 0
			sPlayer.start()

		if perfume_start_at != 0 and perfume_start_at < t :
			perfume_start_at = 0
			perfume.start()

		if perfume_stop_at != 0 and perfume_stop_at < t :
			perfume_stop_at = 0
			perfume.stop()

		wasActive = isActive
	except KeyboardInterrupt :
		logging.info("KeyboardInterrupt") 
		break        
	except TypeError:
		logging.error("TypeError") 
		break
	except IOError:
		logging.error("IOError") 
		break

USReader.stop()
perfume.stop()
buzz.stop()
logging.info("stop") 
time.sleep(1.0)