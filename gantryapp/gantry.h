#ifndef GANTRY_H
#define GANTRY_H

/****************************************
    funciton name: 

    parameters:

    returns

    Description:
           This is to initialise hardware and software components
           1) Set up Pins

  *************************************/
void initSystem();
void goHome(void);
void goHomeX();
void goHomeY();
void goHomeZ();

void goToX(float x_in);
void goToY(float y_in);
void goToZ(float z_in);
void goToXYZ(float x_in, float y_in, float z_in);

void goStepsX(int stepx_in);
void goStepsY(int stepy_in);
void goStepsZ(int stepz_in);
void goToXYZ(float x_in, float y_in, float z_in, bool oneByOne_in);
void goTozXY(float x_in, float y_in, float z_in);
void goToXYandZ(float x_in, float y_in, float z_in);
void gripperOpen(int grip);
void gripperClose(int grip);
void goToSource(int x_in,int y_in,int z_in);
void goToDest(int x_in,int y_in,int z_in);
void gripperRotate(float angle_in);
void end_servo_rot(int grip);


#endif
