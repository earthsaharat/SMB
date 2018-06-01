// MARK : NeoPixel
#include <Adafruit_NeoPixel.h>
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(1, pin[2], NEO_GRB + NEO_KHZ800);
void pixel(int r,int g, int b){
  pixels.setPixelColor(0, pixels.Color(r,g,b));
  pixels.show();
}

// MARK : DHT
#include "DHT.h"
DHT dht1(pin[1], DHT22);
float temp = 0;
float humi = 0;
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
}

// PCF8574(Pin Extension)
#include "PCF8574.h"
#include <Wire.h>
PCF8574 pcf(0x38);// A0=0 A1=0 A2=0 // pcf.write(address,value) // 0=on 1=off
//pcf.write(pin,value);
//pcf.read(pin);

void outlet_init(){
  pixels.begin();
  dht1.begin();
  pcf.begin();
}

