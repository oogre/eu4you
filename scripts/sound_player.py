import time
import grovepi
import socket

buzzer = 8

HOST = "127.0.0.1" 	# Get local machine name
PORT = 12345        # Reserve a port for your service.

isActive = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

grovepi.pinMode(buzzer,"OUTPUT")

while True:
	try:
		data = s.recv(1024)
		if data == "ACTIVATION" :
			isActive = True
			print("active")
		elif data == "DISACTIVATION" :
			isActive = False
			print("disactive")
	except KeyboardInterrupt :
		break        
	except TypeError:
		print "Error1"
	except IOError:
		print "Error2"
s.close()
