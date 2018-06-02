float target_temp = 0;
float target_humi = 0;
int target_r = 0;
int target_g = 0;
int target_b = 0;

float temp = 0;
float humi = 0;

// MARK : NeoPixel
#include <Adafruit_NeoPixel.h>
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(1, pin[2], NEO_GRB + NEO_KHZ800);
void pixel(int r,int g, int b){
  pixels.setPixelColor(0, pixels.Color(r,g,b));
  pixels.show();
}

// MARK : LED
void led(int r,int g,int b){
  Serial.println("[  LED  ] R:"+String(r)+" G:"+String(g)+" B:"+String(b));
  analogWrite(pin[6],((100-r)/100.0*999.0));
  analogWrite(pin[7],((100-g)/100.0*999.0));
  analogWrite(pin[8],((100-b)/100.0*999.0));
}

// MARK : Cooler
void cooler(bool state){
  Serial.println("[Cooler ] "+String(state ? "ON":"OFF"));
  digitalWrite(pin[5],state);
}

// MAKR : Humidifier
void humidifier(bool state){
  Serial.println("[ Humi  ] "+String(state ? "ON":"OFF"));
  digitalWrite(pin[0],state);
}

void updateCooler(){
  if(target_temp == 0) cooler(false);
  else cooler(temp > target_temp);
}
void updateHumidifier(){
  if(target_humi == 0) humidifier(false);
  else humidifier(humi < target_humi);
}

// MARK : DHT
#include "DHT.h"
DHT dht1(pin[3], DHT22);
void updateDht(){
  float t = dht1.readTemperature();
  float h = dht1.readHumidity();
  for(int i=0;i<10 && (isnan(h) || isnan(t)) ;i++){
    h = dht1.readHumidity();
    t = dht1.readTemperature();
    delay(10);
  }
  temp = t;
  humi = h;
  
  Serial.println("[  DHT  ] T:"+String(temp)+" H:"+String(humi));
}

// PCF8574(Pin Extension)
//#include "PCF8574.h"
//#include <Wire.h>
//PCF8574 pcf(0x38);// A0=0 A1=0 A2=0 // pcf.write(address,value) // 0=on 1=off
//pcf.write(pin,value);
//pcf.read(pin);
//pcf.begin();


void outlet_init(){
  pixels.begin();
  dht1.begin();
  pinMode(pin[0],OUTPUT);
  pinMode(pin[5],OUTPUT);
  pinMode(pin[6],OUTPUT);
  pinMode(pin[7],OUTPUT);
  pinMode(pin[8],OUTPUT);
  led(0,0,0);
}

