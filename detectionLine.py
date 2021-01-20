from LEGO_FastControl import LEGO_FastControl
from LEGO_Serial import LEGO_Serial
import numpy as np
import cv2
import time
# np.set_printoptions(threshold='nan')
np.set_printoptions(threshold=np.inf)
def getCenter():
    FastControl = LEGO_FastControl()
    FastSerial = LEGO_Serial()
    cap = cv2.VideoCapture(0)
    center = center2 = 999
    beginTime = 0
    resolution = 200
    while(True):
        # Capture frame-by-frame
        endTime = time.time()
        intervalTime = endTime - beginTime
        print("intervalTime:",intervalTime)
        beginTime = time.time()
        
        ret, frame = cap.read()
        frame = cv2.resize(frame,(resolution,resolution),interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        ret,thresh1 = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
        edges = cv2.Canny(thresh1,100,300,apertureSize = 3)
        a = edges
        [rows, cols] = a.shape
        # print(rows, cols)
        center2 = 999
        
        
        for i in [resolution-10,int(resolution/2)]:
            if i == resolution-10:
                temp1 = a[i][:]
                #print(type(temp1))
                # temp = np.vstack((temp,np.arange(1,513)))
                res1 = np.where(temp1 == 255)[0]
                if res1.size > 1:
                    # print("SS",res1)
                    res_sort = np.argsort(np.abs(res1-resolution/2))
                    # print(res_sort)
                    # print("res1 type is",type(res1))
                    center = (res1[res_sort[0]] + res1[res_sort[1]])/2 - resolution/2
                else:
                    center = 999 
            #print("center is ", center)
            if i == resolution/2:
                temp2 = a[i][:]
                res2 = np.where(temp2 == 255)[0]
                if res2.size > 1:
                    # print("SS",res2)
                    res_sort2 = np.argsort(np.abs(res2-resolution/2))
                    # print(res_sort2)
                    center2 = (res2[res_sort2[0]] + res2[res_sort2[1]])/2 - resolution/2
                else:
                    center2 = 999 
            #print("center2 is ", center2)
        
        
        if center != 999 and center2 != 999:
            start = []
            start.append(int(center+resolution/2))
            start.append(200)
            end = []
            end.append(int(center2+ resolution/2))
            end.append(resolution/2)
            pstart = tuple(start)
            pend = tuple(end)
            #print("start",pstart)
            #print("end",pend)
            
            #cv2.line(thresh1,pstart,pend,(255,155,155),2)
            #cv2.imshow("ff",thresh1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            #cv2.imshow("ff",frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        if center2 != 999:
            wl_output,wr_output = FastControl.control(center,0)
            cv2.putText(thresh1,str(wl_output) + "   " + str(wr_output),(20,100),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,0),2)
            #cv2.line(thresh1,pstart,pend,(255,155,155),2)
            cv2.imshow("ff",thresh1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            FastSerial.go_encoder(-wr_output,wl_output,0,0,0)
            #print("Go finished")
    # return center
#print("begin")
getCenter()
