#include <Servo.h>


const int leftMotorForward = 3;
const int leftMotorBackward = 5;

const int rightMotorForward = 10;
const int rightMotorBackward = 11;

const int servoPin = 7;


Servo steeringServo;

void setup() {

  pinMode(leftMotorForward, OUTPUT);
  pinMode(leftMotorBackward, OUTPUT);
  pinMode(rightMotorForward, OUTPUT);
  pinMode(rightMotorBackward, OUTPUT);


  steeringServo.attach(servoPin);


  Serial.begin(9600);
}

void loop() {

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  

    if (command == "forward") {
      driveForward();
    } 
    else if (command == "backward") {
      driveBackward();
    } 
    else if (command == "left") {
      turnLeft();
    } 
    else if (command == "right") {
      turnRight();
    } 
    else if (command == "stop") {
      stopCar();
    }
  }
}

void driveForward() {
  analogWrite(leftMotorForward, 100);
  analogWrite(leftMotorBackward, 0);
  analogWrite(rightMotorForward, 100);
  analogWrite(rightMotorBackward, 0);
}

void driveBackward() {
  analogWrite(leftMotorForward, 0);
  analogWrite(leftMotorBackward, 100);
  analogWrite(rightMotorForward, 0);
  analogWrite(rightMotorBackward, 100);
}

void turnLeft() {    // 방향 전환시 감속
  steeringServo.write(70);   // 조향 각도

  analogWrite(leftMotorForward, 50);
  analogWrite(leftMotorBackward, 0);
  analogWrite(rightMotorForward, 50);
  analogWrite(rightMotorBackward, 0);
}

void turnRight() {
  steeringServo.write(110);  // 조향 각도
  
  analogWrite(leftMotorForward, 50);
  analogWrite(leftMotorBackward, 0);
  analogWrite(rightMotorForward, 50);
  analogWrite(rightMotorBackward, 0);
}

void stopCar() {
  analogWrite(leftMotorForward, 0);
  analogWrite(leftMotorBackward, 0);
  analogWrite(rightMotorForward, 0);
  analogWrite(rightMotorBackward, 0);
  steeringServo.write(90); 
}