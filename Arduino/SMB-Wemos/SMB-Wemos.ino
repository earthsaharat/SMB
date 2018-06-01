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

int counter = 100000;
void loop() {
  network_handle();
  counter++;
  if(counter > 20){ // recommand 600 = 60*1000 (every hour) // delay 100
    counter = 0;
    updateDht();
    Serial.println("[DHT] T:"+String(temp)+" H:"+String(humi));
  }
  delay(100);
}
