#coding=utf-8

import numpy as np
import os,shutil
import random

folder_path =  "/home/zhangjing/Detectron/data/results/" #改
pre = "18060803"

num = 1
for dirpath, dirnames, filenames in os.walk(folder_path):	
	for filename in filenames:
		if filename.endswith('.xml'):
			name = filename[:len(filename)-4]
			if os.path.exists(folder_path + name+".jpg"):
				os.rename(folder_path +name+".jpg", folder_path +pre+name+".jpg")
				os.rename(folder_path +name+".xml", folder_path +pre+name+".xml")
				num = num + 1
				print (num)
	