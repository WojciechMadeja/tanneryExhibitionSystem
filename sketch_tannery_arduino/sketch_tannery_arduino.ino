#include <IRremote.h>        //Library IR
int led = 13;                //LED for send process
int sensor = 2;              //PIN for sensor PIR
int state = LOW;             
int val = 0;                 // variable to store the sensor status (value)
const int RECV_PIN = 7;
IRrecv irrecv(RECV_PIN);
decode_results results;
unsigned long key_value = 0;


void setup() {
  pinMode(led, OUTPUT);      // initalize LED as an output
  pinMode(sensor, INPUT);    // initialize sensor as an input
  irrecv.enableIRIn();
  irrecv.blink13(true);
  Serial.begin(9600);        // initialize serial
}

void loop() {
  val = digitalRead(sensor);   // read sensor value
  if (val == HIGH) {           // check if the sensor is HIGH
    digitalWrite(led, HIGH);   // turn LED ON
    delay(1500);
    Serial.println(1);         // print information for Raspberry Pi
    digitalWrite(led, LOW);    // turn LED OFF
  }

  if (irrecv.decode(&results)) {     // check if any remote's button pressed

    if (results.value == 0XFFFFFFFF) 
      results.value = key_value;

    switch (results.value) {         // case for Raspberry Pi which button pressed
      case 0xFFE01F:
        Serial.println("-vol");      //volume down information for RPi 
        delay(500);
        break;
      case 0xFFA857:
        Serial.println("+vol");      //volume up information for RPi
        delay(500);
        break;
      case 0xFFC23D:
        Serial.println("mute");      //mute information for RPi
        delay(500);
        break;
      case 0xFF30CF:
        Serial.println("a");         //front speakers  volume mode
        delay(500);
        break;
      case 0xFF18E7:
        Serial.println("b");         //back speakers volume mode
        delay(500);
        break;
      case 0xFF7A85:
        Serial.println("c");         //off speakers volume mode
        delay(500);
        break;
    }
    key_value = results.value;
    irrecv.resume();
  }
}
