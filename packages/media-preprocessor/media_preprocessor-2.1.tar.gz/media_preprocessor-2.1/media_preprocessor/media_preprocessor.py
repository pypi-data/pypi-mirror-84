from os import listdir
from os.path import isfile, join
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import cv2

class preprocessor:
    def nbg_vc(self,shape):
        shape=shape
        cap = cv2.VideoCapture(0)
        fgbg= cv2.createBackgroundSubtractorMOG2()


        while(1):

            _, frame = cap.read()

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = fgbg.apply(img)
            img = cv2.resize(img,(shape,shape))
            img = cv2.Canny(img,150,200)
            img = img.reshape(1,shape*shape)
            cv2.imshow('img',img.reshape(shape,shape))
            return img
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        cap.release()

    def img_pre(self,location,shape,edges):
        shape=shape
        temp=[]
        mypath=location
        onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
        temp1 = np.empty(len(onlyfiles), dtype=object)
        for n in range(0, len(onlyfiles)):
            temp1=cv2.imread( join(mypath,onlyfiles[n]),0 )
            temp.append(temp1)
        temp = np.array(temp)
        temp3 = []
        for i in range(0,len(temp)):
            temp2=cv2.resize(temp[i],(shape,shape))
            temp3.append(temp2)
        temp = np.array(temp3)
        temp4=[]
        temp5=[]
        temp6=[]
        if edges==True:
            for i in range(0,len(temp)):
                temp4 = cv2.Canny(temp[i],150,200)
                temp5.append(temp4)
            temp5=np.array(temp5)
            for i in range(0,len(temp)):  
                a=temp5[i].reshape(shape*shape,)
                temp6.append(a)
            temp = np.array(temp6)
        temp = temp.astype('float32')
        temp /= 255.0
        return temp