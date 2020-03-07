from walabot import Walabot 
import time
import json
import collections
from multiprocessing import Process,Value
import cv2
class Getmap:
    def __init__(self):
        self.w=Walabot()
        self.w.ARENA=[(100, 500, 10), (-45, 45, 3), (-45, 45, 3)]
        self.RF_array=collections.OrderedDict()
        self.cap = cv2.VideoCapture(1)
    def work(self,map_num,mapfile,photofile):
        self.w.isConnectedAny()
        self.w.simpleInit()  
        for i in range(map_num):
            rawImage=self.w.triggerAndGetRawImage()               
            self.RF_array['{:.2f}'.format(time.time())]=rawImage
            ret, frame = self.cap.read()
            cv2.imshow('frame', frame)
            cv2.imwrite(photofile+'/{:.2f}.jpg'.format(time.time()), frame)
            cv2.waitKey(1)
        self.w.disConnected()
        self.cap.release()
        cv2.destroyAllWindows()
        with open(mapfile+'\rawImage.txt', 'w') as f:
            json.dump(self.RF_array, f)


if __name__=='__main__':
    w=Getmap()
    w.work()
        