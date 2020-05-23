# UV IoT Device

Project to make a battery powered IoT device for the measurement of UV radiation, temperature and visible light levels.


### Software Requirements

- Python>=3.7
- RPi.GPIO>=0.7
- gpiozero>=1.5
- numpy>= 1.16
- DFRobot_VEML6075.py library for UV sensor (https://github.com/DFRobot/DFRobot_VEML6075)
- ADCDevice-1.0.2 library for PCF8591 (https://github.com/Freenove/Freenove_Super_Starter_Kit_for_Raspberry_Pi/tree/master/Libs/Python-Libs)


### Hardware Requirements

- Raspberry Pi Zero W
- Thermistor
- PCF8591 (or another ADC)
- 5000 or 10000 mAh powerbank
- VEML6075 UV sensor

### Prototype Device v1

**Initial set up of the device Prototype on the Breadboard**
![Breadboard of the v1 set-up](images/IMGBreadboardv1.jpg)


### Software- Python

**IoT recorder every 1 minute**
Program to record temperature, UVA, UVB and UVindex every 10s and dump these into a json file every minute can be done by adding the following to the Raspberry Pi startup scripts:

> startupBash.sh

This automatically starts the main python script upon boot up:

> RPiUVmeasureMain.py


### Software- julia
