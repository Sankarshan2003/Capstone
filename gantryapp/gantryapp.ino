#define TOP_DEBUG true
#define FUNC_DEBUG true
#define RUN_TO_POS true


#include "gantry.h"
#include "SerialTransfer.h"


void setup() {
  Serial.begin(115200);
  pinMode(30, OUTPUT);
}


void loop() {
  uint16_t sendSize = 0;
  uint16_t recSize = 0;


  static float distX, distY, distZ, endd, end_servo;
  bool oneByOne = true;

  if (Serial.available() > 0) {
    char input[128];                                   // Assuming a reasonable buffer size
    Serial.readBytesUntil(';', input, sizeof(input));  // Read until the semicolon (;)
    input[sizeof(input) - 1] = '\0';                   // Null-terminate the string

    char* token = strtok(input, " ");
    if (token != NULL) {
      distX = atof(token);

      token = strtok(NULL, " ");
      if (token != NULL) {
        distY = atof(token);

        token = strtok(NULL, " ");
        if (token != NULL) {
          distZ = atof(token);

          token = strtok(NULL, " ");
          if (token != NULL) {
            endd = atof(token);

            token = strtok(NULL, " ");
            if (token != NULL) {
              end_servo = atof(token);

              // Serial.print("X: ");
              Serial.print(distX);
              // Serial.print(", Y: ");
              Serial.print(distY);
              // Serial.print(", Z: ");
              Serial.print(distZ);
              // Serial.print(", Servo: ");
              Serial.println(end_servo);

              if (distX != -1 && distY != -1 && distZ != -1) {
                //  goTozXY(distX,distY,distZ);
                end_servo_rot(end_servo);
                goToXYZ(distX, distY, distZ, oneByOne);
                if (endd == 0) {
                  gripperClose(0);
                } else if (endd == 1) {
                  gripperClose(20);
                }
                Serial.println("j");
              } else if (distX == -1 && distY == -1 && distZ == -1 && endd == 2) {
                initSystem();
                goHome();
                Serial.println("Home done");
              } else if (distX == -1 && distY == -1 && distZ == -1 && endd == 5) {
                digitalWrite(40, HIGH);
                goToXYZ(600, 500, 0, oneByOne);
                goToXYZ(0, 0, 0, oneByOne);
              } else if (distX == -1 && distY == -1 && distZ == -1 && endd == 6) {
                digitalWrite(40, HIGH);
              } else if (distX == -1 && distY == -1 && distZ == -1 && endd == 3) {
                digitalWrite(40, LOW);
              } else if (distX == -1 && distY == -1 && distZ == -1) {
                if (endd == 0) {
                  gripperClose(0);
                } else if (endd == 1) {
                  gripperClose(20);
                }
              }
              if (distX == -1 && distY == -1 && distZ == -1) {
                if (endd == 9) {
                  end_servo_rot(end_servo);
                  Serial.println("r");
                }
              }
            }
          }
        }
      }
    }
  }
}
