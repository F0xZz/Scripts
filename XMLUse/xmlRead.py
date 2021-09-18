import cv2
import os
import xml.etree.cElementTree as ET 
def Read_xml(filepath):
    xml_list = []
    list_name = os.listdir(filepath)
    for name in list_name:
        xml_path = os.path.join(filepath,name)
        xml_list.append(xml_path)
    return xml_list
def Read_annotation(xmllist):
    tree = ET.parse(xmllist)
    root = tree.getroot() 
    for child in root: 
        # print (child.tag, "---", child.attrib )
        # print(child.text)
        if(child.tag=="path"):
            # print(child.text)
            imgfiltpath = child.text.split("\\")[-1]
            imgfiltpath = os.path.join(folderPath,imgfiltpath)
            img= cv2.imread(imgfiltpath)
        if(child.tag=="object"):
            # print(child.text)
            ob = child
            rank = ob.find('name').text
            if rank =="fire":
                bbox = ob.find("bndbox")
                boxminx = int(bbox.find("xmin").text)
                boxminy =  int(bbox.find("ymin").text)
                boxmaxx = int(bbox.find("xmax").text)
                boxmaxy= int(bbox.find("ymax").text)
    return imgfiltpath,boxminx,boxminy,boxmaxx,boxmaxy
def Swtich_arg(a,b):
    if(a>b):
        return b,a
    if(a<b):
        return a,b    
if __name__=="__main__":
    folderPath = "./JPEGImages"
    annotationPath  = "./Annotations"
    xml_list =  Read_xml(annotationPath)
    for i in range(len(xml_list)):
        imgfiltpath,boxminx,boxminy,boxmaxx,boxmaxy=Read_annotation(xml_list[i])
        img = cv2.imread(imgfiltpath)
        boxminx,boxmaxx=Swtich_arg(boxminx,boxmaxx)
        boxminy,boxmaxy=Swtich_arg(boxminy,boxmaxy)
        print(imgfiltpath,boxminx,boxmaxx,boxminy,boxmaxy)
        if img is None:
            print("the file path is Wrong",imgfiltpath)
            continue
        imgCrop = img[boxminy:boxmaxy,boxminx:boxmaxx]
        folder = "./firevoc"
        if (os.path.exists(folder))==False:
            os.makedirs(folder)
        savepath = os.path.join(folder,imgfiltpath.split("/")[-1])
        cv2.imwrite(savepath,imgCrop)
   