from machine import ADC
from time import sleep

tempsensor = ADC(4)
conversion_factor = 3.3 / (65535) # Conversion from Pin read to proper voltage

while True:
	currentvoltage = tempsensor.read_u16() * conversion_factor
	temp = 27 - ((currentvoltage - 0.706)/0.001721)
	print(str(currentvoltage) + " : " + str(temp))
	sleep(2)