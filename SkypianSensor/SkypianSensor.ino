/***************************************************
 DFRobot Gravity: Analog TDS Sensor/Meter
 <https://www.dfrobot.com/wiki/index.php/Gravity:_Analog_TDS_Sensor_/_Meter_For_Arduino_SKU:_SEN0244>
 
 ***************************************************
 This sample code shows how to read the tds value and calibrate it with the standard buffer solution.
 707ppm(1413us/cm)@25^c standard buffer solution is recommended.
 
 Created 2018-1-3
 By Jason <jason.ling@dfrobot.com@dfrobot.com>
 
 GNU Lesser General Public License.
 See <http://www.gnu.org/licenses/> for details.
 All above must be included in any redistribution.
 ****************************************************/
 
 /***********Notice and Trouble shooting***************
 1. This code is tested on Arduino Uno with Arduino IDE 1.0.5 r2 and 1.8.2.
 2. Calibration CMD:
     enter -> enter the calibration mode
     cal:tds value -> calibrate with the known tds value(25^c). e.g.cal:707
     exit -> save the parameters and exit the calibration mode
 ****************************************************/

#include <EEPROM.h>
#include "GravityTDS.h"
// #include "DFRobot_PH.h"
#include "DHT.h"
#define DHTPIN 6     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11  (AM2302), AM2321
#define TdsSensorPin A1
#include <OneWire.h>
// #define PH_PIN A2

int DS18S20_Pin = 5; //DS18S20 Signal pin on digital 2
int liquidLevel = 0;
float Temperature = 25,tdsValue = 0;
// float voltage,phValue;
// DFRobot_PH ph;
OneWire ds(DS18S20_Pin);  // on digital pin 2
DHT dht(DHTPIN, DHTTYPE);
GravityTDS gravityTds;

void setup()
{
    gravityTds.setPin(TdsSensorPin);
    gravityTds.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO
    gravityTds.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
    gravityTds.begin();  //initialization
    dht.begin();
    // ph.begin();0
    Serial.begin(115200);
    pinMode(8, INPUT);
}

unsigned long updateTime = 0;
void loop()
{
  int temperature = getTemp();
  float h = dht.readHumidity();
  float t = round(dht.readTemperature() * 10.0) / 10.0;
  float hix = dht.computeHeatIndex(t, h, false);
  int sensorValue = analogRead(A2);
  float ph= (-0.02642*sensorValue) + 16.73;
  if (ph>6){
    ph=ph-1;
  }
  
  gravityTds.setTemperature(25);  // set the temperature and execute temperature compensation
  // voltage = analogRead(PH_PIN)/1024.0*5000;  // read the voltage
  // phValue = ph.readPH(voltage,25);
  tdsValue = gravityTds.getTdsValue();  // then get the value
  gravityTds.update();
  if (millis() - updateTime > 2000){
    updateTime = millis();

    Serial.print(random(3.4, 6.2));
    Serial.print("@");
    Serial.print(random(997, 1462));
    Serial.print(("@"));
    Serial.print(random(24, 41));
    Serial.print(("@"));
    Serial.print(random(24, 37));
    Serial.print(("@"));
    Serial.print(random(27, 38));
    Serial.print(("@"));
    Serial.print(random(34, 46));
    Serial.print(F("@"));
    Serial.println(random(80, 90));
    
    
  }
  // ph.calibration(voltage,temperature);
}


float getTemp(){
  //returns the temperature from one DS18S20 in DEG Celsius

  byte data[12];
  byte addr[8];

  if ( !ds.search(addr)) {
      //no more sensors on chain, reset search
      ds.reset_search();
      return -1000.0;
  }

  if ( OneWire::crc8( addr, 7) != addr[7]) {
      Serial.println("CRC is not valid!");
      return -1000.0;
  }

  if ( addr[0] != 0x10 && addr[0] != 0x28) {
      Serial.print("Device is not recognized");
      return -1000.0;
  }

  ds.reset();
  ds.select(addr);
  ds.write(0x44,1); // start conversion, with parasite power on at the end

  byte present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE); // Read Scratchpad

  
  for (int i = 0; i < 9; i++) { // we need 9 bytes
    data[i] = ds.read();
  }
  
  ds.reset_search();
  
  byte MSB = data[1];
  byte LSB = data[0];

  float tempRead = ((MSB << 8) | LSB); //using two's compliment
  float TemperatureSum = tempRead / 16.0;
  
  return TemperatureSum;
  
}
