""""
///////////////////////////////////////////////////////////////////////
//                                                                   //
//                       Segment House v1                            //
//                        Luis  Lujano, 13-10775                     //
//                       Jaime Villegas, 13-11493                    //
///////////////////////////////////////////////////////////////////////
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt



# Convert to BGR to HSV

directory = 'Sensor_Data2'
a= os.listdir(directory)
Distance_matrix = np.array([])
Voltage_matrix = np.array([])
for element in a:
    imBGR = cv2.imread(directory+'/'+element))
    imHSV = cv2.cvtColor(imBGR, cv2.COLOR_BGR2HSV)
    cv2.imwrite(directory+"HSV"+element, imHSV)


#segLabels
