import os
import random

from os import path

fw = open("/opt/zhangjing/caffe/caffe/data/actions_new/train1.txt",'w+')

with open("/opt/zhangjing/caffe/caffe/data/actions_new/train.txt", 'rb') as ann_file:
	lines = ann_file.readlines()
	random.shuffle(lines)
	for l in lines:
		fw.write(l)
fw.close()
			
