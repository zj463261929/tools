#coding = UTF-8
import cv2
import os
import numpy as np
import shutil

'''
save_image_dir= "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations_17116/" 
orig_image_dir= "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations_826/" #"/opt/zhangjing/caffe/data/actions_new/benchmark/pictures_1080_ratio_new_new_ratio_ratio/"
files = [x for x in os.listdir(orig_image_dir) if os.path.isfile(orig_image_dir+os.sep+x) and x.endswith('.xml')]
	
for i in xrange(len(files)): 
	file=files[i]
	#print file     
	basename = os.path.splitext(file)[0]
	
	shutil.copyfile(orig_image_dir+file,save_image_dir+file)
	print (save_image_dir+file)
	shutil.copyfile(orig_image_dir+file,save_image_dir+basename+"_gray.xml")

	print (save_image_dir+basename+"_gray.xml")
	#os.rename(orig_image_dir+file, save_image_dir+basename+"_gray.xml")
	print i
'''

save_image_dir= "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/JPEGImages_17116/" 
orig_image_dir= "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/JPEGImages_826/" #"/opt/zhangjing/caffe/data/actions_new/benchmark/pictures_1080_ratio_new_new_ratio_ratio/"
files = [x for x in os.listdir(orig_image_dir) if os.path.isfile(orig_image_dir+os.sep+x) and x.endswith('.jpg')]
	
for i in xrange(len(files)): 
	file=files[i]
	#print file     
	basename = os.path.splitext(file)[0]
	frame = cv2.imread(orig_image_dir + file)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	print (save_image_dir+file)
	cv2.imwrite(save_image_dir+file, frame)
	print (save_image_dir+basename+"_gray.jpg")
	cv2.imwrite(save_image_dir+basename+"_gray.jpg", gray)
	print i
