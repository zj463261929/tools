#coding=utf-8
import  xml.dom.minidom
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class xml_info(object):
	def __init__(self, input_width, input_height, class_name_lst):
		self.input_width = input_width   #网络输入的图像宽度
		self.input_height = input_height #网络输入的图像高度
		self.class_name_lst = class_name_lst #网络训练的类别名称

	'''
	函数名称：getBoxBasicInfo
	功能：统计box类别名称为class_name的宽高值，注意：该宽高值是根据input_width、input_height缩放以后的数值。
	参数：
		输入：
			lines：存放文件的list, 每行为pictures_864/0123030269.jpg labels_864/0123030269.xml
			folder_path：xml所在的文件夹
			class_name：类的名称 （str类型）
		输出：
			class_w_lst：宽度
			class_h_lst：高度
			
	'''
	def getBoxBasicInfo(self, lines, folder_path, class_name): 
		class_w_lst = [] #存放该类的宽度 （统一缩放到input_width）
		class_h_lst = []
		
		for l in lines:
			lst = l.strip().split()
			if 2==len(lst):	#pictures_864/0123030269.jpg labels_864/0123030269.xml
				#打开xml文档
				if not os.path.exists( folder_path+lst[1] ):
					continue
				#print folder_path+lst[1]
				dom = xml.dom.minidom.parse(folder_path+lst[1]) #用于打开一个xml文件，并将这个文件对象dom变量。
												
				root = dom.documentElement #用于得到dom对象的文档元素，并把获得的对象给root
				
				width_lst = root.getElementsByTagName("width")
				height_lst = root.getElementsByTagName("height")
				width = int(width_lst[0].firstChild.data)	#原始图片宽度
				height = int(height_lst[0].firstChild.data)
					
				xmin_lst = root.getElementsByTagName("xmin")
				ymin_lst = root.getElementsByTagName("ymin")
				xmax_lst = root.getElementsByTagName("xmax")
				ymax_lst = root.getElementsByTagName("ymax")
				'''for i in range(len(xmin_lst)):
					print xmin_lst[i].firstChild.data  #获得标签对之间的数据,如：<xmin>418</xmin>'''

				name_lst = []
				lst_temp = root.getElementsByTagName("name")
				for i in range(len(lst_temp)):
					l = lst_temp[i].firstChild.data 
					if l in self.class_name_lst:
						name_lst.append(l)
								
				num = min(len(name_lst), len(xmin_lst))
				#num = len(xmin_lst)
				# w/h
				for i in range(num):
					#print (name_lst[i], class_name)
					if name_lst[i] == class_name:
						x1 = float(xmin_lst[i].firstChild.data)
						x2 = float(xmax_lst[i].firstChild.data)
						y1 = float(ymin_lst[i].firstChild.data)
						y2 = float(ymax_lst[i].firstChild.data)
						w = x2 - x1 + 1.0
						h = y2 - y1 + 1.0
						#print (x1,x2,y1,y2,w,h)
						if (h>0 and w>0):		#(h>5 and w>5):
							#print (self.input_width/width, self.input_height/height)
							#w = w*self.input_width/width
							#h = h*self.input_height/height
							
							'''ratio = w/h
							if ratio>20:
								print folder_path+lst[1]
								print (x1,x2,y1,y2,w,h)'''
							class_w_lst.append( w )
							class_h_lst.append( h )
						else:
							print ("error xml: ", lst[1], y2, y1, x1, x2)
							
					
		return (class_w_lst, class_h_lst)
	
	'''
	函数名称：getBoxBasicInfo
	功能：根据宽度、高度，统计box的面积、宽高比
	参数：
		输入：
			w_lst：宽度
			h_lst：高度
		输出：
			area_lst： 面积
			ratio_lst：宽高比
	'''
	def getBoxAreaRatio(self, w_lst, h_lst):
		ratio_lst = []
		area_lst = []
		
		num = min(len(w_lst), len(h_lst))
		for i in range(num):
			area = w_lst[i] * h_lst[i]
			ratio = w_lst[i] / h_lst[i]
			
			area_lst.append( area )
			ratio_lst.append( ratio )
			
		return (area_lst, ratio_lst)
		
		
	#data_lst: 是面积或者宽高比的数值； interval：是采样的间隔；
	#返回值：(interval_lst, num_lst)是采样的数值、采样数据的直方图
	def get_histogram(self, data_lst, interval=20 ):
		lst = []
		for i in range(len(data_lst)):
			#lst.append( int(data_lst[i]*100)/100.0  )
			lst.append( int(data_lst[i]*10000)/10000.0  )
		#print (len(temp))

		interval_lst = []
		for d in np.arange(min(lst), max(lst), interval):
			interval_lst.append( d )
		interval_lst.append( max(lst) )

		num = len(interval_lst) - 1
		num_arr = np.zeros( num )
		for ii in range( len(lst) ):
			data = lst[ii]
			for i in range( num ):
				if num-1 == i:
					if data >=interval_lst[i] and data<=interval_lst[i+1]:
						num_arr[i] = num_arr[i] + 1
				else:
					if data >=interval_lst[i] and data<interval_lst[i+1]:
						num_arr[i] = num_arr[i] + 1
		num_lst = [0]
		for i in range(num):
			num_lst.append( num_arr[i] )
		return (interval_lst, num_lst)		
	
	#将数据分段显示
	def draw_histogram(self, interval_lst, num_lst, level, filename):
		plt.clf() 
		## 'r--'红色的破折号，'bs'蓝色的方块，'g^'绿色的三角形, 'ro' 红色 散点
		color_lst = ['r', 'g', 'b', 'r--', 'g--', 'b--', 'rs', 'gs', 'bs', 'r^', 'g^', 'b^', 'ro', 'go', 'bo']
		if level > len(color_lst):
			level = len(color_lst)
		num = len(interval_lst)
		num1 = num/level

		if 1==level:
			plt.xlim(interval_lst[0], interval_lst[num1-1])# set axis limits
		else:
			plt.xlim(interval_lst[0], interval_lst[num1])# set axis limits
		plt.ylim(0.0, np.max(num_lst) )
		
		for i in range(level):
			lst_x = []
			lst_y = []
			for ii in range(num1):
				lst_x.append( interval_lst[i*num1 + ii] - interval_lst[i*num1] )
				lst_y.append( num_lst[i*num1 + ii] )
				
			s = "data(" + str(min(lst_x) + interval_lst[i*num1]) + "," + str(max(lst_x) + interval_lst[i*num1]) + ")"
			plt.plot(lst_x, lst_y, color_lst[i], label=s) #

		plt.legend(loc='upper right', shadow=True, fontsize='x-large')# make legend

		plt.title('histogram') 
		plt.xlabel('data')
		plt.ylabel('num')

		plt.show()# show the plot on the screen
		plt.savefig(filename)

	def get_anchor_info(self, ratio_interval, area_interval, area_lst, ratio_lst):
		if ratio_interval[0] > min(ratio_lst):
			#ratio_interval.insert(0, int(min(ratio_lst)*100)/100.0 - 1.0)
			ratio_interval[0] = int(min(ratio_lst)*100)/100.0 - 0.05
		#print min(ratio_lst)
		#print ratio_interval
		num = len(ratio_interval)
		if ratio_interval[num-1] < max(ratio_lst):
			#ratio_interval.insert(num, int(max(ratio_lst)*100)/100.0 + 1.0)
			ratio_interval[num-1] = int(max(ratio_lst)*100)/100.0 + 1.0
		
		#print (area_interval)
		if area_interval[0] > min(area_lst):
			#area_interval.insert(0, int(min(area_lst)*100)/100.0 - 1.0)
			area_interval[0] = int(min(area_lst)*100)/100.0 - 0.05
		num = len(area_interval)
		if area_interval[num-1] < max(area_lst):
			#area_interval.insert(num, int(max(area_lst)*100)/100.0 + 1.0)
			area_interval[num-1] = int(max(area_lst)*100)/100.0 + 1.0
		#print (area_interval)
		
		rows = len(area_interval) - 1
		cols = len(ratio_interval) - 1
		num_arr = np.zeros( (rows, cols) )
		for ii in range( len(ratio_lst) ):
			area = int(area_lst[ii]*100)/100.0 
			ratio = int(ratio_lst[ii]*100)/100.0  #保留2位小数点
			
			for row in range(rows):
				for col in range(cols):		
					if ( area>=area_interval[row] and area<area_interval[row+1]):
						if (ratio >=ratio_interval[col] and ratio<ratio_interval[col+1]):
							num_arr[row][col] = num_arr[row][col] + 1
	
			
		return (num_arr, ratio_interval, area_interval)

##############################################################################################
#主函数
class_name_lst = ["autotruck", "forklift", "digger", "car", "bus", "tanker", "person", "minitruck", "minibus"] 
#class_name_lst = ["autotruck", "crane", "digger", "mixerTruck", "forklift", "colorPlate", "pit", "bricksPile", "mound", "worker", "car"] 
#class_name_lst = ["aeroplane","bicycle","bird","boat","bottle","bus","car","cat","chair","cow","diningtable","dog","horse","motorbike","person","pottedplant","sheep","sofa","train","tvmonitor"]
				#["handsup", "like", "hate", "sleep"] #类别名称, 	改
input_width = 1920	#训练网络结构中指定的输入图片宽高，	改
input_height = 1080	#	改


folder_path = "/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations/" 		#改
xml_file = open("/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/val_30_40_aug.txt", 'r') 	#改
#xml_file = open("/opt/zhangjing/caffe/caffe/data/actions_new/" + "test.txt", 'r') 	#改
lines = xml_file.readlines()
#print ("file path: ", folder_path + "benchmark.txt")
print ("xml num = ", len(lines))

c = xml_info(input_width, input_height, class_name_lst)

all_w_lst = []
all_h_lst = []
all_area_lst = []
all_ratio_lst = []
all_num_lst = []

for i in range(len(class_name_lst)):
	class_name = class_name_lst[i].strip()
	w_lst, h_lst = c.getBoxBasicInfo(lines, folder_path, class_name) #改 "handsup"
	area_lst, ratio_lst = c.getBoxAreaRatio(w_lst, h_lst)	#某个类别的宽高比、面积
	#print len(w_lst)
	
	if len(w_lst)>0:
		print (" %s box info: ", class_name)
		print ("num = ", len(w_lst))
		print ("(minW,minH,maxW,maxH)=", int(min(w_lst)*100)/100.0, int(min(h_lst)*100)/100.0, int(max(w_lst)*100)/100.0, int(max(h_lst)*100)/100.0)
		print ("(minArea, maxArea)=", int(min(area_lst)*100)/100.0, int(max(area_lst)*100)/100.0)
		print ("(minRatio, maxRatio)=\n", int(min(ratio_lst)*100)/100.0, int(max(ratio_lst)*100)/100.0)
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
		
		all_w_lst = all_w_lst + w_lst
		all_h_lst = all_h_lst + h_lst
		all_area_lst = all_area_lst + area_lst
		all_ratio_lst = all_ratio_lst + ratio_lst
		all_num_lst.append(len(w_lst))
		print "\n"

if len(all_w_lst)>0:
	print (" all box info: ")
	print ("num = ", len(all_w_lst))
	print ("(minW,minH,maxW,maxH)=", int(min(all_w_lst)*100)/100.0, int(min(all_h_lst)*100)/100.0, int(max(all_w_lst)*100)/100.0, int(max(all_h_lst)*100)/100.0)
	print ("(minArea, maxArea)=", int(min(all_area_lst)*100)/100.0, int(max(all_area_lst)*100)/100.0)
	print ("(minRatio, maxRatio)=\n", int(min(all_ratio_lst)*100)/100.0, int(max(all_ratio_lst)*100)/100.0)
	print "\n"
		
'''	print "class/all_num:"
for i in range(len(all_num_lst)):
	class_name = class_name_lst[i].strip()
	print class_name, all_num_lst[i], all_num_lst[i]/(len(all_w_lst)+0.0)*100,"%"


#计算占空比
dutyRatio_lst = [] #存放所有类别box的占空比
area = input_width*input_height + 0.0000001
for i in range( len(all_area_lst) ):
	dutyRatio_lst.append( all_area_lst[i]/area ) 

#print (dutyRatio_lst)
#以一定间隔为单位来统计面积或宽高比的直方图
interval_lst, num_lst = c.get_histogram(dutyRatio_lst, interval=0.0005) #(ratio_lst, 0.05)
c.draw_histogram(interval_lst, num_lst, 3, "dutyRatio.png") #以图的形式展示出来，interval_lst为x坐标（面积或宽高比的大小），num_lst为y轴（面积或宽高比的个数）


#以一定间隔为单位来统计面积或宽高比的直方图
interval_lst, num_lst = c.get_histogram(all_area_lst, interval=20) #(ratio_lst, 0.05)
c.draw_histogram(interval_lst, num_lst, 3, "area.png") #以图的形式展示出来，interval_lst为x坐标（面积或宽高比的大小），num_lst为y轴（面积或宽高比的个数）

#以一定间隔为单位来统计面积或宽高比的直方图
interval_lst, num_lst = c.get_histogram(all_ratio_lst, interval=0.05) #(ratio_lst, 0.05)
c.draw_histogram(interval_lst, num_lst, 3, "whRatio.png") #以图的形式展示出来，interval_lst为x坐标（面积或宽高比的大小），num_lst为y轴（面积或宽高比的个数）


#统计分布
area_interval = [35.84*35.84, 76.8*76.8, 153.6*153.6, 230.4*230.4, 307.2*307.2, 384.0*384.0, 460.8*460.8, 537.6*537.6] #VOC
#area_interval = [20.48*20.48, 46.72*46.72, 128.57*128.57, 210.42*210.42, 292.27*292.27, 374.12*374.12, 455.97*455.97, 537.6*537.6]# 改
#area_interval = [20.48*20.48, 51.2*51.2, 133.12*133.12, 215.04*215.04, 296.96*296.96, 378.88*378.88, 460.8*460.8, 542.72*542.72] #coco
#ratio_interval = [0.2,0.25,0.33,0.5,0.7,1.0,1.2,1.4,1.6,2.0]	#改
ratio_interval = [0.2, 0.24, 0.29, 0.8, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]	#改

#统计面积落入某个面积间隔区域内，同时宽高比也落入某个宽高比间隔区域的个数
num_arr, ratio_interval, area_interval = c.get_anchor_info(ratio_interval, area_interval, all_area_lst, all_ratio_lst)
print ("area_interval:", area_interval)		
print ("ratio_interval:", ratio_interval)
print ("num: ")					#num_arr的列表示ratio_interval
for row in range(num_arr.shape[0]):	
	print ( num_arr[row][:])
#print ("sum: ", np.sum(num_arr))
'''
xml_file.close()




