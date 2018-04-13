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

class EuForYou:
    def __init__ (self):
        logging.basicConfig(filename="../eu4you.log", filemode='a',
                                    format='%(asctime)s %(levelname)s %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S',
                                    level=logging.DEBUG)

        logging.info("start")
        print("Starting initialising EuForYou...")

        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open('/home/pi/bitrepublic/eu4you/config.cfg'))
        self.configJs = json.load(open('/home/pi/bitrepublic/Config.json'))                                                    #added by iGor for the post request to create Bitsoils
        self.address = self.configJs["requests"]["genBitSoil"]["Address"]                                                      #getting the address from the config
        
        self.USReader = ultrasonicSensorReader("USReader", json.loads(self.config.get("sensor", "pins")), self.config.getint("sensor", "dist_limit"), grovepi)
        self.USReader.start()
        self.isActive = False
        self.wasActive = False

        self.buzz = buzzer("buzz", self.config.getint("buzzer", "pin"), grovepi)
        self.buzz_start_defered = self.config.getfloat("buzzer", "activation_time")
        self.buzz_stop_defered = self.config.getfloat("buzzer", "disactivation_time")
        self.buzz_start_at = 0
        self.buzz_stop_at = 0

        self.sPlayer = soundPlayer("sPlayer", "../"+self.config.get("soundPlayer", "filename"))
        self.sPlayer_start_defered = self.config.getfloat("soundPlayer", "activation_time")
        self.sPlayer_start_at = 0

        self.perfume = relay("perfume", self.config.getint("perfume", "pin"), grovepi)
        self.perfume_start_defered = self.config.getfloat("perfume", "activation_time") 
        self.perfume_duration = self.config.getfloat("perfume", "activation_duration") 
        self.perfume_stop_defered = self.config.getfloat("perfume", "disactivation_time")
        self.perfume_start_at = 0
        self.perfume_stop_at = 0

    def run(self, headers):
        print("Running EuForYou...")
        while True:
            try:
                self.buzz.buzzLoop()
                print("1")
                self.USReader.readLoop()

                self.t = time.time()
                print("2")
                self.isActive = self.USReader.readStatus()
                if self.isActive != self.wasActive:
                    if self.isActive :
                        print("Trying to create Bitsoil...")
                        logging.info("activation")
                        self.buzz_start_at = t + buzz_start_defered
                        self.perfume_start_at = t + perfume_start_defered
                        if self.perfume_duration != 0 :
                            self.perfume_stop_at = t + self.perfume_duration
                        self.sPlayer_start_at = t + self.sPlayer_start_defered
                        
                        self.r = requests.post(self.address, headers=headers)                          #send the post request.
                        if self.r.status_code == 200:
                            self.jdata = self.r.json()
                            print(self.jdata)
                        else:
                            print(self.r)
                            
                    else :
                        print("No movement detected")
                        logging.info("disactivation")
                        self.buzz_stop_at = t + self.buzz_stop_defered
                        self.perfume_stop_at = t + self.perfume_stop_defered

                if self.buzz_start_at != 0 and self.buzz_start_at < t :
                    self.buzz_start_at = 0
                    buzz.start()

                if self.buzz_stop_at != 0 and self.buzz_stop_at < t :
                    self.buzz_stop_at = 0
                    buzz.stop()

                if self.sPlayer_start_at != 0 and self.sPlayer_start_at < t :
                    self.sPlayer_start_at = 0
                    sPlayer.start()

                if self.perfume_start_at != 0 and self.perfume_start_at < t :
                    self.perfume_start_at = 0
                    perfume.start()

                if self.perfume_stop_at != 0 and self.perfume_stop_at < t :
                    self.perfume_stop_at = 0
                    perfume.stop()

                self.wasActive = self.isActive
            except KeyboardInterrupt :
                print("KeyboardInterrupt")
                logging.info("KeyboardInterrupt") 
                break        
            except TypeError:
                print("TypeError")
                logging.error("TypeError") 
                break
            except IOError:
                print("IOError")
                logging.error("IOError") 
                break

        self.USReader.stop()
        self.perfume.stop()
        self.buzz.stop()
        logging.info("stop") 
        time.sleep(1.0)