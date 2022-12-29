import cv2
import sys, signal
import BodyTracking.cv_viewer.tracking_viewer as cv_viewer
from CoordinatePipe import CoordinatePipe
from DataExtractionWrapper import DataExtractionWrapper
from SpoutFrameSender import SpoutFrameSender



def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    dataWrapper.Close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


dataWrapper = DataExtractionWrapper()
pipe = CoordinatePipe()
frameSender = SpoutFrameSender()

while True:
    #Load fresh data from zed
    dataWrapper.LoadDataFromZed()

    posString = dataWrapper.GetDataAsJSONString()
    pipe.Write(str.encode(posString,'utf8'))

    currentFrame = dataWrapper.image.get_data()
    #maskFrame = dataWrapper.ApplyBodyMasksToFrame()
    frameSender.SendFrame(currentFrame)
    
    #Show the frame
    cv2.imshow("ZED | 2D View",currentFrame)

    cv2.waitKey(10)
