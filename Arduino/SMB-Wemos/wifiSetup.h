char *ap_ssid = "WEMOS";
char *ap_pass = "";

char wifi_ssid[20] = "";
char wifi_pass[20] = "";

char serial[10] = "";

void cleanMem(){
  for(int i=0;i<50;i++) EEPROM.write(i,0);
  EEPROM.commit();
  String("").toCharArray(wifi_ssid, 20);
  String("").toCharArray(wifi_pass, 20);
  String("").toCharArray(serial, 10);
}

int isAPMode = false;
void activeAPMode(){
  if(!isAPMode){
    pixel(75,25,0);
    WiFi.disconnect();
    Serial.println("[WIFI] Disconnected");
    WiFi.softAP(ap_ssid, ap_pass);
    IPAddress myIP = WiFi.softAPIP();
    Serial.println("[WIFI] Mode : Access Point");
    Serial.print("[WIFI] IP   : ");
    Serial.println(myIP);
    isAPMode = true;
  }
}

void activeRecoveryMode(){
  Serial.println("[WIFI] Recovery mode");
  cleanMem();
  activeAPMode();
}

#define mode_button_pin 6
void mode_button_handle(){
  if(digitalRead(pin[mode_button_pin]) == true) activeRecoveryMode();
}

#define reconnect_max_count 25
bool connectWifi(char *temp_ssid,char *temp_pass){
  if( temp_ssid == "" || temp_pass == "" ){
    Serial.println("[WIFI] Connection ERROR : No ssid or pass");
    return false;
  }
  WiFi.disconnect();
  Serial.println("[WIFI] Disconnected");
  WiFi.begin(temp_ssid, temp_pass);
  Serial.println("[WIFI] Connecting to");
  Serial.println("[WIFI] SSID : "+String(temp_ssid));
//  Serial.println("[WIFI] PASS : "+String(temp_pass));
//  Serial.print("[WIFI] ");
//  int connect_counter = 0;
//  for(connect_counter;connect_counter<reconnect_max_count && WiFi.status() != WL_CONNECTED;connect_counter++) {
//    delay(200);
//    pixel(75,25,0);
//    delay(200);
//    pixel(0,0,0);
//    Serial.print(".");
//    mode_button_handle();
//  }
//  Serial.println();
//  if(connect_counter<reconnect_max_count){
//    Serial.println("[WIFI] Connected");
//    Serial.print("[WIFI] IP   : ");
//    Serial.println(WiFi.localIP());
//    pixel(0,100,0);
//    return true;
//  }
//  Serial.println("[WIFI] Failed : Connection Time out");
  return true;
}

bool activeClientMode(String temp_ssid,String temp_pass){
  if( temp_ssid != "" && temp_pass != "" ){
    char temp_ssid2[20];
    char temp_pass2[20];
    temp_ssid.toCharArray(temp_ssid2, 20);
    temp_pass.toCharArray(temp_pass2, 20);
    Serial.println("[WIFI] Mode : Client");
    WiFi.mode(WIFI_STA);
    isAPMode = false;
    if(connectWifi(temp_ssid2,temp_pass2)){
      memcpy( wifi_ssid, temp_ssid2, 20*sizeof(char) );
      memcpy( wifi_pass, temp_pass2, 20*sizeof(char) );
      for(int i=0;i<20;i++)EEPROM.write(i,int(temp_ssid[i]));
      for(int i=0;i<20;i++)EEPROM.write(20+i,int(temp_pass[i]));
      EEPROM.commit();
      return true;
    }else{
//      activeAPMode();
    }
  }
  return false;
}

ESP8266WebServer server(80);
void handleRoot() {
  Serial.println("[HTTP] Get a request");
  String temp_ssid = "";
  String temp_pass = "";
  for (uint8_t i = 0; i < server.args(); i++) {
    if (server.argName(i) == "A") {
      temp_ssid = server.arg(i).c_str();
    }else if (server.argName(i) == "B") {
      temp_pass = server.arg(i).c_str();
    }else if (server.argName(i) == "S") {
      String temp_serial = server.arg(i).c_str();
      temp_serial.toCharArray(serial, 10);
      for(int i=0;i<10;i++)EEPROM.write(40+i,int(serial[i]));
      Serial.println("[WIFI] Get serial : "+String(serial));
    }
  }
  if( temp_ssid != "" && temp_pass != "" ) server.send(200, "text/html", template_saved());
  else server.send(200, "text/html", template_home(wifi_ssid,serial));
  Serial.println("[HTTP] responded");
  if( temp_ssid != "" && temp_pass != "" ){
    delay(1000);
    activeClientMode(temp_ssid,temp_pass);
  }

//  String("<input type=\"text\" id=\"A\" maxlength=\"20\">")+
//  String("<input type=\"text\" id=\"B\" maxlength=\"20\">")+
//  String("<button onclick=\"window.open(\'?A=\'+document.getElementById(\'A\').value+\'&B=\'+document.getElementById(\'B\').value,\'_self\');\">Save</button>"));

}

void network_init(){
  pinMode(pin[mode_button_pin],OUTPUT);
  if(EEPROM.read(0) == 0){
    activeAPMode();
  }else{
    for(int i=0;i<20;i++) if(EEPROM.read(i) != 0)     wifi_ssid[i] = char(EEPROM.read(i));    else break;
    for(int i=0;i<20;i++) if(EEPROM.read(i+20) != 0)  wifi_pass[i] = char(EEPROM.read(i+20)); else break;
    connectWifi(wifi_ssid,wifi_pass);
    for(int i=0;i<10;i++) serial[i] = char(EEPROM.read(i+40));
  }
  server.on("/", handleRoot);
  server.begin();
  Serial.println("[HTTP] Server started");
}

void network_handle(){
  server.handleClient();
  mode_button_handle();
  if(!isAPMode){
    if(WiFi.status() != WL_CONNECTED) pixel(100,0,0);
    else pixel(0,100,0);
  }
}

