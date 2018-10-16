#coding=utf-8
import os
from os import path
import numpy as np
import  xml.dom.minidom
import shutil

class_name = ["suv", "forklift", "digger", "car", "bus", "tanker", "person", "minitruck", "minibus", "truckbig", "trucksmall", "tricycle", "bicycle"]

orig_xml_dir = "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations/" 
orig_img_dir = "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/JPEGImages/" 
save_xml_dir = "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/xml/" 
save_img_dir = "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/img/" 
if not os.path.exists(save_xml_dir):
	os.mkdir(save_xml_dir)
if not os.path.exists(save_img_dir):
	os.mkdir(save_img_dir)
	
files = [x for x in os.listdir(orig_xml_dir) if path.isfile(orig_xml_dir+os.sep+x) and x.endswith('.xml')]

def get_class_xmlName(singleClassName, singleClassRatio):
	singleClassXmlNameLst = []
	for i in xrange(len(files)): 
		file = files[i]
		basename = os.path.splitext(file)[0]

		dom = xml.dom.minidom.parse(orig_xml_dir+basename+".xml") #用于打开一个xml文件，并将这个文件对象dom变量。
		root = dom.documentElement #用于得到dom对象的文档元素，并把获得的对象给root
		
		name_lst = []
		lst_temp = root.getElementsByTagName("name")
		
		for i in range(len(lst_temp)):
			l1 = lst_temp[i].firstChild.data 
			if l1 in class_name:
				name_lst.append(l1)
		num = 0	
		for i in range(len(name_lst)):
			if singleClassName==name_lst[i]:
				num = num + 1
		
		ratio = round(num/(0.0+len(name_lst)),1)
		if ratio>=round(singleClassRatio,1):
			singleClassXmlNameLst.append(basename)
	
	return singleClassXmlNameLst
	
className = ["bus", "tanker", "minitruck","tricycle"]
classRatio = [0.5,0.5,0.5,0.5]
fw = open("/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/className.txt",'w+')

lst = []
for i in range(min(len(className),len(classRatio))):
	singleClassName = className[i]
	singleClassRatio = classRatio[i]
	singleClassXmlNameLst = get_class_xmlName(singleClassName, singleClassRatio)
	print singleClassName, len(singleClassXmlNameLst)
	
	lst = lst + singleClassXmlNameLst
	
print len(lst)	
lst = list(set(lst))
print len(lst)

for i in range(len(lst)):
	basename = lst[i]
	#print basename
	fw.write( basename + "\n")
	#shutil.copy(orig_xml_dir+basename+".xml" , save_xml_dir+basename+".xml" )
	#shutil.copy(orig_img_dir+basename+".jpg" , save_img_dir+basename+".jpg" )
fw.close()	