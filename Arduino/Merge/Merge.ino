#include <Keypad.h> // the library for the 4x4 keypad
#include <LiquidCrystal_I2C.h> // the library for the i2c 1602 lcd
#include <Servo.h> // the library to control the servo motor
LiquidCrystal_I2C lcd(0x3F, 16, 2); // gets the lcd
Servo servo;
char recStr[10];
#define Password_Length 8 // the length of the password, if the password is 4 digits long set this to 5
int Position = 0; // position of the servo
char Particular[Password_Length]; // the password length
char Specific[Password_Length] = "111111A"; // the password which is called specific in the code, change this to anything you want with the numbers 0-9 an dthe letters A-D
byte Particular_Count = 0, Specific_Count = 0; // counts the amount of digits and and checks to see if the password is correct
char Key;
int GREEN_LED =  12;
int RED_LED =  13;
int buzzer = 11 ;
int dem = 0 ;
char x = '0';


const byte ROWS = 4; // the amount of rows on the keypad
const byte COLS = 4; // the amount of columns on the keypad
char keys[ROWS][COLS] = { // sets the rowns and columns
  // sets the keypad digits
  {'1', '2', '3', 'A'},

  {'4', '5', '6', 'B'},

  {'7', '8', '9', 'C'},

  {'*', '0', '#', 'D'}
};
bool SmartDoor = true; // the servo
// the pins to plug the keypad into
byte rowPins[ROWS] = {8, 7, 6, 9};
byte colPins[COLS] = {5, 4, 3, 2};
Keypad myKeypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS); // gets the data from the keypad

// locked charcater
byte Locked[8] = {
  B01110,
  B10001,
  B10001,
  B11111,
  B11011,
  B11011,
  B11011,
  B11111
};
// open character
byte Opened[8] = {
  B01110,
  B00001,
  B00001,
  B11111,
  B11011,
  B11011,
  B11011,
  B11111
};

void setup()
{
  Serial2.begin(115200);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  servo.attach(0); // attaches the servo to pin 0
  ServoClose(); // closes the servo when you say this function
  lcd.init(); // initializes the lcd
  lcd.backlight(); // turns on the backlight
  lcd.setCursor(5, 0); // sets the cursor on the lcd
  lcd.print("Welcome"); // prints the text/charater
  lcd.setCursor(6, 1); // sets the cursor on the lcd
  lcd.print("Door!"); // prints text
  delay(4000); // waits 4 seconds
  lcd.clear(); // clears the lcd diplay

}

void loop()
{
  controlServo();
}
void controlServo()
{
  if (SmartDoor == 0) // opens the smart door
  {
      doorclose();
  }


  else Open(); // keeps the door open
}

void clearData() // clears the data
{
  while (Particular_Count != 0) // counts the digits pressed
  {
    Particular[Particular_Count--] = 0; // counts how many digits
  }
  return; // returns the data
}

void ServoClose()
{
  for (Position = 120; Position >= 0; Position -= 5) { // moves from 0 to 180 degrees
    servo.write(Position); // moves to the postion
    delay(15); // waits 15 milliseconds
  }
}

void ServoOpen()
{
  for (Position = 0; Position <= 120; Position += 5) { // moves from position 0 to 180 degrees
    servo.write(Position); // moves to the position
    delay(15); // waits 15 milliseconds
  }
}

void Open()
{

  switch (x) {
    case '0':
      {
        hienthi(0, 0, "1.Enter Password");
        hienthi(1, 0, "2.Fingerprint");
        delay(500);
        while (x == '0')
        {
          Key = myKeypad.getKey();
          if (Key == '1')
          {
            x = '1'; //thay doi gia tri x tai day neu co case 1
            hienthi_clear(0, 0, "Enter Password");
            inputpassword();
            break;
          }
          if (Key == '2')
          {
            x = '2';
             hienthi_clear(0, 5, "Press");
             hienthi(1, 2, "Fingerprint");
            inputFingerprint();
            break;
          }
        }
        break;
      }
  }
}
void inputpassword()
{
  int i = 0;
  while (i < Password_Length - 1) {
    Key = myKeypad.getKey(); // gets the keys you press from the keypad
    if (Key)
    {
      i++;
      Particular[Particular_Count] = Key;
      lcd.setCursor(Particular_Count, 1); // sets the cursor on the lcd
      lcd.print("*"); // prints '*' instead of the password
      Particular_Count++; // counts the length of the password
    }
  }

  if (Particular_Count == Password_Length - 1) // gets the length of the password
  {
    if (strcmp(Particular, Specific)==0) // counts the length and checks to see if the password is correct
    {
      dooropen();
    }
    else
    {
      incorrectpass();
    }

    clearData(); // clears the data

  }
}

void inputFingerprint() {
  Serial2.print("<1>");
  Serial2.print("<0>");
  String temp =  receiveDatafromNodeMCU();

  while (1) {
    if (temp == "OpenDoor" || temp == "Wrong") {
      break;
    }
    else {
      temp =  receiveDatafromNodeMCU();
    }
  }
  if (temp == "OpenDoor") {
    dooropen();
  }
  else {
    incorrectpass();
  }
  clearData();
  x = '0';
  temp = "";
}
void hienthi(int hang, int cot, char* noidung) {
  lcd.setCursor(cot, hang);
  lcd.print(noidung);
}
void hienthi_clear(int hang, int cot, char* noidung) {
  lcd.clear();
  lcd.setCursor(cot, hang);
  lcd.print(noidung);
}
void baodong(int led) {
  int i = 0;
  while (i <= 3) {
    i++;
    digitalWrite(led, HIGH);
    tone(buzzer,450);
    delay(125);
    digitalWrite(led, LOW);
    noTone(buzzer);
    delay(125);
  }
}

void turnLedOn2(int led) {
  int i = 0;
  while (i <= 3) {
    i++;
    digitalWrite(led, HIGH);
    delay(125);
    digitalWrite(led, LOW);
    delay(125);
  }
}

void turnLedOn(int led){
  digitalWrite(led,HIGH);
  delay(200);
}
void turnLedOff(int led){
  digitalWrite(led,LOW);
  delay(200);
}

void dooropen(){
      dem = 0;
      lcd.clear();
      turnLedOn(GREEN_LED);
      ServoOpen(); // moves the servo 180 degrees
      lcd.setCursor(2, 0); // sets the cursor on the lcd
      lcd.print("Door Opened");
      lcd.createChar(1, Opened);
      lcd.setCursor(14, 0); // sets the cursor on the lcd
      lcd.write(1);
      SmartDoor = 0;
  }
void doorclose(){
    delay(5000); // change time
    lcd.clear(); // clears the lcd diplay
    ServoClose(); // closes the servo motor
    lcd.setCursor(2, 0); // sets the cursor on the lcd
    lcd.print("Door Closed"); // prints the text to the lcd
    lcd.createChar(0, Locked); // prints the locked character
    lcd.setCursor(14, 0); // sets the cursor on the lcd
    lcd.write(0);
    turnLedOff(GREEN_LED);
    turnLedOn(RED_LED);
    delay(4000);
    turnLedOff(RED_LED);
    SmartDoor = 1; // closes the door
    x = '0';
  }
void incorrectpass(){
      dem ++;
      if(dem == 3){
      lcd.clear();
      lcd.setCursor(0, 0); // sets the cursor on the lcd
      lcd.print("Warning!"); // prints the text/character
      lcd.setCursor(0, 1);
      lcd.print("Try Again In");
      int i = 5 ;
      while(i >=0){
      lcd.setCursor(13, 1);
      lcd.print(i);
      baodong(RED_LED);
      i--;
        }
      dem = 0;
      turnLedOff(RED_LED);
      lcd.clear();
      SmartDoor = 1; // closes the smart door
      x = '0';
        }
        else {
      lcd.clear();
      lcd.setCursor(0, 0); // sets the cursor on the lcd
      lcd.print("Wrong Password"); // prints the text/character
      lcd.setCursor(0, 1);
      lcd.print("Try Again In");
      int i = 5 ;
      while(i >=0){
      lcd.setCursor(13, 1);
      lcd.print(i);
      turnLedOn2(RED_LED);
      i--;
        }
      turnLedOff(RED_LED);
      lcd.clear();
      SmartDoor = 1; // closes the smart door
      x = '0';
        }

  }

String receiveDatafromNodeMCU() {
  byte n = Serial2.available();
  Serial2.readBytesUntil('>', recStr, 10);
  int x = atoi(recStr + 1);
  if (x == 1)
  {
    char recStr[10] = "";
    return "OpenDoor";
  }
  else if (x == 2) {
    char recStr[10] = "";
    return "Wrong";
  }
  else {
    char recStr[10] = "";
    return "Nope";
  }
}
