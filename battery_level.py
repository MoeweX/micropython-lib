"""
Module to read the battery level.

Max analog in = 1.1v, use factor to calculate real voltage.
Module uses smallest attenuation, as the accuracy is highest.

Usage example:

battery = BatteryLevel("P16", 2.0)
battery.get_level()
"""


from machine import ADC
import time

class BatteryLevel:

    def __init__(self, p_analog_id, factor):
        self.factor = factor

        adc = ADC() # create an ADC object
        self.p_analog = adc.channel(pin=p_analog_id) # create an analog pin

    def get_raw_avg(self):
        measurements = []
        for i in range(0, 5):
            measurements.append(self.p_analog.voltage())
            time.sleep(0.2)
        return sum(measurements) / float(len(measurements))

    def get_level(self):
        voltage = self.read_average() * self.factor
        level = voltage / 1000
        print("Voltage level is {}V".format(level))
        return level
