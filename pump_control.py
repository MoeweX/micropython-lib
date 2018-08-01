"""
Module to manage a pump with optional PWM functionality.
The pump will turn on for a specified interval upon calling start_pump.
Set Interval to 0 to disable this functionality.

Usage Example:

pump = PumpControl(p_pwm_id='P20', p_channel_enable_id='P21', duty_cycle=0.5, interval=10, channel_name="cactus")
pump.start_pump()

"""


from machine import Pin
from machine import PWM
from machine import Timer
from tb6612_single_channel import TB6612_1CH

class PumpControl(TB6612_1CH):

    def __init__(self, p_pwm_id, p_channel_enable_id, channel_name, pwm_timer_id=0, pwm_channel_id=0, duty_cycle=1.0, interval=5):
        """
        p_pwm_id            -- the id of the pwm pin (e.g, connect pin to PWMA)
        p_channel_enable_id -- the id of the motor enable pin (e.g., connect pin to AIN2)
        channel_name        -- the name of the channel used for logging
        pwm_timer_id        -- [0], id of the timer, must be 0 to 3
        pwm_channel_id      -- [0], id of the pwm channel, must be 0 to 7
        duty_cycle          -- [1], the duty cycle of the pump, from 0-1
        interval            -- [10], the time the pump runs upon calling start_pump()
        """
        super().__init__(p_pwm_id, p_channel_enable_id, channel_name, pwm_timer_id, pwm_channel_id)
        self.__duty_cycle = duty_cycle
        self.__interval = interval

    def duty_cycle(self, duty_cycle):
        self.__duty_cycle = duty_cycle
        if (self.is_running()):
            self.set_voltage_percent(duty_cycle*100)

    def _timeout(self, alarm):
        self.stop_pump()

    def interval(self, interval=None):
        if (not interval is None):
            self.__interval = interval
        return self.__interval

    def start_pump(self):
        if (self.__interval > 0):
            self.alarm = Timer.Alarm(handler=self._timeout, s=self.__interval)
        self.set_voltage_percent(self.__duty_cycle*100)

    def stop_pump(self):
        try:
            self.alarm.cancel()
        except Exception:
            pass
        self.shut_off()

    def is_running(self):
        return self.p_channel_enable.value()
