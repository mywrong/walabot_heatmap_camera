#!/usr/bin/python3
#-*- coding=utf-8 -*-
import WalabotAPI as wlbt
import numpy as np

class Walabot:
    """ 控制walabot使用API
    """

    def __init__(self):
        """ 初始化Walabot API.
        """
        #             R             Phi          Theta
        self.ARENA = [(100, 400, 3), (-60, 60, 1.2), (-30, 30, 10)]
        self.Threshold = 10
        self.filterModel = True
        self.wlbt = wlbt
        self.filter = self.wlbt.FILTER_TYPE_MTI if self.filterModel else self.wlbt.FILTER_TYPE_NONE
        self.wlbt.Init()
        self.wlbt.SetSettingsFolder()

    def isConnectedAny(self):
        """ 尝试连接Walabot设备,相应地返回真/假。
        """
        try:
            self.wlbt.ConnectAny()
        except self.wlbt.WalabotError as err:
            if err.code == 19:  # "WALABOT_INSTRUMENT_NOT_FOUND"
                return False
            else:
                raise err
        return True

    def isConnected(self,UUID):
        """ 尝试连接Walabot设备,相应地返回真/假。
        """
        try:
            self.wlbt.Connect(UUID)
        except self.wlbt.WalabotError as err:
            if err.code == 19:  # "WALABOT_INSTRUMENT_NOT_FOUND"
                return False
            else:
                raise err
        return True

    def setParams(self, r, phi,theta, threshold, mti):
        """ 设置天线参数
        """
        self.wlbt.SetProfile(self.wlbt.PROF_SENSOR)
        self.wlbt.SetArenaR(*r)
        self.wlbt.SetArenaTheta(*theta)
        self.wlbt.SetArenaPhi(*phi)
        self.wlbt.SetThreshold(threshold)
        self.wlbt.SetDynamicImageFilter(mti)
        self.wlbt.Start()

    def simpleInit(self):
        self.wlbt.SetProfile(self.wlbt.PROF_SENSOR)
        self.setParams(self.ARENA[0],self.ARENA[1],self.ARENA[2],
                       self.Threshold,self.filter)
        self.calibrate()

    def getArenaParams(self):
        """ Returns the Walabot parameters from the Walabot SDK.
            Returns:
                params      rParams, thetaParams, phiParams, threshold as
                            given from the Walabot SDK.
        """
        rParams = self.wlbt.GetArenaR()
        thetaParams = self.wlbt.GetArenaTheta()
        phiParams = self.wlbt.GetArenaPhi()
        threshold = self.wlbt.GetThreshold()
        return rParams, thetaParams, phiParams, threshold

    def calibrate(self):
        """ 校准 Walabot.
        """
        self.wlbt.StartCalibration()
        while self.wlbt.GetStatus()[0] == self.wlbt.STATUS_CALIBRATING:
            self.wlbt.Trigger()

    def getRawImageSliceDimensions(self):
        """ Returns the dimensions of the rawImage 2D list given from the
            Walabot SDK.
            Returns:
                lenOfPhi    Num of cells in Phi axis.
                lenOfR      Num of cells in Theta axis.
        """
        return self.wlbt.GetRawImageSlice()[1:3]

    def triggerAndGetRawImageSlice(self,model):
        """ Returns the rawImage given from the Walabot SDK.
            Returns:
                rawImage    A rawImage list as described in the Walabot docs.
        """
        self.wlbt.Trigger()
        rawImage = self.wlbt.GetRawImageSlice()[0]
        rawImage = np.array(rawImage)
        if model == '15':
            rawImage = np.rot90(np.rot90(np.rot90(rawImage)))
            rawImage = np.flip(rawImage)
            rawImage = np.flip(rawImage, 1)
        else:
            rawImage = np.flip(rawImage)
        return rawImage

    def triggerAndGetRawImage(self):
        self.wlbt.Trigger()
        rawImage = self.wlbt.GetRawImage()[0]
        return rawImage

    def getFps(self):
        """ Returns the Walabot current fps as given from the Walabot SDK.
            Returns:
                fpsVar      Number of frames per seconds.
        """
        return int(self.wlbt.GetAdvancedParameter('FrameRate'))

    def getUUID(self):
        """ Returns the Walabot UUID  as given from the Walabot SDK.
            Returns:
                horizontalWalabotUUID, verticalWalabotUUID
        """
        uuidList = self.wlbt.GetInstrumentsList()
        print(uuidList)
        wl_V, wl_H, w1_V_m, w1_H_m =str(uuidList[0:2], encoding='utf-8'), str(uuidList[14:16], encoding='utf-8'),\
               str(uuidList[11:13], encoding='utf-8'),str(uuidList[25:27], encoding='utf-8')
        print(wl_V, wl_H, w1_V_m, w1_H_m)
        return wl_V, wl_H, w1_V_m, w1_H_m

    def disConnected(self):
        self.wlbt.Stop()
        self.wlbt.Disconnect()
    def getAntennaPairs(self):
        return self.wlbt.GetAntennaPairs()
if __name__ == '__main__':
    # Select scan arena
    #             R             Phi          Theta
    # ARENA = [(1, 450, 2), (-90, 90, 2), (-15, 15, 5)]
    # Threshold, MTImodel = 10, False
    test = Walabot()
    wl_v,wl_h = test.getUUID()
    print(wl_v,wl_h)
    test.isConnected(wl_h)
    test.simpleInit()
    now = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    rawImage = test.triggerAndGetRawImageSlice()
    img = np.array(rawImage)
    plt.imshow(img, cmap=plt.cm.hot, interpolation='nearest', extent=[-90, 90, 200, 0])
    plt.savefig('D:\Project\walabot\Learning\Data\{}:{}.jpg'.format(wl_h,now))

    test.disConnected()