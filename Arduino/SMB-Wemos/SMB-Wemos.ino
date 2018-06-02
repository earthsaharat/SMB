int pin[] = {16, 5, 4, 0, 2, 14, 12, 13, 15};
/*   EEPROM - MAP
 *   0 - 19 : SSID
 *  20 - 39 : PASS
 *  40 - 50 : serial */

#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <EEPROM.h>

#include "outlet.h"
#include "template.h"
#include "wifiSetup.h"
#include "wifiRequest.h"

void setup() {
  delay(1000);
  Serial.begin(115200);
  EEPROM.begin(4096);
  Serial.println();
  Serial.println("[SYSTEM] Booting");
  
  outlet_init();  
  network_init();
}

bool isConnectPrevious = false;
int counter = 100000;
void loop() {
  network_handle();
  counter++;
  
  if(isConnect != isConnectPrevious){
    if(isConnect){
      pixel(0,100,0);
      Serial.println("[WIFI] Connected");
      Serial.print("[WIFI] IP   : ");
      Serial.println(WiFi.localIP());
      requestToServer();
    }else{
      Serial.println("[WIFI] Disconnected");
      pixel(100,0,0);
    }
  }
  isConnectPrevious = isConnect;

  if(counter > 1200 ){ // delay 100 // 10 time = 1 secound // 600 time = 1 minute
    counter = 0;
    requestToServer();
    led(target_r,target_g,target_b);
    updateCooler();
  }else if(counter%20 == 0){
    updateDht();
    updateHumidifier();
  }
  delay(100);
}
