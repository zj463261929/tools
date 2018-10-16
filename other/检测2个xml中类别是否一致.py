#coding=utf-8
import os
from os import path
import numpy as np
import  xml.dom.minidom

orig_xml_dir1 = "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations35176/" 
orig_xml_dir2 = "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations/" 
files1 = [x for x in os.listdir(orig_xml_dir1) if path.isfile(orig_xml_dir1+os.sep+x) and x.endswith('.xml')]
files2 = [x for x in os.listdir(orig_xml_dir2) if path.isfile(orig_xml_dir2+os.sep+x) and x.endswith('.xml')]

fw = open("/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/zj.txt",'w+')
fw1 = open("/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/zj1.txt",'w+')
fw2 = open("/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/zj2.txt",'w+')
fw3 = open("/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/zj3.txt",'w+')
'''	
for i in xrange(len(files1)): 
	file1 = files1[i]
	basename = os.path.splitext(file1)[0]
	if file1 in files2:
		fw.write(basename + "\n")
'''
class_name = ["suv", "forklift", "digger", "car", "bus", "tanker", "person", "minitruck", "minibus", "truckbig", "trucksmall", "tricycle", "bicycle"]
trainFile = '/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/ImageSets/Main/train.txt'	

a1 = 0		
with open(trainFile, "r") as f:
	lines = f.readlines()
	for ll in lines:
		basename = ll.strip()
		dom1 = xml.dom.minidom.parse(orig_xml_dir1+basename+".xml") #用于打开一个xml文件，并将这个文件对象dom变量。
		root1 = dom1.documentElement #用于得到dom对象的文档元素，并把获得的对象给root
		
		name_lst1 = []
		lst_temp1 = root1.getElementsByTagName("name")
		for i in range(len(lst_temp1)):
			l1 = lst_temp1[i].firstChild.data 
			if l1 in class_name:
				name_lst1.append(l1)
				
		dom2 = xml.dom.minidom.parse(orig_xml_dir2+basename+".xml") #用于打开一个xml文件，并将这个文件对象dom变量。
		root2 = dom2.documentElement #用于得到dom对象的文档元素，并把获得的对象给root
		
		name_lst2 = []
		lst_temp2 = root2.getElementsByTagName("name")
		for i in range(len(lst_temp2)):
			l2 = lst_temp2[i].firstChild.data 
			if l2 in class_name:
				name_lst2.append(l2)
		
		num1 = []
		for name in class_name:
			n = 0
			for i in range(len(name_lst1)):
				if name == name_lst1[i]:
					n = n + 1
			num1.append(str(n))
		str1 = ''.join(num1)
		
		num2 = []
		for name in class_name:
			n = 0
			for i in range(len(name_lst2)):
				if name == name_lst2[i]:
					n = n + 1
			num2.append(str(n))
		str2 = ''.join(num2)
		
		n11 = int(num1[0]) + int(num1[7])
		n12 = int(num2[0]) + int(num2[7])
		
		if str1==str2:
			fw2.write(basename + "\n")
			continue

		n1 = 0
		n2 = 0
		for i in range(len(class_name)):
			n1 = n1 + int(num1[i])
			n2 = n2 + int(num2[i])
			
		if n1!=n2:
			if n11==n12:
				a1 = a1 + 1
				print n1, n2
				fw1.write(basename + "\n")
				'''fw.write(str(a1) + " " + basename + "\n") 		
				fw.write(' '.join(name_lst1) + "\n")
				fw.write( str1+ "\n")
				fw.write( ' '.join(name_lst2) + "\n")
				fw.write( str2+ "\n")
					
				fw.write( "\n")'''
			else:
				fw3.write(basename + "\n")
				
		'''if str1!=str2:
			if n1==n2:
				#print num1
				#print num2
				#print "\n"
				fw3.write(basename + "\n")
				continue
			if n1!=n2:
				a1 = a1 + 1
				print n1, n2
				fw1.write(basename + "\n")
				fw.write(str(a1) + " " + basename + "\n") 		
				fw.write(' '.join(name_lst1) + "\n")
				fw.write( str1+ "\n")
				fw.write( ' '.join(name_lst2) + "\n")
				fw.write( str2+ "\n")
				
				fw.write( "\n")'''
		