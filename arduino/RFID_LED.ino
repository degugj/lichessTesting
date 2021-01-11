

/*<br>PINOUTS OF RFID CARD READER >> ARDUINO PINS
SDA >> 10
SCA >> 13
MOSI >> 11
MISO >> 12
RST >> 9
LED1 >> 6
*/
#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN 10
#define RST_PIN 9
const int LED1 = 6;
MFRC522 mfrc522(SS_PIN, RST_PIN);
void setup() 
{
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  pinMode(LED1, OUTPUT);
  digitalWrite(LED1,LOW);
  Serial.println("Put your card to the reader...");
  Serial.println();
}
void loop() 
{
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serial monitor
  Serial.print("UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.print("Message : ");
  content.toUpperCase();
  if (content.substring(1) == "D1 8A 29 83") //change here the UID of the card/cards that you want to give access
  {
    Serial.println("Authorized access");
    Serial.println();
    digitalWrite(LED1, HIGH);
  }
  else 
  //if (content.substring(1) == "6A 34 D9 AB") 
  {
    Serial.println(" Access denied"); 
    Serial.println();
    digitalWrite(LED1, LOW);
  }
}


