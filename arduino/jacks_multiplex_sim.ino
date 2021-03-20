 /*
  Arduino Slave for Raspberry Pi Master
  i2c_slave_ard.ino
  Connects to Raspberry Pi via I2C
  
  DroneBot Workshop 2019
  https://dronebotworkshop.com
*/
 
// Include the Wire library for I2C
#include <Wire.h>

bool isFastScanOn = false;
int startFS = 0b00110000;
int stopFS = 0b00111000;
int typeMask = 0b11111000;

void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  Serial.begin(115200);
  // Call receiveEvent when data received                
  Wire.onRequest(requestEvent);
  Wire.onReceive(recEvent);
}

String returnMessageType(char inputByte){
  String typeMessage = "UNKNOWN";
  //Serial.println(int(inputByte & typeMask));
  //Serial.println(int(startFS));
  //Serial.println(int(inputByte & typeMask) == int(startFS));
  if(int(inputByte & typeMask) == int(startFS)){
    typeMessage = "start";
  }
  if(int(inputByte & typeMask) == int(stopFS)){
    typeMessage = "stop";
  }
  return typeMessage;
}

// Function that executes whenever data is received from master
void requestEvent(int howMany) {
  Serial.println("Req Functioning Executing");
  if(isFastScanOn){
    // If FS On, return gamestate
    Serial.println("Transmitting Message");
    Serial.println(0xFF, BIN);
    Wire.write(0xFF);
  }else{
    Serial.println("Transmitting Message");
    Serial.println(0xF0, BIN);
    Wire.write(0xF0);
  }
}

void recEvent(int howMany) {
  char recByte = Wire.read();
  String messageType = returnMessageType(recByte);
  Serial.println("Received Message Type: "+messageType);
  Serial.println(recByte, BIN);
  if(messageType == "start"){
    Serial.println("Set FS boolean");
    isFastScanOn = true;
  }
  if(messageType == "stop"){
    isFastScanOn = false;
  }
}
void loop() {
  delay(100);
  //read start fast scan

  //
}
