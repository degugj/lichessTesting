   //////////////////////////////////////////////
  //        HALL EFFECT SENSOR DEMO           //
 //          Author: Nick Koumaris           //
//           http://www.educ8s.tv           //
/////////////////////////////////////////////
// using a1104lua-t //

const int ledPin = 13;
const int hallPin = 2;
int hallState = 0;

void setup() 
{
  Serial.begin(9600);
  pinMode(ledPin,OUTPUT);
  pinMode(hallPin,INPUT);
  //attachInterrupt(digitalPinToInterrupt(hallPin), hall_ISR, CHANGE);
}

void loop() 
{
// read the state of the hall effect sensor:
  hallState = digitalRead(hallPin);

  if (hallState == LOW) {     
    // turn LED on:    
    digitalWrite(ledPin, HIGH);
    Serial.println("Detect");
  }   
  else {
    // turn LED off:
    digitalWrite(ledPin, LOW); 
  }
}
