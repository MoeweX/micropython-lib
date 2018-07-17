"""
Module to control the voltage of a single tb6612 driver channel.
Note, that one PWM pin controls two channels simultaniously.
Voltage can be set in percent, 0% = 0V, 100% = Vin

Usage example:

tb_channel = TB6612_1CH("P22", "P21", "voltage channel")
tb_channel.set_voltage(80) # set voltage to 80%
tb_channel.shut_off() # shut off
"""

from machine import Pin
from machine import PWM

class TB6612_1CH:

    def __init__(self, p_pwm_id, p_channel_enable_id, channel_name, pwm_timer_id=0, pwm_channel_id=0):
        """
        p_pwm_id            -- the id of the pwm pin (e.g, connect pin to PWMA)
        p_channel_enable_id -- the id of the motor enable pin (e.g., connect pin to AIN2)
        channel_name        -- the name of the channel used for logging
        pwm_timer_id        -- [0], id of the timer, must be 0 to 3
        pwm_channel_id      -- [0], id of the pwm channel, must be 0 to 7
        """
        self.channel_name = channel_name
        pwm = PWM(pwm_timer_id, frequency=5000)  # use given pwm timer, with a frequency of 5KHz
        self.p_pwm = pwm.channel(pwm_channel_id, pin=p_pwm_id, duty_cycle=0.0)

        self.p_channel_enable = Pin(p_channel_enable_id, mode=Pin.OUT)

    def set_voltage(self, percent):
        scale = percent / 100.0
        if scale > 1.0:
            scale = 1.0
        elif scale < 0.0:
            scale = 0.0
        print("Setting {0} voltage to {1}%".format(self.channel_name, percent))
        self.p_channel_enable.value(1)
        self.p_pwm.duty_cycle(scale)

    def shut_off(self):
        print("Disabling {} output".format(self.channel_name))
        self.p_channel_enable.value(0)
        self.p_pwm.duty_cycle(0.0)
