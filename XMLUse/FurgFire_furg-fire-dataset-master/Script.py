
import cv2
import os 
import xml.etree.ElementTree as ET
import numpy as np 
from xmlCreate import GEN_Annotations
video_path ="/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/furg-fire-dataset-master/house6.mp4"
xml_path ="/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/furg-fire-dataset-master/house6.xml"
# xml_path ="/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/furg-fire-dataset-master/non_fire_patrolbot_onboard.xml"
Create_folder = video_path.split("/")[-1].split(".")[0] # video_name
folder_img = os.path.join(Create_folder,"img") # img_path 
folder_anno = os.path.join(Create_folder,"Anno") # anno_path 
if(os.path.exists(folder_img)==False):
    os.makedirs(folder_img)
    os.makedirs(folder_anno)
print(Create_folder)

# assert(1>2)
target = ET.ElementTree(file=xml_path)
FrameNumList = []
res = np.empty((0, 5))

obj = target.find("frames")
Count = 0
CASH = obj.iter("_")




while True:
    try:
        xFrame = next(CASH)
        if(xFrame.find("frameNumber") is not None):
            FrameNum = xFrame.find("frameNumber").text
            # print(FrameNum)
            yLableBbox = next(CASH)
            
            bndBox = []

            if(yLableBbox.text!=None):
                A = yLableBbox.text.split(" ")
                # print(A)
                x,y,w,h = A[-4:]
                # print(x,y,w,h)
                bndBox.append(x)
                bndBox.append(y)
                bndBox.append(w)
                bndBox.append(h)
                bndBox.append(FrameNum)
                res = np.vstack((res, bndBox))
    except StopIteration:
        
        break
Count=0
innerCount =0
print(res[:,4])
cap = cv2.VideoCapture(video_path)

while(cap.isOpened()): 
    ret, frame = cap.read() 
    if(frame is None):
        break
    if(int(res[:,4][innerCount])==Count):
        h,w,c=frame.shape
        imgSaveName = Create_folder+"_"+str(Count).zfill(4)+".jpg"
        imgSavepath = os.path.join(folder_img,imgSaveName)
        annoSaveName = Create_folder+"_"+str(Count).zfill(4)+".xml"
        annoSavepath = os.path.join(folder_anno,annoSaveName)
        Ptxt = int(res[:,0][innerCount])
        Ptyt = int(res[:,1][innerCount])
        Ptxb = Ptxt+int(res[:,2][innerCount])
        Ptyb = Ptyt+int(res[:,3][innerCount])
        cv2.imwrite(imgSavepath,frame)
        AnnoClass = GEN_Annotations(imgSaveName)
        AnnoClass.set_size(w,h,c)
        xmin=Ptxt+1
        ymin=Ptyt+1
        xmax=Ptxb-1
        ymax=Ptyb-1
        AnnoClass.add_pic_attr("fire",xmin,ymin,xmax,ymax)
        AnnoClass.savefile(annoSavepath)
        cv2.rectangle(frame, (Ptxt, Ptyt), (Ptxb, Ptyb), (255,0,0), 2)
        innerCount=innerCount+1
    
    cv2.imshow('image', frame) 
    Count=Count+1
    k = cv2.waitKey(20) 
 #q键退出
    if (k & 0xff == ord('q')): 
        break
 
cap.release() 
cv2.destroyAllWindows()

# for objIter in CASH:
# cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)

# x1,y1 ------
# |          |
# |          |
# |          |
# --------x2,y2
# sp = img.shape
# sz1 = sp[0]#height(rows) of image
# sz2 = sp[1]#width(colums) of image
# sz3 = sp[2]#the pixels value is made up of three primary colors
#     Count=Count+1
#     if(Count%2==1):
      
#             A = objIter.find("frameNumber")
#             if(A is not None):
                
#                 print(A.text)
#                 nex
#                 bndBox = []
#                 if(objIter.text!=None):
#                     if(objIter.text!=""):
#                 # print(type(objIter.text))
#                         A = objIter.text.split(" ")
#                         # print(type(A[-4:]))
#                         x,y,w,h = A[-4:]
#                         bndBox.append(x)
#                         bndBox.append(y)
#                         bndBox.append(w)
#                         bndBox.append(h)
#                         res = np.vstack((res, bndBox))
    # if(Count%2==0):
    #     bndBox = []
    #     if(objIter.text!=None):
    #         if(objIter.text!=""):
    #             # print(type(objIter.text))
    #             A = objIter.text.split(" ")
    #             # print(type(A[-4:]))
    #             x,y,w,h = A[-4:]
    #             bndBox.append(x)
    #             bndBox.append(y)
    #             bndBox.append(w)
    #             bndBox.append(h)
    #             res = np.vstack((res, bndBox))
# print(len(FrameNumList))


            # print(x)
# obj = list(obj.iter())
# print(obj[1])
# print(obj[2])
# FrameNumIter = obj[1].iter("frameNumber")
# for FrameNum in FrameNumIter:
#     print(FrameNum.text)

# for iterObj in obj:
#     frameNumber = iterObj.find("frameNumber").text
    
#     annotations = iterObj.find("annotations")
#     print(frameNumber)
#     print(annotations)


# a=obj.findall("frameNumber")
# print(a)
# for obj in target.iter("_"):
#     FrameNum = obj.find("frameNumber")
#     print("XS")
#     print(FrameNum)