import cv2
import numpy as np
import os 
import shutil
import re
class script(object):
    def __init__(self,label_file_path,frame_file_path,Cam_ID,Ser_ID):
        self.label_file_path=label_file_path
        self.frame_file_path = frame_file_path
        self.Cam_Num = Cam_ID
        self.ser_Num = Ser_ID
        frameid,classid,pid,bbox,diclist = self.pre_label(self.label_file_path)
        self.re_crop_img(self.frame_file_path,diclist)
        return None
    def crop_img (self,pid,cameraid,serid,frame_file,frameid,bbox,ser_ID,Cam_ID): # crop the image set in the same folder
    # n = 0
    # for i in range(len(bboxs)):
            # bbox = bboxs[i]
        # print(type(bbox[0]))   
        x1 = int(bbox[0])
        y1 = int(bbox[1])
        w = int(bbox[2])
        h = int(bbox[3])
        x2 = x1 + w
        y2 = y1 + h
            # n= n+1
        # print(n)
        # sourceimg = cv2.imread(os.path.join(frame_file,frameid[i]+".jpg"))
        # print(sourceimg.shape)
        afcrop_img = frame_file[y1:y2, x1:x2]
        pid = int(pid)+0
        cameraid = int(cameraid)
        namepath = str(pid)+"_"+"c"+str(cameraid)+"s"+str(ser_Num)+"_"+str(frameid)+"_"+"00"+".jpg"
        # crop_save_path = os.path.join(os.getcwd(),"cropimage",str(cameraid),str(serid),str(pid))
        crop_save_path = os.path.join(os.getcwd(),"cropimage",str(Cam_ID),str(ser_ID),str(pid))
        if(int(frameid)%500 == 0):
            print(crop_save_path)
        if not os.path.exists(crop_save_path):
            os.makedirs(crop_save_path)
        crop_save_in_folder = os.path.join(crop_save_path,namepath)
        cv2.imwrite(crop_save_in_folder,afcrop_img)
        # if (i - 20 == 0 ):
        #     print("is running")
        #     print(crop_save_path)
            # break
        return 0
        #this function use to select the xywh and don't out the boundary
    def xywh (self,bbox,width,height):
        box = []

        # print(bbox)
        x = bbox[0]
        y = bbox[1]
        w = bbox[2]
        h = bbox[3]
        x = int(max(int(x),1))
        y = int(max(int(y),1))
        if int(x+int(w))>int(width):
            # print("is out the boundary of the image")
            # print(x,w)
            w = int(width-x-1)
            # print("is refresh")
            # print(x,w)
        if int(y+int(h))>height:
            # print("is out the boundary of the image")
            # print(y,h)
            h = int(height - y -1)
            # print("is refresh")
            # print(y,h)
        box.append(x)
        box.append(y)
        box.append(w)
        box.append(h)
        return box
    def pre_label(self,label_file_path):
        diclist = []
        frameid = []  # ['1005', 'person', '7', '270', '408', '101', '139']
        # dic ={}
        classid = [] 
        pid = []
        bbox = []
        with open(self.label_file_path) as f :
            label_lines=f.readlines()
            for lines in label_lines:
                dic = {}
                lines = lines.replace('\n','')
                sepmark = lines.split(',')
                frameid.append(sepmark[0])
                classid.append(sepmark[1])
                pid.append(sepmark[2])
                bbox.append((sepmark[3],sepmark[4],sepmark[5],sepmark[6]))
                dic["frameid"] = str(sepmark[0])
                dic["classid"] = sepmark[1]
                dic["pid"] = sepmark[2]
                dic["bbox"] = [sepmark[3],sepmark[4],sepmark[5],sepmark[6]]
                diclist.append(dic)
        return frameid,classid,pid,bbox,diclist
    def re_crop_img(self,frame_file_path,diclist):
        r=0
        for j in range(len(diclist)):
            r = r+1
            if r % 100==0:
                print(Cam_ID)
            frameid = diclist[j].get("frameid")    
            pid = diclist[j].get("pid")
            pid = pid.zfill(4)
            bbox = diclist[j].get("bbox")
            # 43.30-554-20210224-112922 
            # print(os.path.join(frame_file_path,frameid))
            frame_folder = frame_file_path.split("/")[-1]
            pattern = re.compile(r"\d{2}.\d{2}") 
            pattern2 = re.compile(r"\d{8}-\d*")
            ser_ID =pattern2.search(frame_folder).group()
            Cam_ID =pattern.search(frame_folder).group()
            frame = cv2.imread(os.path.join(frame_file_path,frameid))
            h,w = frame.shape[:2]
            bbox = self.xywh(bbox,w,h)    
            i = str(int(frameid.split(".")[0])-1000)
            self.crop_img(pid,str(self.Cam_Num),str(self.ser_Num),frame,str(i),bbox,ser_ID,Cam_ID)


if __name__=="__main__":
    label_root = "./ml" # this you should set the root of the label file
    
    label_list = os.listdir(label_root)
    frame_set = "/home/ubuntu/3060code/torchcode/yolo_deepsort"
    # tool = script()
    #this is set the label frame
    # "/home/ubuntu/Downloads/camera/newname/43.30-554-20210224-112922"
    Cam_ID_list =[]
    Cam_Num = 0
    ser_ID_list = []
    ser_Num = 0
    # print(label_list)    
    
    for label_name in label_list:
        
        frame_folder = label_name.split(".txt")[0]
        pattern = re.compile(r"\d{2}.\d{2}") 
        pattern2 = re.compile(r"\d{8}-\d*")
        Cam_ID =pattern.search(frame_folder).group()
        
        print(Cam_ID_list)
        print(Cam_ID)
        if Cam_ID not in Cam_ID_list:
            # print()
            Cam_Num  = Cam_Num + 1
        ser_ID =pattern2.search(frame_folder).group()
        if ser_ID not in ser_ID_list:
            ser_Num = ser_Num+1

        print(Cam_Num)
        print(ser_Num)
        Cam_ID_list.append(Cam_ID)
        ser_ID_list.append(ser_ID)
        frame_path = os.path.join(frame_set,frame_folder)
        label_path = os.path.join(label_root,label_name)
        tool = script(label_path,frame_path,Cam_Num,ser_Num)
        # frameid,classid,pid,bbox,diclist= tool.pre_label(label_path)
        # print(frameid,classid,pid,bbox,diclist)
