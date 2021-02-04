# POSTURE DETECTOR

* * * 

sensors docs and references for psoture detector

# SPI Wirering

SPI wirering

![](images/spi_wiring_table_for_arduino.png)
![](images/spi_wirering_esp.png)
![](images/spi_wemos_wirering.png)


## Acelerometro - ADXL362		
THIS IS 3.3V

[very basic tutorial](https://github.com/annem/ADXL362/blob/master/examples/ADXL362_MotionActivatedSleep/ADXL362_MotionActivatedSleep.ino)

``` cpp 
#include <LowPower.h>

#include <SPI.h>
#include <ADXL362.h>

ADXL362 xl;

//  Setup interrupt on Arduino
//  See interrupt example at http://arduino.cc/en/Reference/AttachInterrupt
//
int16_t interruptPin = 2;          //Setup ADXL362 interrupt output to Interrupt 0 (digital pin 2)
int16_t interruptStatus = 0;

int16_t XValue, YValue, ZValue, Temperature;

xl.begin();  


xl.setupDCActivityInterrupt(300, 10);		// 300 code activity threshold.  With default ODR = 100Hz, time threshold of 10 results in 0.1 second time threshold
xl.setupDCInactivityInterrupt(80, 200);


```

## ADC - ADS115 

``` c++

#include<ADS1115_WE.h> 
#include<Wire.h>
#define I2C_ADDRESS 0x48

ADS1115_WE adc(I2C_ADDRESS);

adc.setVoltageRange_mV(ADS1115_RANGE_6144); 

voltage = readChannel(ADS1115_COMP_0_GND);

float readChannel(ADS1115_MUX channel) {
  float voltage = 0.0;
  adc.setCompareChannels(channel);
  adc.startSingleMeasurement();
  while(adc.isBusy()){}
  voltage = adc.getResult_V(); // alternative: getResult_mV for Millivolt
  return voltage;
}
```


## Acelerometro - MPU6050 

``` c++
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
{
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
}
  
// Calibrate gyroscope. The calibration must be at rest.
// If you don't want calibrate, comment this line.
mpu.calibrateGyro();
// Set threshold sensivty. Default 3.
// If you don't want use threshold, comment this line or set 0.
mpu.setThreshold(3);


Vector norm = mpu.readNormalizeGyro();

// Calculate Pitch, Roll and Yaw
pitch = pitch + norm.YAxis * timeStep;
roll = roll + norm.XAxis * timeStep;
yaw = yaw + norm.ZAxis * timeStep;

```