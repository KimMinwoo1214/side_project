#include <Servo.h>
#include <U8x8lib.h>

Servo base;
Servo shoulder;
Servo upperarm;
Servo forearm;

int baseAngle = 90;
int shoulderAngle = 90;
int upperarmAngle = 90;
int forearmAngle = 90;

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

U8X8_SSD1306_128X64_NONAME_HW_I2C u8x8(/* reset=*/ U8X8_PIN_NONE);

int servoParallelControl(int thePos, Servo theServo, int speed) {
  int startPos = theServo.read();
  int newPos = startPos;

  if (startPos < thePos) {
    newPos = newPos + 1;
    theServo.write(newPos);
    delay(speed);
    return 0;
  } else if (newPos > thePos) {
    newPos = newPos - 1;
    theServo.write(newPos);
    delay(speed);
    return 0;
  } else {
    return 1;
  }
}

void clear_oled() {
  u8x8.setFont(u8x8_font_chroma48medium8_r);
  u8x8.clearDisplay();
  delay(100);
}

void setup() {
  Serial.begin(115200);
  base.attach(3);
  base.write(baseAngle);
  shoulder.attach(5);
  shoulder.write(shoulderAngle);
  upperarm.attach(6);
  upperarm.write(upperarmAngle);
  forearm.attach(9);
  forearm.write(forearmAngle);
  u8x8.begin();
  u8x8.setPowerSave(0);
}

void loop() {
  if (Serial.available() > 0) {
    String inString = Serial.readStringUntil('\n');
    
    int firstComma = inString.indexOf(',');
    int secondComma = inString.indexOf(',', firstComma + 1);
    int thirdComma = inString.indexOf(',', secondComma + 1);
    
    baseAngle = inString.substring(0, firstComma).toInt();
    shoulderAngle = inString.substring(firstComma + 1, secondComma).toInt();
    upperarmAngle = inString.substring(secondComma + 1, thirdComma).toInt();
    forearmAngle = inString.substring(thirdComma + 1).toInt();

    int status1 = 0, status2 = 0, status3 = 0, status4 = 0;
    int done = 0;

    while (done == 0) {
      status1 = servoParallelControl(baseAngle, base, 20);
      status2 = servoParallelControl(shoulderAngle, shoulder, 20);
      status3 = servoParallelControl(upperarmAngle, upperarm, 20);
      status4 = servoParallelControl(forearmAngle, forearm, 20);

      if (status1 == 1 && status2 == 1 && status3 == 1 && status4 == 1) {
        done = 1;
      }
    }

    clear_oled();
    u8x8.drawString(0, 0, inString.c_str());
  }
}
