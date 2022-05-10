import cv2
import time
import numpy as np
cap = cv2.VideoCapture(0)

SHEET = 'sheet'
MARKER = 'marker'

DEBUG = False
run_in_idle = False

def check_crossing( img, mode='sheet', thresh=35, thresh_defect=1000):
    if mode == 'sheet':
        if img.mean() > thresh:
            return True
        return False
    
    elif mode == 'marker':
        if img.mean() > thresh:

            _,mask = cv2.threshold( img, 150, 255, cv2.THRESH_BINARY)
            mask = cv2.erode( mask, np.ones((3,3)), iterations=3)
            mask = cv2.dilate( mask, np.ones((3,3)), iterations=5)

            if DEBUG:
                cv2.imshow('mask', cv2.resize(mask, None, fx=0.5, fy=0.5))
                #cv2.waitKey(0)

            cnts,_ = cv2.findContours( mask , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts)==0:
                return False
            areas = list( map( cv2.contourArea, cnts))
            areas = np.array( areas )
            if areas.max() > thresh_defect:
                if DEBUG:
                    print('max:',areas.max())
                return True
            else:
                return False
        else:
            return False
            
    


if __name__ == '__main__':
    DEBUG = True
    import os
    #path = 'imgs/Sheet defect Marker'
    path = 'imgs/Sheet defect Marker'
    for file in os.listdir( path ):
        print(file)
        if file[-4:] not in ['.bmp', '.jpg']:
            continue
        img = cv2.imread( os.path.join(path, file ),0)
        state = check_crossing(img,mode = MARKER)
        print(state)
        cv2.imshow('img', cv2.resize(img, None , fx=0.4, fy=0.4))
        cv2.waitKey(0)
        

    


    
