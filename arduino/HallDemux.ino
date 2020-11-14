int AB = 10;

int Y1 = 11;
int Y2 = 12;

int hallState1 = 0;
int hallState2 = 0;
int hallState3 = 0;
int hallState4 = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(AB,OUTPUT);

  pinMode(Y1,INPUT);
  pinMode(Y2,INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(AB, LOW);   // Set AB to LOW
  hallState1 = digitalRead(Y1);
  delay(100);
  digitalWrite(AB, HIGH);
  hallState2 = digitalRead(Y1);
  delay(100);
  digitalWrite(AB, LOW);
  hallState3 = digitalRead(Y2);
  delay(100);
  digitalWrite(AB, HIGH);
  hallState4 = digitalRead(Y2);
  delay(100);


  if (hallState1 == LOW) {
    Serial.println("Detect hall sensor 1");
  }

  if (hallState2 == LOW) {
    Serial.println("Detect hall sensor 2");
  }

  if (hallState3 == LOW) {
    Serial.println("Detect hall sensor 3");
  }

  if (hallState4 == LOW) {
    Serial.println("Detect hall sensor 4");
  }

}
