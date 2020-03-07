from walabot import Walabot
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import json
import collections
from multiprocessing import Process
import os
import seaborn as sns
"""输出热图"""
def getmap(param,rawImage):#获取垂直和水平热图
    theta,phi,R=rawImage.shape
    H=np.zeros((phi,R))
    V=np.zeros((theta,R))
    for i in range(phi):
        for j in range(theta):
            for k in range(R):
                """计算点在垂直平面的映射位置：theta不变，r=cos(phi)"""
                pv=math.radians(param[1][2]*i-45)
                rv=100+10*k
                rnv=rv*math.cos(pv)
                r_indx_v=round((rnv-100)/10)#计算索引

                """计算点在水平平面的映射位置：phi不变，r=cos(theta)"""
                ph = math.radians(param[2][2] * j - 45)
                rh = 100 + 10 * k
                rnh = rh * math.cos(ph)
                r_indx_h = round((rnh - 100) / 10)
                try:
                    V[j][r_indx_v]+=rawImage[j][i][k]#j为点在theta维度上的索引，r_indx_v为经过映射后点应当的R维度上的索引
                    H[i][r_indx_h] += rawImage[j][i][k]#i为点在phi维度上的索引，r_indx_h为经过映射后点应当的R维度上的索引
                except:
                    pass
    V=np.rot90(V,2)#逆时针旋转180度
    H=np.rot90(H,1)#逆时针旋转90度
    return H,V


def out_picture(array,path,model):
    for key, value in array.items():
        img = plt.imshow(value)
        img.set_cmap('coolwarm')
        plt.axis('off')
        plt.savefig(path+'\\'+model+'\{}.jpg'.format(key))

def one_json2picture(path,start,end):
    param = [(100, 500, 10), (-45, 45, 3), (-45, 45, 3)]
    for i in range(start,end+1):
        path = path+'\\{}'.format(i)
        with open(path+'\heatmap2.txt', 'r') as load_f:
            rawImage = json.load(load_f,object_pairs_hook=collections.OrderedDict)
        H_array = collections.OrderedDict()
        V_array=collections.OrderedDict()
        for key,value in rawImage.items():
            value=np.array(value)
            H,V=getmap(param, value)
            H_array[key]=  H
            V_array[key] = V

        os.mkdir(path+'\H_b2')
        os.mkdir(path+'\V_b2')
        P1 = Process(target=out_picture, args=(H_array, path,'H_b2'))
        P2 = Process(target=out_picture, args=(V_array, path,'V_b2'))
        P1.start()
        P2.start()
        P1.join()
        P2.join()



if __name__ == '__main__':
    one_json2picture('E:\AAAA\walabot\data\\2019_12_05',3,3)

