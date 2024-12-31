import cameraModules.realsense.camera_rs as cam
import cv2 as cv
import robotInterfaces as rb
import objDetInterface as objDet
import barcodeReader as barReader
import time
import archiving_funcs as func
import pallet_pos as pPos
import multiprocessing
robot = rb.Robot('gantry', 'COM3')
robot.home()