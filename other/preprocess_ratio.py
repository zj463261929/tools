#coding=utf-8
'''
脚本功能：将图片的大小按照宽高比=1920/1080进行处理，同时处理图片中目标的box.
'''

import os
import numpy as np
import cv2
import random
import xml.dom.minidom
from xml.dom.minidom import Document

class_name = ["handsup", "like", "hate", "sleep"] #类别名称, 	改

width = 1920 #2880	#改
height = 1080 #1620	#改

fw = open("/opt/zhangjing/caffe/data/actions_new/benchmark_ratio_new.txt",'w+')	#改  1620=1080*1.5 (原因是benchmark的占空比范围比训练集的大)
org_image_dir = "/opt/zhangjing/caffe/data/actions_new/benchmark/pictures"	#改
org_xml_dir = "/opt/zhangjing/caffe/data/actions_new/benchmark/labels"	#改
save_image_dir = "/opt/zhangjing/caffe/data/actions_new/benchmark/pictures_ratio_new" #改
save_xml_dir = "/opt/zhangjing/caffe/data/actions_new/benchmark/labels_ratio_new" #改

if not os.path.exists(save_image_dir):
	os.makedirs(save_image_dir)
	
if not os.path.exists(save_xml_dir):
	os.makedirs(save_xml_dir)

files = [x for x in os.listdir(org_image_dir) if os.path.isfile(org_image_dir+os.sep+x) and x.endswith('.jpg')]
#random.shuffle(files)

for i in xrange(len(files)): 
	file=files[i] #"01240001.jpg" #
	print file	   
	
	#扩充图片大小
	image_path = org_image_dir + "/" + file
	if not os.path.exists(image_path):
		continue
	
	img = cv2.imread(image_path)
	if img is None:	
		continue

	h = img.shape[0]
	w = img.shape[1]
	if h>height or w>width:
		continue
		
	channels = 3
	if 2==len(img.shape):
		channels = 1
		
	h_new = h
	w_new = w

	#按照w、h小的来缩放
	'''
	if w>h:
		w_new = width*h/height
	else:
		h_new = height*w/width'''
		
	if w<h:
		w_new = width*h/height
	else:
		h_new = height*w/width
		
	img_new = cv2.resize(img, (w_new, h_new))
	#cv2.rectangle(img_new, (xmin_new,ymin_new), (xmax_new,ymax_new), (0, 0, 255))
	cv2.imwrite(save_image_dir + "/" + file, img_new)
	#cv2.imwrite("/opt/zhangjing/caffe/data/actions_new/benchmark/1.jpg", img_new)
	
	#写txt
	basename = os.path.splitext(file)[0]
	result = 'benchmark/pictures_ratio_new'+os.sep+file+' '+ 'benchmark/labels_ratio_new'+os.sep+basename+'.xml\n'
	fw.write(result)
	
	#xml 处理box
	xml_path = org_xml_dir + "/" + file[:len(file)-4] + ".xml"
	print xml_path
	
	if not os.path.exists( xml_path ):
		continue
	dom = xml.dom.minidom.parse( xml_path ) #用于打开一个xml文件，并将这个文件对象dom变量。
												
	root = dom.documentElement #用于得到dom对象的文档元素，并把获得的对象给root
	
	name_lst = []
	lst_temp = root.getElementsByTagName("name")
	for i in range(len(lst_temp)):
		l = lst_temp[i].firstChild.data 
		if l in class_name:
			name_lst.append(l)	
					
	xmin_lst1 = root.getElementsByTagName("xmin")
	ymin_lst1 = root.getElementsByTagName("ymin")
	xmax_lst1 = root.getElementsByTagName("xmax")
	ymax_lst1 = root.getElementsByTagName("ymax")
	num = min(len(xmin_lst1), len(name_lst))
	xmin_lst = []
	xmax_lst = []
	ymin_lst = []
	ymax_lst = []
	for i in range(num):
		xmin = int(xmin_lst1[i].firstChild.data)
		xmax = int(xmax_lst1[i].firstChild.data)
		ymin = int(ymin_lst1[i].firstChild.data)
		ymax = int(ymax_lst1[i].firstChild.data)
	
		#print type(xmin_lst1[i].firstChild.data) #<type 'unicode'>
		xmin_new = xmin
		xmax_new = xmax
		ymin_new = ymin
		ymax_new = ymax
	
		ymin_new = ymin*h_new/h
		ymax_new = ymax*h_new/h
		xmin_new = xmin*w_new/w
		xmax_new = xmax*w_new/w
	
		xmin_lst.append(xmin_new)
		xmax_lst.append(xmax_new)
		ymin_lst.append(ymin_new)
		ymax_lst.append(ymax_new)
		#cv2.rectangle(img_new, (xmin_new,ymin_new), (xmax_new,ymax_new), (0, 0, 255))
		#cv2.imwrite("/opt/zhangjing/caffe/data/actions_new/benchmark/1.jpg", img_new)
		#cv2.imwrite(save_image_dir + "/" + file, img_new)
		
	#重写xml
	
	# 创建dom文档
	doc = Document()
	# 创建根节点
	orderlist = doc.createElement('annotation')
	# 根节点插入dom树
	doc.appendChild(orderlist)
	
	# 每一组信息先创建节点<folder>，然后插入到父节点<orderlist>下
	folder = doc.createElement('folder')
	orderlist.appendChild(folder)
	# 创建<folder>下的文本节点
	folder_text = doc.createTextNode("VOC2007")
	# 将文本节点插入到<folder>下
	folder.appendChild(folder_text)
	
	filename = doc.createElement('filename')
	orderlist.appendChild(filename)
	filename_text = doc.createTextNode(file)
	filename.appendChild(filename_text)
	
	#############
	source = doc.createElement('source')
	orderlist.appendChild(source)
	database = doc.createElement('database')
	source.appendChild(database)
	database_text = doc.createTextNode("The GDS Database")
	database.appendChild(database_text)
	
	annotation = doc.createElement('annotation')
	source.appendChild(annotation)
	annotation_text = doc.createTextNode("PASCAL VOC2007")
	annotation.appendChild(annotation_text)
	
	image = doc.createElement('image')
	source.appendChild(image)
	image_text = doc.createTextNode("flickr")
	image.appendChild(image_text)
	
	flickrid = doc.createElement('flickrid')
	source.appendChild(flickrid)
	flickrid_text = doc.createTextNode("12345678")
	flickrid.appendChild(flickrid_text)
	
	########
	owner = doc.createElement('owner')
	orderlist.appendChild(owner)
	flickrid = doc.createElement('flickrid')
	owner.appendChild(flickrid)
	flickrid_text = doc.createTextNode("12345678")
	flickrid.appendChild(flickrid_text)
	
	name = doc.createElement('name')
	owner.appendChild(name)
	name_text = doc.createTextNode("GDS")
	name.appendChild(name_text)
	
	#########
	size = doc.createElement('size')
	orderlist.appendChild(size)
	width1 = doc.createElement('width')
	size.appendChild(width1)
	width_text = doc.createTextNode(str(w_new))
	width1.appendChild(width_text)
	
	height1 = doc.createElement('height')
	size.appendChild(height1)
	height_text = doc.createTextNode(str(h_new))
	height1.appendChild(height_text)
	
	depth = doc.createElement('depth')
	size.appendChild(depth)
	depth_text = doc.createTextNode(str(channels))
	depth.appendChild(depth_text)
	
	######
	segmented = doc.createElement('segmented')
	orderlist.appendChild(segmented)
	
	#######
	for i in range(num):
		object = doc.createElement('object')
		orderlist.appendChild(object)
		name = doc.createElement('name')
		object.appendChild(name)
		name_text = doc.createTextNode(name_lst[i])
		name.appendChild(name_text)
		
		pose = doc.createElement('pose')
		object.appendChild(pose)
		pose_text = doc.createTextNode("Unspecified")
		pose.appendChild(pose_text)
		
		truncated = doc.createElement('truncated')
		object.appendChild(truncated)
		truncated_text = doc.createTextNode("0")
		truncated.appendChild(truncated_text)
		
		difficult = doc.createElement('difficult')
		object.appendChild(difficult)
		difficult_text = doc.createTextNode("0")
		difficult.appendChild(difficult_text)
		
		#########
		bndbox = doc.createElement('bndbox')
		object.appendChild(bndbox)
		xmin = doc.createElement('xmin')
		bndbox.appendChild(xmin)
		xmin_text = doc.createTextNode(str(xmin_lst[i]))
		xmin.appendChild(xmin_text)
		
		ymin = doc.createElement('ymin')
		bndbox.appendChild(ymin)
		ymin_text = doc.createTextNode(str(ymin_lst[i]))
		ymin.appendChild(ymin_text)
		
		xmax = doc.createElement('xmax')
		bndbox.appendChild(xmax)
		xmax_text = doc.createTextNode(str(xmax_lst[i]))
		xmax.appendChild(xmax_text)
		
		ymax = doc.createElement('ymax')
		bndbox.appendChild(ymax)
		ymax_text = doc.createTextNode(str(ymax_lst[i]))
		ymax.appendChild(ymax_text)
		
	with open(save_xml_dir + "/" + file[:len(file)-4] + ".xml", 'w') as f:
		f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
	
fw.close()







