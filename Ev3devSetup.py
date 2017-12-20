from ev3dev.ev3 import *

class Ev3devSetup:
	def __init__(self):
		self.MAX_SENSOR = 100.0 # percent
		self.MAX_MOTOR = 1000.0

		self.BIAS = 0.05
		self.SENSOR_GAIN = 1.0
		self.OUTPUT_GAIN = 1.0

	def initLargeMotor(self, motorname):
		return LargeMotor(motorname)

	def initColorSensor(self, sensorname):
		return ColorSensor(sensorname)

	def initUltraSonicSensor(self, sensorname):
		return UltrasonicSensor(sensorname)