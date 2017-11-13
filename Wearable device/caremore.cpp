#define heartratePin A0
#include "DFRobot_Heartrate.h"
#include <SoftwareSerial.h>
#include <TinyGPS++.h>
#include <sim800cmd.h>
#include <std::string>
#include <vector>

class MessageBox{
private:
    uint8_t year,month,day,hour,minute,second,centisecond;
    double lat,lng;
public:
    void setLat(double data){
        lat=data;
    }
    void setLng(double data){
        lng=data;
    }
    void setTime(uint8_t hour,uint8_t minute,uint8_t second){
        this.hour=hour;
        this.minute=minute;
        this.second=second;
    }
    std::string getGPS(){
        return "Lat:"+lat+";Lng:"+lng;
    }
    std::string getRate(){
        return std::string("rate:"+rate);
    }
}
MessageBox messageBox;
DFRobot_Heartrate heartrate(DIGITAL_MODE); ///< ANALOG_MODE or DIGITAL_MODE
int buttonState = 0;
static const int buttonPin = 2,LED = 13;
static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 4800;
std::string phoneNumber = "";
SoftwareSerial GPSSerial(RXPin, TXPin); // RX, TX
TinyGPSPlus gps;
Sim800Cmd sim800demo(fundebug);

void setup()
{
    Serial.begin(115200);
    GPSSerial.begin(4800);
    //initialize the digital pin as an input.
    pinMode(buttonPin,INPUT)
    //initialize the digital pin as an output.
    pinMode(LED,OUTPUT);
    //initialize SIM800H,return 1 when initialize success.
    while((sim800demo.sim800init()) == 0);
    //初始化消息盒子
    initMessageBox();
}

void loop()
{
    buttonState = digitalRead(buttonPin);
    if(buttonState == HIGH)
    {
        digitalWrite(LED,HIGH);
        makeCall();
        digitalWrite(LED,LOW);
    }
    receiveMessage();
    //heartrate module
    uint8_t rateValue;
    heartrate.getValue(heartratePin); ///< A1 foot sampled values
    rateValue = heartrate.getRate(); ///< Get heart rate value
    if(rateValue)
    {
        saveHeartrateInfo(rateValue);
    }
    //GPS module
    while(GPSSerial.available()>0)
    {
        if(gps.encode(GPSSerial.read()))
        {
            saveGPSInfo();
        }
    }

}
void initMessageBox()
{
    Serial.println("get-phonenumber");
    while(Serial.available()>0)
    {
        phoneNumber+=Serial.read();
    }
    phoneNumber+=';';
}
void saveGPSInfo()
{
    messageBox.setLat(gps.lat());
    messageBox.setLat(gps.lng());
    mseeageBox.setTime(gps.hour(),gps.minute();gps.second());
}
//the loop routine runs over and over again forever:
void makeCall()
{
    unsigned char csq = 0;
    //To obtain the signal strength, return 1 when obtain success.
    if( sim800demo.callReadCSQ(&csq) )
    {
        //Make Voice Call
        sim800demo.dialTelephoneNumber(std::string(phoneNumber+";").c_str());
        while(1);
    }
    digitalWrite(13,HIGH);//turn the LED on by making the voltage HIGH
    delay(500);
    digitalWrite(13,LOW);//turn the LED off by making the voltage LOW
    delay(500);
}
void receiveMessage()
{
    char[] msg;
    while(Serial.available()>0)
    {
        msg+=std::string(Serial.read());
    }
    std::vector<std::string> msgBox;
    char* tmpStr = strtok(msg, std::string("@").c_str());
    while (tmpStr != NULL)
    {
        resultVec.push_back(std::string(tmpStr));
        tmpStr = strtok(NULL, pattern.c_str());
    }
    switch(resultVec[0].substr(7))//action:xxx-xxxxxx data:15570888042
    {
        case "set-phonenumber":phoneNumber=resultVec[1].substr(5);break;
        case "get-phonenumber":sendMessage("reply-number",phoneNumber);
        case "get-GPS":sendMessage("reply-GPS",messageBox.getGPS());
        case "get-rate":sendMessage("reply-rate",messageBox.getRate());
    }
}
void sendMessage(std::string action,std::string data)
{
    Serial.println("@action:");
    Serial.println(action);
    Serial.println("@data:");
    Serial.println(data);
    Serial.println("@");
}
//application callback function
void fundebug(void)
{
    char str[15] = {'\0'};
    sim800demo.getCallnumber(str);
    if(memcmp(str,phonenumber.c_str(),11) == 0)
    {
        sim800demo.answerTelephone(); //answer
    }
}
