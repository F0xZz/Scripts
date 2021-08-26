
from numpy.core.fromnumeric import resize
import cv2
import os 
import xml.etree.ElementTree as ET
import numpy as np 
from lxml import etree, objectify
import random
import re
def xmlparse(path):
    parser = etree.XMLParser(encoding="utf-8", strip_cdata=False, remove_blank_text=True)
    root = etree.parse(path, parser=parser)
    return root
def ADDVOCKey(srcFile,dstFodler):
    root = xmlparse(srcFile)
    node = etree.Element('object')
    
    for obj in root.iter("object"):
        
        childnode2=etree.Element("pose")
        childnode2.text="Unspecified"
        childnode3=etree.Element("truncated")
        childnode3.text="0"
        childnode4=etree.Element("difficult")
        childnode4.text="0"
        obj.append(childnode2)
        obj.append(childnode3)
        obj.append(childnode4)
    root.write(dstFodler, pretty_print=True, encoding='utf-8')
srcFile = "/home/ubuntu/20210701-/newfiredata/FurgFire_furg-fire-dataset-master/resultAug/Test/XML"
dstFile = "newtestXML"
if (os.path.exists(dstFile)==False):
    os.makedirs(dstFile)
nameList = os.listdir(srcFile)
count = 0
for i in nameList:
    name = i.split(".")[0]
    pattern = re.compile("VOC\w+\d+")
    matchValue = pattern.match(name)
    srcXMLFile = os.path.join(srcFile,i)
    dstXMLFile = os.path.join(dstFile,i)
    if(matchValue is None):
        print(name)
        ADDVOCKey(srcXMLFile,dstXMLFile)
    if(matchValue is not None):
        count+=1
print(count)


