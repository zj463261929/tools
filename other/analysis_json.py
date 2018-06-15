#coding=utf-8
import os
import random
from os import path
import json
import numpy as np

#fw = open("/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/val_30_40_aug.txt",'w+')

class_name_lst = ["autotruck", "forklift", "digger", "car", "bus", "tanker", "person", "minitruck", "minibus"] 

num = 0
#folder_path = "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations/"
##json路径
with open("/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/voc_oil_train_18768.json", "r") as f:
	ann_data = json.load(f)
	images = ann_data["images"]
	print ("images num = ", len(images))
	annotations = ann_data["annotations"]
	print ("all box num = ", len(annotations))
	
	def get_bboxArea(annotations, class_index):
		lst = []
		for ann in annotations:
			image_id = ann["image_id"]		#"i
			bbox = ann["bbox"]
			area = bbox[3]*bbox[2]
			category_id = ann["category_id"]
			if class_index == category_id:
				lst.append( area )
		return lst		
	
	for n in range(len(class_name_lst)):
		area_lst = get_bboxArea(annotations, n+1)
		print (class_name_lst[n], len(area_lst))
		num = 0
		for area in area_lst:
			if area>30*30:
				num = num + 1
		print ("area >30*30 num=", num)
		num = 0
		for area in area_lst:
			if area>40*40:
				num = num + 1
		print ("area >40*40 num=", num)
		num = 0
		for area in area_lst:
			if area>50*50:
				num = num + 1
		print ("area >50*50 num=", num)
		num = 0
		for area in area_lst:
			if area>60*60:
				num = num + 1
		print ("area >60*60 num=", num)
		
		print ("\n")