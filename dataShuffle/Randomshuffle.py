import cv2
import os 
import shutil
imgFolderPath = "/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/resultAug/resulthouse2/IMG"
xmlFolderPath = "/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/resultAug/resulthouse2/Anno"
dstFolder = "./Train"
dstImgFolder = os.path.join(dstFolder,"IMG")
dstXMLFolder = os.path.join(dstFolder,"XML")
if(os.path.exists(dstImgFolder)==False):
    os.makedirs(dstImgFolder)
    os.makedirs(dstXMLFolder)
dstTestFolder = "./Test"
dstImgTestFolder = os.path.join(dstTestFolder,"IMG")
dstXMLTestFolder = os.path.join(dstTestFolder,"XML")
if(os.path.exists(dstXMLTestFolder)==False):
    os.makedirs(dstImgTestFolder)
    os.makedirs(dstXMLTestFolder)
imgList = os.listdir(imgFolderPath)
ratio = 0.8
lenIMG = len(imgList)
index = 1
for name in imgList:
    srcImg = os.path.join(imgFolderPath,name)
    nameFile = name.split("/")[-1].split(".")[0]
    srcXML = os.path.join(xmlFolderPath,nameFile+".xml")
    if(os.path.exists(srcXML)==False):
        continue
    if(index<ratio*lenIMG):
        newFireSave = os.path.join(dstImgFolder,nameFile+".jpg")
        newXMLSave = os.path.join(dstXMLFolder,nameFile+".xml")
        shutil.copy(srcImg,newFireSave)
        shutil.copy(srcXML,newXMLSave)
    else:
        newFireSave = os.path.join(dstImgTestFolder,nameFile+".jpg")
        newXMLSave = os.path.join(dstXMLTestFolder,nameFile+".xml")
        shutil.copy(srcImg,newFireSave)
        shutil.copy(srcXML,newXMLSave)
    index+=1