
from numpy.core.fromnumeric import resize
import cv2
import os 
import xml.etree.ElementTree as ET
import numpy as np 
from lxml import etree, objectify
import random
class DataCopyPasteAugmentSmallObject():

    def __init__(self,ImgFolderPath,AnnoFolderPath,Label_dict,dstFolder):
        self.ImgFolderPath=ImgFolderPath
        self.AnnoFolderPath = AnnoFolderPath
        self.Label_dict= Label_dict
        self.Img = None
        self.dstFolder = dstFolder
        
        self.dstImgFolder = os.path.join(self.dstFolder,"IMG")
        self.dstAnnoFolder = os.path.join(self.dstFolder,"Anno")
        if(os.path.exists(self.dstImgFolder)==False):
            os.makedirs(self.dstImgFolder)
        if(os.path.exists(self.dstAnnoFolder)==False):
            os.makedirs(self.dstAnnoFolder)
    def xmlparse(self,path):
        parser = etree.XMLParser(encoding="utf-8", strip_cdata=False, remove_blank_text=True)
        root = etree.parse(path, parser=parser)
        return root
    def CrossOrNot(self,h,w,res):
        CrossValue = 0  
        # print("AAAA")
        # print(self.Img.shape)
        SH,SW,SC = self.Img.shape
        Bbox_xmin=int(SW*random.uniform(0,0.8))
        Bbox_ymin=int(SH*random.uniform(0,0.8))
        Bbox_xmax=Bbox_xmin+w
        Bbox_ymax=Bbox_ymin+h
        for i in range(res[:,1].shape[0]):
            xmin =int(res[:,0][i])
            ymin = int(res[:,1][i])
            xmax = int(res[:,2][i])
            ymax = int(res[:,3][i])
            # label = int(res[:,4][i])
            if(Bbox_xmin<xmin-15 or Bbox_ymin<ymin-15):
                CrossValue=1
                return CrossValue,Bbox_xmin,Bbox_ymin,Bbox_xmax,Bbox_ymax
            else:
                if(Bbox_xmax>xmax+15 or Bbox_ymax>ymax+15):
                    CrossValue=1
                    return CrossValue,Bbox_xmin,Bbox_ymin,Bbox_xmax,Bbox_ymax
                else:
                    return CrossValue,Bbox_xmin,Bbox_ymin,Bbox_xmax,Bbox_ymax
    def ReadXml(self,filePath):
        target = ET.ElementTree(file=filePath)
        # print(filepath)
        res = np.empty((0, 5))
        for obj in target.iter("object"):
            # print("1")
            name = obj.find("name").text.lower().strip()
            print(name)
            # name = obj.find("name").text
            bbox = obj.find("bndbox")
            pts = ["xmin", "ymin", "xmax", "ymax"]
            bndbox = []
            for i, pt in enumerate(pts):
                cur_pt = int(bbox.find(pt).text) - 1
                # scale height or width
                # cur_pt = cur_pt / width if i % 2 == 0 else cur_pt / height
                bndbox.append(cur_pt)
            label_idx =self.Label_dict[name]
            bndbox.append(label_idx)
            res = np.vstack((res, bndbox))
        return res
    def GetList(self,ImgPath,res):
        self.Img = cv2.imread(ImgPath)
        # print(res)
        ImgMatList = []
        LabelList = []
        for i in range(res[:,1].shape[0]):
            xmin =int(res[:,0][i])
            ymin = int(res[:,1][i])
            xmax = int(res[:,2][i])
            ymax = int(res[:,3][i])
            label = int(res[:,4][i])
            LabelList.append(label)
            Target_Area = self.Img[ymin+1:ymax-1,xmin+1:xmax-1]
            #resize to [10x10]--[20x20] Mat 
            W = int(random.uniform(10,15))
            Ratio = min(ymax-ymin,xmax-xmin)/W
            pic = cv2.resize(Target_Area,None,fx=1/Ratio,fy=1/Ratio,interpolation=cv2.INTER_LINEAR)
            ImgMatList.append(pic)            
        return ImgMatList,LabelList
    def ergodic_path(self):
        imgPathList = os.listdir(self.ImgFolderPath)
        index = 0
        for nameImg in imgPathList:
            index +=1
            if(index ==200):
                return 0
            name = nameImg.split(".")[0]
            imgFile = os.path.join(self.ImgFolderPath,nameImg)
            xmlFile = os.path.join(self.AnnoFolderPath,name+".xml")
            res = self.ReadXml(xmlFile)
            ImgMatList,LabelList = self.GetList(imgFile,res)
            self.Create_ImgCPAug(ImgMatList,LabelList,res,imgFile,xmlFile)
    
    def Create_ImgCPAug(self,ImgMatList,LabelList,res,imgFile,xmlFile):
        Img = cv2.imread(imgFile)
        name = imgFile.split("/")[-1].split(".")[0]
        srcxmlFile = os.path.join(self.AnnoFolderPath,name+".xml")
        if(xmlFile!=srcxmlFile):
            print("there was an error in the ,",xmlFile)
            return 0
        saveImgPath = os.path.join(self.dstImgFolder,name+"aug"+".jpg")
        saveXmlPath = os.path.join(self.dstAnnoFolder,name+"aug"+".xml")
        if(Img is None):
            print("Maybe there was Error",imgFile)
            return 0
        for i in range(len(ImgMatList)):
            h,w,c = ImgMatList[i].shape
            CrossValue,Bbox_xmin,Bbox_ymin,Bbox_xmax,Bbox_ymax=self.CrossOrNot(h,w,res)
            if(CrossValue==1):
                Img[Bbox_ymin:Bbox_ymax,Bbox_xmin:Bbox_xmax]=ImgMatList[i]
#write the img  
                cv2.imwrite(saveImgPath,Img)
                for key in self.Label_dict.keys():
                    if(self.Label_dict[key]==LabelList[i]):
                        label_name=key
                       # this will point to the folder 
                        self.Create_AnnoFile(xmlFile,label_name,Bbox_xmin,Bbox_ymin,Bbox_xmax,Bbox_ymax,saveXmlPath)   
            else:
                print("this crop copy paste has occupy the source img")
                continue
        
    def Create_AnnoFile(self,srcFile,LabelName,xmin,ymin,xmax,ymax,dstXmlPath):    
        root = self.xmlparse(srcFile)
        node = etree.Element('object')
        childnode2=etree.Element("name")
        childnode2.text=str(LabelName)
        childnode3 = etree.Element("bndbox")
        grandchildnode1 = etree.Element("xmin")
        grandchildnode1.text =str(xmin) 
        grandchildnode2 = etree.Element("ymin")
        grandchildnode2.text = str(ymin)
        grandchildnode3 = etree.Element("xmax")
        grandchildnode3.text = str(xmax)
        grandchildnode4 = etree.Element("ymax")
        grandchildnode4.text = str(ymax)
        childnode3.append(grandchildnode1)
        childnode3.append(grandchildnode2)
        childnode3.append(grandchildnode3)
        childnode3.append(grandchildnode4)
        node.append(childnode2)
        node.append(childnode3)
        root.getroot().append(node)
        root.write(dstXmlPath, pretty_print=True, encoding='utf-8')
if __name__=="__main__":
    
    label_dict={"fire":0,"mouse":1}
    annoFolder = "/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/convert/house5/Anno"
    imgFolder = "/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/convert/house5/img"
    dstFolder = "/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/resulthouse5"
    A = DataCopyPasteAugmentSmallObject(imgFolder,annoFolder,label_dict,dstFolder)
    A.ergodic_path()