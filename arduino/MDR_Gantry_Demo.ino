 // include the library code: 
// LCD Library and Stepper Motor Library

#include <LiquidCrystal.h>
#include <Stepper.h>

// Declaration of Switch Pin on Encoder
const int SW = 10; 

//Stepper motor configuration
const int stepsPerRevolution = 200;
Stepper StepperX(stepsPerRevolution, A2, A3, A4, A5);
Stepper StepperY(stepsPerRevolution, 11, 12, A0, A1);

//Rotatry Encoder Settings
//Interrupt Declarations
static int pinA = 2;
static int pinB = 3;
volatile byte aFlag = 0;
volatile byte bFlag = 0;
int  encoderPos = 0;  //no. of turns on encoder
volatile byte oldEncPos = 0;
volatile byte reading = 0;

// LCD Interfacing
const int rs = 5, en = 4, d4 = 6 , d5 = 7, d6 = 8, d7 = 9;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//Variable Declaration
int stepX; //No. of steps in X direction
int stepY; //No. of steps in Y direction


void setup() {
  //Speed set (rpm)
  StepperX.setSpeed(60);
  StepperY.setSpeed(60);
  //Initialize LCD
  lcd.begin(16, 2);
  lcd.print("    Team 10");
  lcd.setCursor(0,1);
  lcd.println(" MDR Gantry Test");
  delay(500);
  lcd.clear();
 
  //Initial Settings for Button
  pinMode(SW,INPUT);
  digitalWrite(SW,HIGH);
  
 //Interrupt Settings
  pinMode(pinA, INPUT_PULLUP);
  pinMode(pinB, INPUT_PULLUP);
  attachInterrupt(0,PinA,RISING);
  attachInterrupt(1,PinB,RISING);
}

//Interrupt for Rotatry Encoder

void PinA(){
  cli();
  reading = PIND & 0xC;
  if(reading == B00001100 && aFlag) {
    encoderPos --; 
    bFlag = 0;
    aFlag = 0;
  }
  else if (reading == B00000100) bFlag = 1;
  sei();
}

void PinB(){
  cli();
  reading = PIND & 0xC;
  if (reading == B00001100 && bFlag) { 
    encoderPos ++; 
    bFlag = 0; 
    aFlag = 0; 
  }
  else if (reading == B00001000) aFlag = 1; 
  sei(); 
}

//declaration of edit
// edit = 0 >> Standby
// edit = 1 >> Set settings for stepX
// edit = 2 >> Set settings for stepY
// edit = 3 >> Running stepper motors. Step X in X direction first Step Y in Y direction second.Then revert to standby
int edit = 0;


void loop() {
 
   if (digitalRead(SW)==0){
    //simple debounce
    delay(200);
    
    //change edit to next edit stage
    //reset encoderPos
    if (edit == 0){
      edit=1;
      encoderPos = 0;
      }
    else if (edit == 1){
      edit =2;
      encoderPos = 0;
      }
    else if (edit == 2){
      edit =3;
      encoderPos = 0;
      }
     else if (edit == 3){
      edit =0;
      encoderPos = 0;
      }
    }
    

//Edit=1 Set StepX number. Read encoderPos, and set stepX
  if ( edit==1){
    lcd.blink();
    stepX = encoderPos*10;
   
        lcd.setCursor(0,1);
        lcd.print("         ");
        lcd.setCursor(1,1);
        lcd.print(stepX);
        delay(30);
    } 
  else if ( edit==2){ //set StepY number
    lcd.blink();
    stepY = encoderPos*10;
   
        lcd.setCursor(9,1);
        lcd.print("       ");
        lcd.setCursor(9,1);
        lcd.print(stepY);
        delay(30);
    }
  else if ( edit==3){  //Run Gantry for X direction then Y direction
      lcd.noBlink();
      lcd.setCursor(15,0);
      lcd.print(edit);
      lcd.setCursor(0,1);
      lcd.print("   Running....");
      StepperX.step(stepX);
      delay(500);
      StepperY.step(stepY);
      delay(500);
      stepX=0;
      stepY=0;
      lcd.setCursor(0,1);
      lcd.print("   COMPLETED    ");
      delay(1000);
      edit = 0;
    }
  else if ( edit==0){ //Standby
    lcd.noBlink();
    lcd.setCursor(0,1);
    lcd.print(" PRESS ENTER    ");
    }
  
 //LCD Display Update
  lcd.setCursor(0,0);
  lcd.print("StepX ");
  lcd.setCursor(8,0);
  lcd.print("StepY ");
  lcd.setCursor(15,0);
  lcd.print(edit);
}
