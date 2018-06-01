String template_home(char *temp_ssid,char *temp_serial){
  return
"\
<style type='text/css'>\
 body{ font-family: Sans-serif; } p{margin: 0px; }\
  .t1{ font-size: 70px; color: #666; margin-top: 30px; }\
  .t2{ font-size: 20px; color: #ccc;  }\
  p{ text-align: center; font-weight: bold;}\
  input{width: 100%; border: solid; color: #666; border: none; background-color: #eee; font-size: 30px; padding: 15px; margin-top: 10px; }\
  ::placeholder { color: #ccc; opacity: 1; }\
  :-ms-input-placeholder { color: #ccc; }\
  ::-ms-input-placeholder { color: #ccc; }\
  .section{ margin: auto; width: 80%; margin-top: 20px; }\
  button{ border: none; font-weight: bold; cursor: pointer; width: 100%; }\
  button.b2{ background-color: #faaf3c; color: #fff;  font-size: 40px; height: 80px;  }\
  :focus{ outline: none; }\
</style>\
<title>Smart Mushroom Box</title>\
<body>\
  <p class='t1'>Smart <span style='color: #faaf3c;'>Mushroom</span> Box</p>\
  <div class='section'>\
    <p class='t2'>WIFI</p>\
    <input type='text' id='A' maxlength='20' placeholder='name' value="+String(temp_ssid)+">\
    <input type='password' id='B' maxlength='20' placeholder='password'>\
  </div>\
  <div class='section'>\
    <p class='t2'>SERIAL</p>\
    <input type='text' id='S' maxlength='10' placeholder='serial' value="+String(temp_serial)+">\
  </div>\
  <div class='section'>\
    <button class='b2' onclick='mysubmit()'>Save</button>\
  </div>\
  <script type='text/javascript'>\
    function mysubmit(){\
      window.open('?A='+document.getElementById('A').value+'&B='+document.getElementById('B').value+'&S='+document.getElementById('S').value,'_self');\
    }\
  </script>\
</body>\
";
}

String template_saved(){
  return
"\
<style type='text/css'>\
 body{ font-family: Sans-serif; } p{margin: 0px; }\
  .t1{ font-size: 70px; color: #666; margin-top: 30px; }\
  .t2{ font-size: 50px; color: #ccc;  }\
  p{ text-align: center; font-weight: bold;}\
  input{width: 100%; border: solid; color: #666; border: none; background-color: #eee; font-size: 30px; padding: 15px; margin-top: 10px; }\
  ::placeholder { color: #ddd; opacity: 1; }\
  :-ms-input-placeholder { color: #ddd; }\
  ::-ms-input-placeholder { color: #ddd; }\
  .section{ margin: auto; width: 80%; margin-top: 20px; }\
  button{ border: none; font-weight: bold; cursor: pointer; width: 100%; }\
  button.b2{ background-color: #faaf3c; color: #fff;  font-size: 40px; height: 80px;  }\
  :focus{ outline: none; }\
</style>\
<title>Smart Mushroom Box</title>\
<body>\
  <p class='t1'>Smart <span style='color: #faaf3c;'>Mushroom</span> Box</p>\
  <div class='section'>\
    <p class='t2'>Saved</p>\
  </div>\
</body>\
";
}

