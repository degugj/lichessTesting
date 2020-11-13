/*
Arduino Code for TestBench
Connections Defined
Sample Codes used from library examples

LCD Outputs 
AnH  Analog Hall Sensor Reading Value  -512 to +512 (Analog Read Value from calibrated “0”G value)
EM  Electromagnet Settings  OFF / 100% to -100% (Electromagnet Power +/- Polarity)
DH  Digital Hall Sensor Value 0 – Magnet Not Present / 1 – Magnet Present
RFID  RFID Tag Unique ID  UID Number of RFID Tag Present

Arduino Nano  MCU for Testbench. Connect sensors, motor controllers, switches, and LCD.
LCD Screen  Display hall sensor values, motor controller settings, and RFID output.
Potentiometer Controls output strength of Motor Controller for Electromagnet
Switch  Turns Electromagnet ON/OFF
12v Power 12v power input. Required for Electromagnet. Can also power the whole system .
5v Power  Power for whole system except Electromagnet.
Arm Electromagnet and RFID reader attached. Allows for free movement to mimic gantry.

*/

#include <LiquidCrystal.h>
#include <SparkFun_TB6612.h>

//LCD Connection
#define rs A3
#define en 8
#define d4 4
#define d5 5 
#define d6 6
#define d7 7
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
  
//HALL SENSORr
#define hall A2
int sensorValue;
int calibrate;
  
//Motor Controller
#define SW A5
#define AIN1 A0
#define AIN2 A1
#define PWMA 3
#define STBY 2
int PWR;
const int offsetA = 1;
Motor motor = Motor(AIN1, AIN2, PWMA, offsetA, STBY);
int driveStrength;  //MAX 255
#define vPot A6   //Electromagnet Control

// RFID
#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN 10
#define RST_PIN 9
byte readCard[4];
String tagID = "";
MFRC522 mfrc522(SS_PIN, RST_PIN);



void setup() {
  pinMode(A4,INPUT); //Digital Hall Sensor
  SPI.begin();       // Initialize SPI bus
  mfrc522.PCD_Init(); // Initialize MFRC522


  lcd.begin(16, 2);
  lcd.print("Team10 Testbench");
  delay(500);
  lcd.clear();
  
// Calibration Sequence Wait 4 Secs to Calibrate
  lcd.print("Calibrate HALL");
  lcd.setCursor(0,1);
  lcd.print("Remove Magnets");
  delay(800);
  
  lcd.clear();
  lcd.print("Remove Magnets");
  lcd.setCursor(0,1);
  lcd.print("Calibrating...");
  lcd.setCursor(15,1);
  int var=4;
  while (var > -1) {
  // do something repetitive 200 times
  lcd.setCursor(15,1);
  lcd.print(var);
  var--;
  delay(800);
}

  calibrate = analogRead(hall);
  lcd.clear();
  lcd.print("Calibrated");
  lcd.setCursor(3,1);
  lcd.print(calibrate);
  delay(1000);
  lcd.clear();
  lcd.print("Ready");
  lcd.clear();
  
}

void loop() {
  
  //Digital hall Sensor Read
  int halle;
  halle=digitalRead(A4);
  //Potentiometer Value
  int pot;
  pot = analogRead(vPot)/2;
  
  //Calculate EM drivestrength from POT
  driveStrength = (256-pot);
  if (driveStrength == 256){
    driveStrength = 255;
    }
  //Hall Sensor Read and Display
  sensorValue = analogRead(hall);
  lcd.setCursor(0,1);
  lcd.print("    ");
  lcd.setCursor(0,1);
  lcd.print(sensorValue-calibrate);
  lcd.setCursor(0,0);
  lcd.print("AnH");
  
  //Digital hall sensor Display
  lcd.setCursor(9,0);
  lcd.print("DH");
  lcd.setCursor(9,1);
  lcd.print(1-halle);

  //EM Control Power and Strength
  PWR = digitalRead(A5);
  
  if (PWR == 1){
  lcd.setCursor(4,0);
  lcd.print("EM");
  lcd.setCursor(4,1);
  lcd.print("     ");
  lcd.setCursor(4,1);
  lcd.print((driveStrength*100)/255);
  lcd.print("%");
  motor.drive(driveStrength);
    }  
  if (PWR == 0){
  lcd.setCursor(4,0);
  lcd.print("EM");
  lcd.setCursor(4,1);
  lcd.print("     ");
  lcd.setCursor(4,1);
  lcd.print("OFF");
  motor.brake();
    }

  //RFID Display
  delay(10);
  lcd.setCursor(12,0);
  lcd.print("RFID");
  lcd.setCursor(12, 1);
  lcd.print("    ");
  lcd.setCursor(12, 1);
  //Tag Not Present
  lcd.print("NO");
  //Tag Present
  if (getID()){
    lcd.setCursor(12, 1);
    lcd.print(tagID);
      delay(1000);
      }
}


boolean getID() 
{
  // Getting ready for Reading PICCs
  if ( ! mfrc522.PICC_IsNewCardPresent()) { //If a new PICC placed to RFID reader continue
  return false;
  }
  if ( ! mfrc522.PICC_ReadCardSerial()) { //Since a PICC placed get Serial and continue
  return false;
  }
  tagID = "";
  for ( uint8_t i = 0; i < 4; i++) { // The MIFARE PICCs that we use have 4 byte UID
  //readCard[i] = mfrc522.uid.uidByte[i];
  tagID.concat(String(mfrc522.uid.uidByte[i], HEX)); // Adds the 4 bytes in a single String variable
  }
  tagID.toUpperCase();
  mfrc522.PICC_HaltA(); // Stop reading
  return true;
}
