from ev3dev.ev3 import *

class Ev3devSetup:
	def __init__(self):
		MAX_SENSOR = 100.0 # percent
		MAX_MOTOR = 1000.0

		BIAS = 0.05
		SENSOR_GAIN = 1.0
		OUTPUT_GAIN = 1.0

	def initLargeMotor(self, motorname):
		return LargeMotor(motorname)

	def initColorSensor(self, sensorname):
		return ColorSensor(sensorname)

	def initUltraSonicSensor(self, sensorname):
		return UltrasonicSensor(sensorname)