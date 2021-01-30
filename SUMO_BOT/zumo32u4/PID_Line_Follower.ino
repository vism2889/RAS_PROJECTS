/*  ORGANIZATION: Pitt-RAS
 *  AUTHORS:      Mark Hofmeister, Morgan Visnesky
 *  DATE:         12/21/2020
 *  FILENAME:     PID_Line_Follower.ino
 *  DESCRIPTION:
 *    Implementation of PID controller for arduino line-follower.
 *
 *    Of the 3 values Ki is the least often implemented in the PID configuration,
 *    and can be a cause of instability in your PID controller.
 */

#include <Wire.h>
#include <Zumo32U4.h>
#include "PID_CLASS/Sumo_PID.h"



const uint16_t maxSpeed = 200;

Zumo32U4LineSensors lineSensors;
Zumo32U4Motors motors;
Zumo32U4LCD lcd;
Zumo32U4ButtonA buttonA;
Zumo32U4ButtonC buttonC;

float Kp = 0.4; // Proportional Term
float Kd = 9; // Derivative Term
float Ki = 0; // Integral Term

double lastError = 0; // Error from last sensor reading.
double totalError = 0; // Accumulated error.
double derivError; // Derivative of error taken over the last time step

double previousTime = 0;
double elapsedTime;

#define numSensors 5
unsigned int lineSensorValues[numSensors];
int leftSpeed = 0, rightSpeed = 0;

//Necessary to calibrate for the environment
void calibrateSensors()
{
  lcd.clear();
  delay(1000);
  for(int i = 0; i < 120; i++)
  {
    if (i > 30 && i <= 90)
    {
      motors.setSpeeds(-200, 200);
    }
    else
    {
      motors.setSpeeds(200, -200);
    }
    lineSensors.calibrate();
  }
  motors.setSpeeds(0, 0);
}

void setup()
{
  //motors.flipLeftMotor(true);
  //motors.flipRightMotor(true);

  //Initialized sensors
  lineSensors.initFiveSensors();

  //Calibration loop
  lcd.clear();
  lcd.print(F("Press A"));
  lcd.gotoXY(0, 1);
  lcd.print(F("to calibrate"));
  buttonA.waitForButton();

  //Spins robt around to expose it to an environment of variable refelectance
  calibrateSensors();

  //Press A to Go
  lcd.clear();
  lcd.print(F("Press A"));
  lcd.gotoXY(0,1);
  lcd.print(F("to begin"));
  buttonA.waitForButton();

  delay(500);
  lcd.clear();
  lcd.print(F("Operating"));
}

void loop()
{
  double currentTime = millis();
  elapsedTime = (currentTime - previousTime);

  //Reads the line sensor values. If there is no error, and a black
  //line is detected, position will be 2000.
  int position = lineSensors.readLine(lineSensorValues);

  // 2000 means that the black line is directly below sensor #2 of the 5 sensor array.
  // sensors = [0 1 2 3 4], values = [0 1000 2000 3000 4000]
  // So when position reads 0 the black line is under sensor 0,
  // when position reads 4000 it is under sensor 4.

  int error = 2000 - position;
  totalError += error * elapsedTime;
  derivError = (error-lastError) / elapsedTime;

  //Uses PID control to adjust the speed
  int speedDifference = (Kp * error) + (Ki * totalError) + (Kd * derivError);
  lastError = error;

  //If the speed difference is positive, the right motor is going faster than the left.
  //This means that the right motor speed will be decreased by the speed difference.
   leftSpeed = (int)maxSpeed - speedDifference;
   rightSpeed = (int)maxSpeed + speedDifference;

  //The contrain function will instill a domain for the speed - it has to be
  // >= 0 and <= maxSpeed. This function will fix that.
  leftSpeed = constrain(leftSpeed, 0, (int)maxSpeed);
  rightSpeed = constrain(rightSpeed, 0, (int)maxSpeed);

  motors.setSpeeds(leftSpeed, rightSpeed);
  //Serial.print(position);

  previousTime = currentTime;
  if (buttonC.isPressed()) {
      motors.setSpeeds(0,0);
      exit(0);
  }
}
