#coding=utf-8
'''
脚本功能：已知图片所在文件夹，生成txt；txt内容为pictures/0125040105.jpg labels/0125040105.xml
'''
import numpy as np
import os,shutil
import random

folder_path1 =  "/opt/yushan/caffe/data/actions_new/" #改
folder_name = "network/" #改

fw = open( folder_path1 + folder_name[:len(folder_name)-1] + ".txt", 'w')	
folder_path = folder_path1 + folder_name

xml_lst = []
for dirpath, dirnames, filenames in os.walk(folder_path + "labels/"):	#'labels' 可改
	for filename in filenames:
		if filename.endswith('.xml'):
			xml_lst.append( filename[:len(filename)-4] )

num = 0			
for dirpath, dirnames, filenames in os.walk(folder_path + "pictures/"):	#"pictures/" 可改
	for filename in filenames:
		random.shuffle(filenames)
		if filename.endswith('.jpg') or filename.endswith('.bmp') or filename.endswith('.png'):
			l = filename[:len(filename)-4]
			if l in xml_lst:
				fw.write( folder_name + "pictures/" + filename +  " " + folder_name + "labels/" + l+".xml\n")
				num = num + 1
				
print ("sample num: ", num)




'''
num = 0	
for dirpath, dirnames, filenames in os.walk(folder_path + "pictures/"):	#"pictures/" 可改
	for filename in filenames:
		if filename.endswith('.jpg') or filename.endswith('.bmp') or filename.endswith('.png'):
			l = filename[:len(filename)-4]
			xml_file = "/opt/yushan/caffe/data/actions/labels/" + l + ".xml"
			xml_file_dst = folder_path + "labels/" + l + ".xml"
			if os.path.exists(xml_file):
				shutil.copy(xml_file,xml_file_dst)  #文件拷贝
				num = num + 1
				print num
			else:
				#os.remove(folder_path + "pictures/" + filename)  #删除文件
				print (filename)
				
'''
			


