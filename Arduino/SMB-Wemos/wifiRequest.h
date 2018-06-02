HTTPClient http;

void requestToServer(){
  if(isAPMode || (isnan(temp) || isnan(humi)) ){
    Serial.println("[REQUEST] Not available");
    return;
  }
  int httpCode = 0;
  String payload = "";
  String url = "http://192.168.1.32:8000/mcu/?serial="+String(serial)+"&temp="+String(temp)+"&humi="+String(humi);
  for(int i=0;(i<5)&&(httpCode!=200);i++){
    http.begin(url);
    httpCode = http.GET();
    if(httpCode == 200) payload = http.getString();
    mode_button_handle();
    http.end();
  }
  if(httpCode == 200){
    Serial.println("[REQUEST] get : "+payload);
    target_temp = payload.substring(0,4).toInt()/10.0;
    target_humi = payload.substring(5,9).toInt()/10.0;
    target_r    = payload.substring(10,13).toInt();
    target_g    = payload.substring(14,17).toInt();
    target_b    = payload.substring(18,21).toInt();
    Serial.println("[SYSTEM ] set target temp:"+String(target_temp)+" humi:"+String(target_humi)+
      " R:"+String(target_r)+" G:"+String(target_g)+" B:"+String(target_b) );
  }
}

