HTTPClient http;

void requestToServer(){
  int httpCode = 0;
  String url = "http://192.168.1.7:8000/mcu/?serial="+String(serial)+"&temp="+String(temp)+"&humi="+String(humi);
  for(int i=0;(i<5)&&(httpCode!=200);i++){
    http.begin(url);
    httpCode = http.GET();
    http.end();
  }
}

