"""
Module to manage a pump with optional PWM functionality.
The pump will turn on for a specified interval upon calling start_pump.

Usage Example:

pump = PumpControl('P20', 'P21', 0.5, 10)
pump.start_pump()

"""


from machine import Pin
from machine import PWM
from machine import Timer

class PumpControl:
    def __init__(self, pump_pin, pwm_pin=None, duty_cycle=1.0, interval=5):
        self.pump_pin = pump_pin
        self.__duty_cycle = duty_cycle
        if (not pwm_pin is None):
            self.pwm_pin = pwm_pin
            self.pwm = PWM(0, frequency=5000)
            self.pwm_c = self.pwm.channel(0, pin=self.pwm_pin, duty_cycle=self.__duty_cycle)
        self.__interval = interval
        self.pump_out = Pin(self.pump_pin, mode=Pin.OUT)

    def duty_cycle(self, duty_cycle):
        self.__duty_cycle = duty_cycle
        if (not self.pwm_c is None):
            self.pwm_c.duty_cycle(duty_cycle)

    def interval(self, interval):
        self.__interval = interval

    def start_pump(self):
        self.alarm = Timer.Alarm(handler=self.stop_pump, s=self.__interval)
        self.pump_out.value(1)
        if (not self.pwm_c is None):
            self.pwm_c.duty_cycle(self.__duty_cycle)

    def stop_pump(self, alarm=None):
        if (not self.alarm is None):
            self.alarm.cancel()
        self.pump_out.value(0)
        if (not self.pwm_c is None):
            self.pwm_c.duty_cycle(0)
