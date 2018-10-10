

from RPi import GPIO
import time



MAX_CHANGES = 67
PULSE_LENGTH=350
SYNC_HIGH=1
SYNC_LOW=31
ZERO_HIGH=1
ZERO_LOW=3
ONE_HIGH=3
ONE_LOW=1

class RFDevice:
	def __init__(self, gpio):
		self.gpio = gpio
		# tx
		self.tx_enabled=False
		self.tx_pulselength=PULSE_LENGTH
		self.tx_repeat=10
		self.tx_length=24
		# rx
		self.rx_enabled=False
		self.rx_tolerance=80
		# internals
		self._rx_timings=[0] * (MAX_CHANGES + 1)
		self._rx_last_timestamp=0
		self._rx_change_count=0
		self._rx_repeat_count=0
		# output values
		self.rx_code = None
		self.rx_code_timestamp = None
		self.rx_bitlength = None
		self.rx_pulselength = None
		
		GPIO.setmode(GPIO.BCM)
		print("Using GPIO " + str(gpio))
		
	# Disable TX and RX and clean up GPIO or cleanup the given pin
	# Internally, GPIO.cleanup() sets all pins to input pins for safety
	def cleanup(self, pin=None):
		if not pin:
			if self.tx_enabled:
				self.disable_tx()
			if self.rx_enabled:
				self.disable_rx()
			print("Cleanup all pins")
			GPIO.cleanup()
		else:
			print("Cleanup pin "+str(pin))
			GPIO.setup(pin, GPIO.IN)
		
	def enable_tx(self):
		# Enable TX, set up GPIO
		if self.rx_enabled:
			print("Pin: "+str(self.gpio)+" already set as RX")
			return False
		if not self.tx_enabled:
			self.tx_enabled=True
			GPIO.setup(self.gpio, GPIO.OUT)
			print("TX enabled")
		return True
	
	# Disable TX, reset GPIO
	def disable_tx(self):
		if self.tx_enabled:
			self.cleanup(self.gpio)
			self.tx_enabled=False
			print("TX disabled")
		return True

	# Send a decimal code
	def tx_code(self, code):
		rawcode=format(code, "#0{}b".format(self.tx_length + 2))[2:]
		return self.tx_bin(rawcode)
		
	# Send a binary code
	def tx_bin(self, rawcode):
		print("TX bin: "+str(rawcode))
		for _ in range(0, self.tx_repeat):
			for bit in range(0, self.tx_length):
				if rawcode[bit]=="0":
					if not self.tx_l0():
						return False
				elif rawcode[bit]=="1":
					if not self.tx_l1():
						return False
			if not self.tx_sync():
				return False
		return True
	
	# Send a '0' bit
	def tx_l0(self):
		return self.tx_waveform(ZERO_HIGH,ZERO_LOW)
	
	# Send a '1' bit
	def tx_l1(self):
		return self.tx_waveform(ONE_HIGH,ONE_LOW)
	
	# Send a sync
	def tx_sync(self):
		return self.tx_waveform(SYNC_HIGH,SYNC_LOW)
	
	# Send basic waveform				
	def tx_waveform(self, highpulses, lowpulses):
		if not self.tx_enabled:
			print("TX is not enabled, not sending data")
			return False
		GPIO.output(self.gpio, GPIO.HIGH)
		self._sleep((highpulses * self.tx_pulselength) / 1000000)
		GPIO.output(self.gpio, GPIO.LOW)
		self._sleep((lowpulses * self.tx_pulselength) / 1000000)
		return True

	# Enable RX, set up GPIO and add event detection
	def enable_rx(self):
		if self.tx_enabled:
			print("Pin: "+str(self.gpio)+" already set as TX")
			return False
		if not self.rx_enabled:
			self.rx_enabled=True
			GPIO.setup(self.gpio, GPIO.IN)
			GPIO.add_event_detect(self.gpio, GPIO.BOTH)
			GPIO.add_event_callback(self.gpio, self.rx_callback)
			print("RX enabled")
		return True
	
	# Disable RX, remove GPIO event detection
	def disable_rx(self):
		if self.rx_enabled:
			GPIO.remove_event_detect(self.gpio)
			self.rx_enabled = False
			print("RX disabled")
		return True

	# RX callback for GPIO event detection
	def rx_callback(self, gpio):
		timestamp=int(time.perf_counter()*1000000)
		duration=timestamp-self._rx_last_timestamp

		if duration>5000:
			if duration-self._rx_timings[0] < 200:
				self._rx_repeat_count+=1
				self._rx_change_count-=1
				if self._rx_repeat_count==2:
					if self._rx_waveform(self._rx_change_count, timestamp):
						print("RX code " + str(self.rx_code))
					self._rx_repeat_count=0
			self._rx_change_count=0

		if self._rx_change_count >= MAX_CHANGES:
			self._rx_change_count = 0
			self._rx_repeat_count = 0
		self._rx_timings[self._rx_change_count] = duration
		self._rx_change_count += 1
		self._rx_last_timestamp = timestamp
	
	# Format code
	def _rx_waveform(self, change_count, timestamp):
		code = 0
		delay = int(self._rx_timings[0] / SYNC_LOW)
		delay_tolerance = delay * self.rx_tolerance / 100

		for i in range(1, change_count, 2):
			if (self._rx_timings[i] - delay * ZERO_HIGH < delay_tolerance and
					self._rx_timings[i+1] - delay * ZERO_LOW < delay_tolerance):
				code <<= 1
			elif (self._rx_timings[i] - delay * ONE_HIGH < delay_tolerance and
				  self._rx_timings[i+1] - delay * ONE_LOW < delay_tolerance):
				code <<= 1
				code |= 1
			else:
				return False

		if self._rx_change_count > 6 and code != 0:
			self.rx_code = code
			self.rx_code_timestamp = timestamp
			self.rx_bitlength = int(change_count / 2)
			self.rx_pulselength = delay
			return True

		return False
								
	def _sleep(self, delay):      
		_delay = delay / 100
		end = time.time() + delay - _delay
		while time.time() < end:
			time.sleep(_delay)
