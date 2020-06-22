#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <SoftwareSerial.h>
#include <Adafruit_Fingerprint.h>
//D1 - 17
//D2 - 16
char recStr[10];
const char* ssid = "Heliosss";  //ENTER YOUR WIFI SETTINGS
const char* password = "8888888889";
const String host = "192.168.43.109";
uint8_t *arrayData;

SoftwareSerial SUART(4, 5);  //D2, D1 = SRX, STX
SoftwareSerial mySerial(13, 15);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);
HTTPClient http;

void setup() {
  Serial.begin(230400);
  SUART.begin(115200);
  WiFi.mode(WIFI_OFF);        //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA);        //This line hides the viewing of ESP as wifi hotspot
  WiFi.begin(ssid, password);     //Connect to your WiFi router
  Serial.println("");
  Serial.print("Connecting");
  //    Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  //  If connection successful show IP address in serial monitor
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //IP address assigned to your ESP

  finger.begin(57600);
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  }
  else {
    Serial.println("Did not find fingerprint sensor :(");
    while (1) {
      delay(1);
    }
  }
}

void loop() {
  String payload, postData = "data=";
  if (receiveRequestfromArduino() == "InputFinger") {
    arrayData = new uint8_t[9216];
    http.begin("http://" + host + "/VDKproject/categories/matchFingerprint.php");
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
    Serial.println("Nhap van tay");
    uint8_t x =  getFingerprintEnroll();
    Serial.println();
    Serial.println("Oke");

    for (int i = 0 ; i < 4608; i++) {
      postData += String(arrayData[i]);
      if ((i + 1) % 32 == 0 ) postData += "\n";
      else {
        postData += " ";
      }
    }
    int httpCode = http.POST(postData);//Send the request
    Serial.println(httpCode);
    http.end();

    http.begin("http://" + host + "/VDKproject/categories/matchFingerprint.php");
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
    postData = "data=";
    for (int i = 4608 ; i < 9184; i++) {
      postData += String(arrayData[i]);
      if ((i + 1) % 32 == 0) postData += "\n";
      else {
        postData += " ";
      }
    }
    delete[] arrayData;
    httpCode = http.POST(postData);   //Send the request
    Serial.println(httpCode);   //Print HTTP return code
    http.end();

    http.begin("http://" + host + "/VDKproject/categories/matchFingerprint.php");
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
    postData = "data=OKE";
    httpCode = http.POST(postData);
    Serial.println(httpCode); //Send the request
    //postData = "";
    http.end();

    delay(1000);
    postData = "";
    payload = "0-0";
    int dem = 0;
    while (payload.substring(0, 1) != "1" && payload.substring(0, 1) != "2") {
      http.begin("http://" + host + "/VDKproject/categories/matchResult.php");
      httpCode = http.GET();
      payload = http.getString();
      Serial.print(dem);
      Serial.println(" : " + payload);
      http.end();
      delay(100);
      dem++;
      if (dem == 60) {
        payload = "2-0";
        break;
      }
    }
    Serial.println(payload);
    SUART.print("<" + payload.substring(0, 1) + ">");
    SUART.print("<0>");
    http.end();
  }
  else {
    http.begin("http://" + host + "/VDKproject/categories/sendRequest.php");
    int httpCode = http.GET();
    payload = http.getString();
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
    if (payload == "create")
    {
      arrayData = new uint8_t[9216];
      //http.end();
      http.begin("http://" + host + "/VDKproject/categories/getData.php");
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
      Serial.println("Nhap van tay");
      uint8_t x =  getFingerprintEnroll();
      Serial.println();
      Serial.println("OKe");

      for (int i = 0 ; i < 4608; i++) {
        postData += String(arrayData[i]);
        if ((i + 1) % 32 == 0 ) postData += "\n";
        else {
          postData += " ";
        }
      }
      int httpCode = http.POST(postData);//Send the request
      Serial.println(httpCode);
      http.end();

      http.begin("http://" + host + "/VDKproject/categories/getData.php");
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
      postData = "data=";
      for (int i = 4608 ; i < 9184; i++) {
        postData += String(arrayData[i]);
        if ((i + 1) % 32 == 0) postData += "\n";
        else {
          postData += " ";
        }
      }
      delete[] arrayData;
      httpCode = http.POST(postData);   //Send the request
      Serial.println(httpCode);   //Print HTTP return code
      http.end();

      http.begin("http://" + host + "/VDKproject/categories/getData.php");
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
      postData = "data=OKE";
      httpCode = http.POST(postData);
      Serial.println(httpCode); //Send the request
      //postData = "";
      http.end();
    }
    else if (payload == "match") {
      arrayData = new uint8_t[9216];
      http.begin("http://" + host + "/VDKproject/categories/matchFingerprint.php");
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
      Serial.println("Nhap van tay");
      uint8_t x =  getFingerprintEnroll();
      Serial.println();
      Serial.println("OKe");

      for (int i = 0 ; i < 4608; i++) {
        postData += String(arrayData[i]);
        if ((i + 1) % 32 == 0 ) postData += "\n";
        else {
          postData += " ";
        }
      }
      int httpCode = http.POST(postData);//Send the request
      Serial.println(httpCode);
      http.end();

      http.begin("http://" + host + "/VDKproject/categories/matchFingerprint.php");
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
      postData = "data=";
      for (int i = 4608 ; i < 9184; i++) {
        postData += String(arrayData[i]);
        if ((i + 1) % 32 == 0) postData += "\n";
        else {
          postData += " ";
        }
      }
      delete[] arrayData;
      httpCode = http.POST(postData);   //Send the request
      Serial.println(httpCode);   //Print HTTP return code
      http.end();

      http.begin("http://" + host + "/VDKproject/categories/matchFingerprint.php");
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
      postData = "data=OKE";
      httpCode = http.POST(postData);
      Serial.println(httpCode); //Send the request
      //postData = "";
      http.end();

      delay(3000);
      postData = "";
      payload = "0-0";
      int dem = 0;
      while (payload.substring(0, 1) != "1" && payload.substring(0, 1) != "2") {
        http.begin("http://" + host + "/VDKproject/categories/matchResult.php");
        httpCode = http.GET();
        payload = http.getString();
        Serial.print(dem);
        Serial.println(" : " + payload);
        http.end();
        delay(100);
        dem++;
        if (dem == 100) {
          //payload = "3-0";
          break;
        }
      }
      Serial.println(payload);
      SUART.print("<" + payload.substring(0, 1) + ">");
      SUART.print("<0>");
      http.end();
    }
    else {
      //SUART.print("<0>"); //sending create command
    }
  }
  http.end();
  delay(100);
}

uint8_t getFingerprintEnroll() {
  int p = -1;
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        //  Serial.println("Image taken");
        break;
      case FINGERPRINT_NOFINGER:
        // Serial.println(".");
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        // Serial.println("Communication error");
        break;
      case FINGERPRINT_IMAGEFAIL:
        // Serial.println("Imaging error");
        break;
      default:
        //  Serial.println("Unknown error");
        break;
    }
  }
  // OK success!
  uint8_t p1;
  // Serial.print("\n==> Attempting to get Image #"); Serial.println(id);
  p1 = finger.downImage();
  switch (p1) {
    case FINGERPRINT_OK:
      //Serial.print("Image "); Serial.print(id); Serial.println(" transferring:");
      break;
    default:
      //Serial.print("Unknown error ");
      // Serial.println(p);
      return p1;
  }
  // Filtering The Packet
  int x = 2, count = 0;
  uint8_t number = 0, dem = 0, temp, a = 0, line = 0, temp_upper, temp_lower;

  while (1) {
    if (a >= 139)
    {
      a = 0;
      x++;
    }
    else
    {
      if (mySerial.available())
      {
        if (a <= 8 || a >= 137) {
          mySerial.read();
        }
        else {
          temp = mySerial.read();
          dem++;
          temp_upper = temp / 16;
          temp_lower = temp % 16;
          if (temp_upper > 6) {
            number = number * 2 + 1;
          }
          else {
            number = number * 2;
          }

          if (temp_lower > 6) {
            number = number * 2 + 1;
          }
          else {
            number = number * 2;
          }

          if (dem == 4) {
            // postData += String(number) + " ";
            Serial.print(count + 1);
            *(arrayData + count) = number;
            Serial.print(":");
            Serial.print(number);
            Serial.print(" ");
            count++;
            dem = 0;
            number = 0;
            line++;
          }
          //          if (line == 32 ) {
          //            postData += "\n";
          //            line = 0;
          //          }
        }
        a++;
      }
    }
    if (x == 289) {
      while (mySerial.available()) {
        mySerial.read();
      }
      // Serial.print("Da lay van tay");
      break;
    }
  }
  return p;
}

String receiveRequestfromArduino() {
  byte n = SUART.available();
  SUART.readBytesUntil('>', recStr, 10);
  int x = atoi(recStr + 1);
  if (x == 1)
  {
    char recStr[10] = "";
    return "InputFinger";
  } 
  else {
    char recStr[10] = "";
    return "Nope";
  }
}
