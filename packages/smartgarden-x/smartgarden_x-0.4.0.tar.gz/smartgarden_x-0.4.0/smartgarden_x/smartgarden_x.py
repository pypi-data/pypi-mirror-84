"""Main module."""

import board
import pulseio
import adafruit_dht
from time import sleep
import spidev
import digitalio

class SmartGardenX:

	def __init__(self):
		self.spi = spidev.SpiDev()
		self.spi.open(0,0)
		self.spi.max_speed_hz=1000000

		self.dht11 = adafruit_dht.DHT11(board.D4)

	def dht11_sensor(self, condition):
		""" Reads Humidity and Temperature data from DHT11 sensor
		:param condition: either temperature or humidity
		:return: condition value
		"""

		device = self.dht11
		try:
			if device.temperature is not None or device.humidity is not None:
				if condition == "temperature":
					return device.temperature
				elif condition == "humidity":
					return device.humidity
			else:
				return 0
		except RuntimeError:
			pass

	def read_analog(self, mcp_port):
		"""Read values from MCP3008 ADC
		:param channel: port in the adc
		:return: channel value
		"""
		val = self.spi.xfer2([1,(8+mcp_port)<<4,0])
		value = ((val[1]&3) << 8) + val[2]
		return value

	def actuator(self, state):
		"""Start and Stop an Actuator
		:param state: ON or OFF state of the actuator
		:return: None
		"""

		device = digitalio.DigitalInOut(board.D17)
		device.direction = digitalio.Direction.OUTPUT

		if state == "ON":
			device.value = 1
		elif state == "OFF":
			device.value = 0
