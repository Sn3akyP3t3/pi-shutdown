#!/usr/bin/python
# shutdown/reboot(/power on) Raspberry Pi with pushbutton
import time
from datetime import datetime
from subprocess import call
import RPi.GPIO as GPIO


class ShutdownManager(object):
	def __init__(self):
		# pushbutton connected to this GPIO pin, using pin 5 also has the benefit of
		# waking / powering up Raspberry Pi when button is pressed
		self.SHUTDOWN_PIN = 5

		# if button pressed for at least this long then shut down. if less then reboot.
		self.SHUTDOWN_MIN_SECONDS = 3

		# button debounce time in seconds
		self.DEBOUNCE_SECONDS = 0.01

		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.BUTTON_PRESSED_TIME = None

	def ButtonStateChanged(self, pin):
		if not GPIO.input(pin) and self.BUTTON_PRESSED_TIME is None:
			# button is down
			self.BUTTON_PRESSED_TIME = datetime.now()
		elif self.BUTTON_PRESSED_TIME is not None:
			# button is up
			elapsed = (datetime.now() - self.BUTTON_PRESSED_TIME).total_seconds()
			self.BUTTON_PRESSED_TIME = None
			if elapsed >= self.SHUTDOWN_MIN_SECONDS:
				# button pressed for more than specified time, shutdown
				call(['shutdown', '-h', 'now'], shell=False)
			elif elapsed >= self.DEBOUNCE_SECONDS:
				# button pressed for a shorter time, reboot
				call(['shutdown', '-r', 'now'], shell=False)


if __name__ == "__main__":
	sdm = ShutdownManager()
	# subscribe to button presses
	GPIO.add_event_detect(sdm.SHUTDOWN_PIN, GPIO.BOTH, callback=sdm.ButtonStateChanged)

	while True:
		# sleep to reduce unnecessary CPU usage
		time.sleep(5)
