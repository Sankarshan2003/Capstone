
#include <AccelStepper.h>
#include <Servo.h>
#include "gantry.h"


#define xSTEP_PIN 2
#define xDIR_PIN 5
#define xlimit 9

#define ySTEP_PIN 3
#define yDIR_PIN 6
#define ylimit 10

#define zSTEP_PIN 4
#define zDIR_PIN 7
#define zlimit 11

#define INIT_X_HOMING -1
#define INIT_Y_HOMING -1
#define INIT_Z_HOMING -1


const float mmPerRevX = 60;
const float mmPerRevY = 60;
const float mmPerRevZ = 8;

const int stepsPerRevX = 400;
const float stepsPerMmX = stepsPerRevX / mmPerRevX;

const int stepsPerRevY = 800;
const float stepsPerMmY = stepsPerRevY / mmPerRevY;

const int stepsPerRevZ = 400;
const float stepsPerMmZ = stepsPerRevZ / mmPerRevZ;

static Servo servoMotor;  // Gripper
const int servoPin = 45;  // Define the servo pin
static int accu_state = 0;

static Servo endServo;  // Rotater
const int servoPinR = 44;

static AccelStepper stepperx(AccelStepper::DRIVER, xSTEP_PIN, xDIR_PIN);
static AccelStepper steppery(AccelStepper::DRIVER, ySTEP_PIN, yDIR_PIN);
static AccelStepper stepperz(AccelStepper::DRIVER, zSTEP_PIN, zDIR_PIN);

// void end_servo_rot(int);

void initSystem() {

  servoMotor.attach(servoPin);
  servoMotor.write(0);

  endServo.attach(servoPinR);
  endServo.write(3);

  pinMode(xlimit, INPUT_PULLUP);
  pinMode(ylimit, INPUT_PULLUP);
  pinMode(ylimit, INPUT_PULLUP);
  pinMode(zlimit, INPUT_PULLUP);
}

void getCurrPos() {
  int xx = stepperx.currentPosition();
  int zz = stepperz.currentPosition();
  int yy = steppery.currentPosition();
}
void goHome(void) {
  Serial.println("Homing");
  goHomeZ();
  goHomeY();
  goHomeX();


  //   stepperx.setMaxSpeed(13000.0);
  //  stepperx.setAcceleration(650.0);

  //   steppery.setMaxSpeed(20000.0);
  //  steppery.setAcceleration(1000.0);

  //   stepperz.setMaxSpeed(15000.0);
  //   stepperz.setAcceleration(12000.0);
  stepperx.setMaxSpeed(15000.0);
  stepperx.setAcceleration(4000);

  steppery.setMaxSpeed(32000.0);
  steppery.setAcceleration(18000.0);

  stepperz.setMaxSpeed(60000.0);
  stepperz.setAcceleration(25000.0);
  // stepperx.setMaxSpeed(12000.0);
  // stepperx.setAcceleration(3500.0);

  // steppery.setMaxSpeed(32000.0);
  // steppery.setAcceleration(18000.0);

  // stepperz.setMaxSpeed(40000.0);
  // stepperz.setAcceleration(20000.0);
  Serial.println("h");
}
void goHomeX() {

  delay(5);

  stepperx.setMaxSpeed(8000.0);
  stepperx.setAcceleration(4000.0);

  long initial_homing = INIT_X_HOMING;

  while (digitalRead(xlimit)) {
    stepperx.moveTo(initial_homing);
    initial_homing--;
    stepperx.run();
    delay(2);
  }

  stepperx.setCurrentPosition(0);
  stepperx.setMaxSpeed(6000.0);
  stepperx.setAcceleration(3000.0);
  initial_homing = -INIT_X_HOMING;

  while (!digitalRead(xlimit)) {
    stepperx.moveTo(initial_homing);
    stepperx.run();
    initial_homing++;
    delay(2);
  }

  stepperx.setCurrentPosition(0);
}
void goHomeY() {

  ///////////////////////////////////////////////////////////
  delay(5);

  steppery.setMaxSpeed(12000.0);
  steppery.setAcceleration(8000.0);

  long initial_homing = INIT_Y_HOMING;

  while (digitalRead(ylimit)) {
    steppery.moveTo(initial_homing);
    initial_homing--;
    steppery.run();
    delay(2);
  }

  steppery.setCurrentPosition(0);
  steppery.setMaxSpeed(6000.0);
  steppery.setAcceleration(3000.0);

  initial_homing = -INIT_Y_HOMING;

  while (!digitalRead(ylimit)) {
    steppery.moveTo(initial_homing);
    steppery.run();
    initial_homing++;
    delay(2);
  }

  steppery.setCurrentPosition(0);
  ///////////////////////////////////////////////////////////////
}
void goHomeZ() {

  delay(5);

  stepperz.setMaxSpeed(8000.0);
  stepperz.setAcceleration(1000.0);


  long initial_homing = INIT_Z_HOMING;

  while (digitalRead(zlimit)) {
    Serial.println(digitalRead(zlimit));
    stepperz.moveTo(initial_homing);
    initial_homing--;
    stepperz.run();
    delay(2);
  }

  stepperz.setCurrentPosition(0);
  stepperz.setMaxSpeed(6000.0);
  stepperz.setAcceleration(3000.0);

  initial_homing = -INIT_Z_HOMING;

  while (!digitalRead(zlimit)) {
    Serial.println(digitalRead(zlimit));
    stepperz.moveTo(initial_homing);
    stepperz.run();
    initial_homing++;
    delay(2);
  }

  stepperz.setCurrentPosition(0);


  //////////////////////////////////////////////////////////////
}



#define MAX_X_STEPS   7000

void goToX(float x_in)
{
    int stepsToMoveX = int(x_in * stepsPerMmX);
    if (stepsToMoveX >MAX_X_STEPS) 
        stepsToMoveX = MAX_X_STEPS;

    stepperx.moveTo(stepsToMoveX);
    // stepperx.setSpeed(5000);
    while (stepperx.distanceToGo() != 0) {
        stepperx.run();
  
    }

}

#define MAX_Y_STEPS   11000
void goToY(float y_in)
{
    int stepsToMoveY = int(y_in * stepsPerMmY); 
    if (stepsToMoveY >MAX_Y_STEPS) 
        stepsToMoveY = MAX_Y_STEPS;

    steppery.moveTo(stepsToMoveY);
    while (steppery.distanceToGo() != 0) {
        steppery.run();
      
    }
}

#define MAX_Z_STEPS   8500

void goToZ(float z_in)
{
    int stepsToMoveZ = int(z_in * stepsPerMmZ);
    if (stepsToMoveZ >MAX_Z_STEPS) 
        stepsToMoveZ = MAX_Z_STEPS;

    stepperz.moveTo(stepsToMoveZ);
    while (stepperz.distanceToGo() != 0) {
        stepperz.run();
    }

}
void goToXYZ(float x_in, float y_in, float z_in, bool oneByOne_in) {

  Serial.println("gotoXYZ()");

  if (oneByOne_in == true) {
   // goToZ(z_in);
    //goToY(y_in);
    goToX(x_in);

    Serial.println("d");
  } else {
    // goToZ(z_in);
    int stepsToMoveX = int(x_in * stepsPerMmX);
    int stepsToMoveY = int(y_in * stepsPerMmY);
    int stepsToMoveZ = int(z_in * stepsPerMmZ);
    stepperx.moveTo(stepsToMoveX);
    steppery.moveTo(stepsToMoveY);
    stepperz.moveTo(stepsToMoveZ);

    bool xDone = false;
    bool yDone = false;
    bool zDone = false;

    while ((xDone == false) || (yDone == false) || (zDone == false)) {
      if (zDone == false) {
        if (stepperz.distanceToGo() != 0)
          stepperz.run();
        else
          zDone = true;
      }
      if (xDone == false) {
        if (stepperx.distanceToGo() != 0)
          stepperx.run();
        else
          xDone = true;
      }
      if (yDone == false) {
        if (steppery.distanceToGo() != 0)
          steppery.run();
        else
          yDone = true;
      }
    }
    if (xDone == true && zDone == true && yDone == true) {
      Serial.println("goXYZ() Done");
      Serial.println("d");
    }
  }
  Serial.println("goXYZ() Done");
}

void goTozXY(float x_in, float y_in, float z_in) {
  int stepsToMoveX = int(x_in * stepsPerMmX);
  int stepsToMoveY = int(y_in * stepsPerMmY);
  int stepsToMoveZ = int(z_in * stepsPerMmZ);
  stepperx.moveTo(stepsToMoveX);
  steppery.moveTo(stepsToMoveY);
  stepperz.moveTo(stepsToMoveZ);

  bool xDone = false;
  bool yDone = false;
  bool zDone = false;

  while ((xDone == false) || (yDone == false)) {
    if (xDone == false) {
      if (stepperx.distanceToGo() != 0)
        stepperx.run();
      else
        xDone = true;
    }
    if (yDone == false) {
      if (steppery.distanceToGo() != 0)
        steppery.run();
      else
        yDone = true;
    }
  }

  while (zDone == false) {

    if (zDone == false) {
      if (stepperz.distanceToGo() != 0)
        stepperz.run();
      else
        zDone = true;
    }
  }
  if (xDone == true && zDone == true && yDone == true) {
    Serial.println("d");
  }
}
void goToXYandZ(float x_in, float y_in, float z_in) {
  int stepsToMoveX = int(x_in * stepsPerMmX);
  int stepsToMoveY = int(y_in * stepsPerMmY);
  int stepsToMoveZ = int(z_in * stepsPerMmZ);
  stepperx.moveTo(stepsToMoveX);
  steppery.moveTo(stepsToMoveY);
  stepperz.moveTo(stepsToMoveZ);

  bool xDone = false;
  bool yDone = false;
  bool zDone = false;
  while (zDone == false) {

    if (zDone == false) {
      if (stepperz.distanceToGo() != 0)
        stepperz.run();
      else
        zDone = true;
    }
  }
  while ((xDone == false) || (yDone == false)) {
    if (xDone == false) {
      if (stepperx.distanceToGo() != 0)
        stepperx.run();
      else
        xDone = true;
    }
    if (yDone == false) {
      if (steppery.distanceToGo() != 0)
        steppery.run();
      else
        yDone = true;
    }
  }
}

//#define GRIP_OPEN_ROTATION  25
void gripperOpen(int grip) {
  servoMotor.write(grip);
}

//#define GRIP_CLOSE_ROTATION  5

void gripperClose(int grip) {
  servoMotor.write(grip);
  delay(100);
  Serial.println("e");
}

void end_servo_rot(int grip) {
  endServo.write(grip);
  delay(50);
  Serial.println("e");
  // Serial.println("d");
}

void goToSource(int x_in, int y_in, int z_in) {

  gripperOpen(18);

  goTozXY(x_in, y_in, z_in);
  if (stepperz.distanceToGo() == 0) {
    //   gripperClose(0);
    //   delay(1000);
  }
}

void goToDest(int x_in, int y_in, int z_in) {
  goToZ(100);
  goTozXY(x_in, y_in, z_in);
  if (stepperz.distanceToGo() == 0) {
    gripperOpen(18);
    delay(500);
    goToZ(100);
  }
}


void goStepsX(int stepx_in) {
}
void goStepsY(int stepy_in) {
}
void goStepsZ(int stepz_in) {
}
void goStepsXYZ(int stepx_in, int stepy_in, int stepz_in) {
}
