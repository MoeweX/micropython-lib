"""
Module to manage an analog soil moisture sensor.
Moisture is a value between 0 and 100. 0 = air humidity; 100 = water humidity

Max analog in = 3.3v!

Usage example:

sensor = SoilMoisture(2915, 1300, "P13")
sensor.get_moisture()
"""


from machine import ADC
import time

class SoilMoisture:

    def __init__(self, air_voltage, water_voltage, p_analog_id):
        self.air_voltage = air_voltage
        self.water_voltage = water_voltage

        adc = ADC() # create an ADC object
        self.p_analog = adc.channel(pin=p_analog_id, attn=ADC.ATTN_11DB) # create an analog pin

    def get_raw_avg(self):
        measurements = []
        for i in range(0, 5):
            measurements.append(self.p_analog.voltage())
            time.sleep(0.2)
        return sum(measurements) / float(len(measurements))

    def get_moisture(self):
        voltage = self.get_raw_avg()
        diff = self.air_voltage - self.water_voltage
        a = voltage - self.water_voltage
        b = a / diff
        percent = int((b - 1) * -100)
        print("Moisture is {}%".format(percent))
        return percent
