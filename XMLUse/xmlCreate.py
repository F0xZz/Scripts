# from lxml.etree import Element, SubElement, tostring
# import pprint
# from xml.dom.minidom import parseString

# node_root = Element('annotation')

# node_folder = SubElement(node_root, 'folder')
# node_folder.text = 'GTSDB'

# node_filename = SubElement(node_root, 'filename')
# node_filename.text = '000001.jpg'

# node_size = SubElement(node_root, 'size')
# node_width = SubElement(node_size, 'width')
# node_width.text = '500'

# node_height = SubElement(node_size, 'height')
# node_height.text = '375'

# node_depth = SubElement(node_size, 'depth')
# node_depth.text = '3'

# node_object = SubElement(node_root, 'object')
# node_name = SubElement(node_object, 'name')
# node_name.text = 'mouse'
# node_difficult = SubElement(node_object, 'difficult')
# node_difficult.text = '0'
# node_bndbox = SubElement(node_object, 'bndbox')
# node_xmin = SubElement(node_bndbox, 'xmin')
# node_xmin.text = '99'
# node_ymin = SubElement(node_bndbox, 'ymin')
# node_ymin.text = '358'
# node_xmax = SubElement(node_bndbox, 'xmax')
# node_xmax.text = '135'
# node_ymax = SubElement(node_bndbox, 'ymax')
# node_ymax.text = '375'

# # xml = tostring(node_root, pretty_print=True)  #格式化显示，该换行的换行
# # dom = parseString(xml)
# filename = "demo.xml"
# node_root.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')
# # print (xml)
from lxml import etree
import xml.etree.ElementTree as ET
class GEN_Annotations:
    def __init__(self, filename):
        self.root = etree.Element("annotation")

        child1 = etree.SubElement(self.root, "folder")
        child1.text = "VOC2007"
 
        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename
 
        child3 = etree.SubElement(self.root, "source")
 
        child4 = etree.SubElement(child3, "annotation")
        child4.text = "PASCAL VOC2007"
        child5 = etree.SubElement(child3, "database")
        child5.text = "Unknown"
 
        child6 = etree.SubElement(child3, "image")
        child6.text = "flickr"
        child7 = etree.SubElement(child3, "flickrid")
        child7.text = "35435"
        print( type(self.root))
        print(type(child3))
 
    def set_size(self,witdh,height,channel):
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(witdh)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "depth")
        channeln.text = str(channel)
    def savefile(self,filename):
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')
    def add_pic_attr(self,label,xmin,ymin,xmax,ymax):
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        namen.text = label
        bndbox = etree.SubElement(object, "bndbox")
        xminn = etree.SubElement(bndbox, "xmin")
        xminn.text = str(xmin)
        yminn = etree.SubElement(bndbox, "ymin")
        yminn.text = str(ymin)
        xmaxn = etree.SubElement(bndbox, "xmax")
        xmaxn.text = str(xmax)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(ymax)
    
 
if __name__ == '__main__':
    filename="000001.jpg"
    anno= GEN_Annotations(filename)
    anno.set_size(1280,720,3)
    for i in range(2):
        xmin=i+1
        ymin=i+10
        xmax=i+100
        ymax=i+100
        anno.add_pic_attr("mouse",xmin+1,ymin,xmax,ymax)
    anno.savefile("101.xml")
   