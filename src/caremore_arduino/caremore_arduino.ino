#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include "DFRobot_Heartrate.h"
#define heartratePin A0

static const int TXPin = 3, RXPin = 2;
static const uint32_t GPSBaud = 9600;

// The TinyGPS++ object
TinyGPSPlus gps;
// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);
// The Heartrate object
DFRobot_Heartrate heartrate(DIGITAL_MODE);

void setup() {
  Serial.begin(115200);
  ss.begin(GPSBaud);
}

void loop() {
  String comdata = "";
  while (Serial.available() > 0) {
    comdata += char(Serial.read());
    delay(2);
  }
  if(comdata==""){
  }else if(comdata[0]=='A'&&comdata[1]=='T'){
    Serial.println("AT:OK");
    Serial.flush();
  }else  if(comdata[0]=='G'&&comdata[1]=='P'&&comdata[2]=='S'){
    Serial.println("AT:GPS");
    Serial.flush();
    for(int i=0;i!=100;i++){
      while(ss.available()){
        gps.encode(ss.read());
        delay(2);
      }
      if(gps.location.isValid()){
        Serial.print("LAT:");
        Serial.print(gps.location.lat()*1000000);
        Serial.println("");
        Serial.print("LNG:");
        Serial.print(gps.location.lng()*1000000);
        Serial.println("");
        ss.flush();
        break;
      }
    }
  }else{
    Serial.flush();
  }
  uint8_t rateValue;
  heartrate.getValue(heartratePin); ///< A1 foot sampled values
  rateValue = heartrate.getRate(); ///< Get heart rate value 
  if(rateValue){
    Serial.print("RATE:");
    Serial.println(rateValue);
    delay(100);
    while(ss.available()){
      gps.encode(ss.read());
      delay(2);
    }
    if(gps.location.isValid()){
      Serial.print("LAT:");
      Serial.print(gps.location.lat()*1000000);
      Serial.println("");
      Serial.print("LNG:");
      Serial.print(gps.location.lng()*1000000);
      Serial.println("");
      delay(100);
      ss.flush();
    }
  }
  delay(20);
}
