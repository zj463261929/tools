#coding=utf-8
import codecs
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import re
import os
import cv2
import random
import sys
from PIL import Image 
sys.path.append(os.path.join(os.getcwd(),'/opt/zhangjing/ocr/Attention-OCR-chinese-version/src/model')) #通知解释器除了在默认路径下查找模块外，还要从指定的路径下查找。指定完模块路径后，就可以导入自己的模块了。
import _trietree as trieTree
reload(sys)
sys.setdefaultencoding("utf-8")

annotation_path = "/opt/ligang/data/pic2000_15_data_2017_5_31/result_img_word_test/WordBBText.txt"#"/opt/datasets/data/str/SynthTextforRecognition/train.txt" #"/opt/datasets/data/str/mnt/ramdisk/max/90kDICT32px/annotation_train_new.txt"
annotation_path1 = "word_label.txt"
annotation_path2 = "class_times.txt"
annotation_path3 = "/opt/ligang/data/pic2000_15_data_2017_5_31/result_img_word_test/WordBBText_new.txt"


'''
l = list('4e00')
l = int("4e00",16) 
print l'''

class chinese_process(object):
	def __init__(self, inputpath, outputpath):
		self.inputpath = inputpath
		self.outputpath = outputpath
		self.words = []
		self.labels = []
		
	def get_WordandLabel(self):
		with codecs.open(inputpath, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			lst = []
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					word = lst[0]
					lex = lst[1]
					self.words.append(word)
					self.labels.append(lex)

	#1.统计annotation_path2文件中字的频率少于50的字；
	#2.根据第一步的结果，去除annotation_path中含有字频少于50的词；
	def remove_word_less(self):
		fw =  codecs.open(annotation_path3, 'w', "utf-8") 
		letter = []
		freq = []
		with codecs.open(annotation_path2, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				word, lex = l.strip().split()
				#print (word)		
				#word = word[len(word)-1]
				letter.append(word)
				freq.append(lex)
				#print (word.encode("utf-8"))
				#print lex
		
		letter_new = []
		for i in range(len(letter)):
			if int(freq[i]) > 50:
				#print (freq[i])
				letter_new.append(letter[i])
				#print (letter[i].encode("utf-8"))
		
		with codecs.open(annotation_path, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			#random.shuffle(lines)
			n = 0
			for l in lines:
				img_path, lex = l.strip().split() 
		
				#print lex
				if lex==None:
					continue
				else:
					#print ("\n")
					n = 0
					for c in lex:
						#print (c.encode("utf-8"))
						if c not in letter_new:
							#print ("111111111")
							n = n + 1
			
					if n < 1:
						fw.write(img_path + " " + lex + '\n')
					#print ("22222222")
	
	def get_word_freq(self):
		self.get_WordandLabel()
		lst = []
		for l in self.labels:
			for c in l:
				lst.append(c)
		
		lst1 = list(set(lst)) #去重复的
		res_lst = []
		with codecs.open(outputpath, 'w', 'utf-8') as fw:
			for c in lst1:
				num = lst.count(c)
				fw.write(c + " " + str(num) + "\n" )
		
	def get_correctWord_num(self):#得到识别正确样本的个数
		self.get_word_freq()
		letter = []
		freq = []
		with codecs.open(annotation_path2, 'rb', "utf-8") as ann_file: #读取字频文件
			lines = ann_file.readlines()
			for l in lines:
				word, lex = l.strip().split()
				#print (word)		
				word = word[1:len(word)-1]
				letter.append(word)
				freq.append(lex)
				#print (word.encode("utf-8"))
				#print lex
				
		with codecs.open(outputpath, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				word1, lex1 = l.strip().split()
				#print (word)		
				#print (word1.encode("utf-8"))
				if word1 in letter:
					#print ("11111111111")
					index1 = letter.index(word1)
					fw.write(word1 + " " + freq[index1] + " " + lex1 + "\n" )
				#print (word.encode("utf-8"))
				#print lex
	def get_lst2(self, path):
		word = []
		lex = []
		with codecs.open(path, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					word.append(lst[0])
					lex.append(lst[1])
					
		return word, lex
		
	def get_lst(self, path):
		word = []
		lex = []
		with codecs.open(path, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 2:
					word.append(lst[1])
					lex.append(lst[2])
					
		return word, lex
		
	def get_correct(self):#获得正确识别的每个字的个数
		word, lex = self.get_lst("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/correct.txt")
		lst = []
		for l in word:
			for c in l:
				lst.append(c)
		
		lst1 = list(set(lst)) #去重复的
		lst_num = []
		for c in lst1:
			num = lst.count(c)
			lst_num.append(num)
			
		return 	lst #
		
	def get_imcorrect(self):
		word, lex = self.get_lst("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/imcorrect.txt")
		
		correct = []
		imcorrect = []
		for i in range(len(word)):
			if len(word[i]) == len(lex[i]):
				for ii in range(len(word[i])):
					if word[i][ii]==lex[i][ii]:
						correct.append(lex[i][ii])
					else:
						imcorrect.append(lex[i][ii])
			elif len(word[i]) < len(lex[i]):
				for ii in range(len(word[i]), len(lex[i])):
					imcorrect.append(lex[i][ii])
			elif len(word[i]) > len(lex[i]):
				for ii in range(len(lex[i]), len(word[i])):
					imcorrect.append(word[i][ii])
			
		return correct, imcorrect
	
	def get_precision(self): #分析识别结果中每个字正确识别个数/错误识别个数
		lst_correct = self.get_correct()
		lst1_correct,lst1_imcorrect = self.get_imcorrect()
		
		label, lex = self.get_lst2(r"/opt/zhangjing/ocr/Attention-OCR-chinese-version/word_label.txt")
		label1, freq = self.get_lst2(r"/opt/zhangjing/ocr/Attention-OCR-chinese-version/class_times_21.txt")
		lst = []
		for c in label1:
			#print c.encode("utf-8")
			lst.append(c)#c[1:len(c)-1]
			
		fw = codecs.open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/letter_precision.txt", 'w', 'utf-8')	
		for c in label:
			#统计正确的
			correct_num = 0
			imcorrect_num = 0
			if c in lst_correct:
				correct_num = correct_num + lst_correct.count(c)
			if c in lst1_correct:
				correct_num = correct_num + lst1_correct.count(c)
			if c in lst1_imcorrect:
				imcorrect_num = imcorrect_num + lst1_imcorrect.count(c)
				
			if c in lst:
				index1 = lst.index(c)
				fw.write(c + " "+ str(correct_num) + " " + str(imcorrect_num) + " " + str(correct_num+imcorrect_num)+ " " + str(correct_num/(correct_num+imcorrect_num+0.00000001)) + " " + str(404*13+100) + "\n")#freq[index1] + "\n")
		
	def get_word_precision(self):
		word, lex = self.get_lst("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/correct.txt")
		word_im, lex_im = self.get_lst("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/imcorrect.txt")
		path, label = self.get_lst2("/opt/ligang/data/pic2000_data_2017_6_15/train.txt")
		
		fw = codecs.open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/word_precision.txt", 'w', 'utf-8')	
		lst = [] 
		lst = word + word_im
		lst1 = list(set(lst)) #去重复的
		for l in lst1:
			correct_num = 0
			imcorrect_num = 0
			num = 0
			if l in word:
				correct_num = word.count(l)
			if l in word_im:
				imcorrect_num = word_im.count(l)
			if l in label:
				num = label.count(l)
			fw.write(l + " "+ str(correct_num) + " " + str(imcorrect_num) + " " + str(correct_num+imcorrect_num)+ " " + str(correct_num/(correct_num+imcorrect_num+0.00000001)) + " " + str(num)+ "\n")
	
	def draw_precision(self, path):#画准确率与样本个数
		prec = []
		num = []
		with codecs.open(path, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 5:
					prec.append(lst[4])
					num.append(int(lst[5].encode("utf-8"))) # u'36'->36
					
		#print max(num)#num[10].encode("utf-8")		
		plt.xlim(0, 1000)#max(num)/2)# set axis limits
		plt.ylim(0.0, 1.0)
			
		plt.plot(num, prec, "ro")#'r') #'ro' 红色 散点
		#plt.legend(loc='upper right', shadow=True, fontsize='x-large')# make legend

		plt.title('precion & sample num') 
		plt.xlabel('sample num')
		plt.ylabel('precsion')
		
		l = path #os.path.dirname(path)
		l = l[:len(l)-3] + "png"
		plt.show()# show the plot on the screen
		plt.savefig(l)
		
	def get_incorrect_image(self):
		path = "/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/imcorrect_32"
		with codecs.open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/imcorrect.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 2:
					img = cv2.imread(lst[0])
					img = cv2.resize (img,(100,32)) 	
					lst1 = lst[0].strip().split("/")
					s = path + "/" + lst1[len(lst1)-1]
					print (s)
					cv2.imwrite(s, img)
					
	def get_letter_times(self):	
		fw = codecs.open("/opt/ligang/data/icdar2017rctw/letter_times_icdar2017chinese.txt", 'w', 'utf-8')	
		lst = []
		with codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText_new.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2) > 1:
					for c in lst2[1]:
						lst.append(c)
		
		lst1 = list(set(lst)) #去重复的
		for c in lst1:
			num = lst.count(c)
			fw.write(c + " "+ str(num) + "\n")
		fw.close()
		
	def is_chinese(self, uchar): #判断一个unicode是否是汉字  例如：uchar = \u4e00
		if uchar.find("\u", 0) > -1:
			uchar = uchar[2:] #4e00
			print uchar
			uchar = int(uchar,16) #转成10进制，4e00->19968   9fa5->40869
			if uchar >= 19968 and uchar<=40869:#if uchar >= u'\u4e00' and uchar<=u'\u9fa5':		
				return True
			else:
				return False
				
	def get_word_times(self):	
		fw = codecs.open("/opt/maoshaojiang/myProject/simple-syntext/syndata_cn/word_times_241.txt", 'w', 'utf-8')	
		lst = []
		with codecs.open("/opt/maoshaojiang/myProject/simple-syntext/syndata_cn/R_label_241.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2) > 1:
					lst.append(lst2[1])
		
		lst1 = list(set(lst)) #去重复的
		for c in lst1:
			cc = c.encode("raw_unicode_escape")
			c1 = c
			if not self.is_chinese(cc):
				c1 = c1.lower()
				
			num = lst.count(c)
			fw.write(c1 + " "+ str(num) + "\n")
		fw.close()
		
	def get_train_test_data(self):
		words = []
		nums = []
		with codecs.open("/opt/ligang/data/pic2000_data_2017_6_15/zj/word_times.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2) > 1:
					words.append(lst2[0])
					nums.append(int(lst2[1]))
					
		num_min = min(nums)
		print nums
		print num_min
		path_train = "/opt/ligang/data/pic2000_data_2017_6_15/zj/no_equal/train/"
		path_test = "/opt/ligang/data/pic2000_data_2017_6_15/zj/no_equal/test/"
		fw_train = codecs.open(path_train + "train.txt", 'w', 'utf-8')
		fw_test = codecs.open(path_test+ "test.txt", 'w', 'utf-8')
		
		class_num = len(words)
		train_num = [0]*class_num
		test_num = [0]*class_num
		
		lst = []
		path = "/opt/ligang/data/pic2000_data_2017_6_15/zj/total/"
		with codecs.open("/opt/ligang/data/pic2000_data_2017_6_15/zj/total/total.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			random.shuffle(lines)
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2) > 1:
					image_path = lst2[0]
					label = lst2[1]
					if label in words:
						index1 = words.index(label)
						img = cv2.imread(path+image_path)
						
						if train_num[index1] < nums[index1]-int(num_min*0.1): #int(num_min*0.9):均衡的参数，nums[index1]-int(num_min*0.1)不均衡的参数
							s = path_train + image_path
							cv2.imwrite(s, img)
							fw_train.write(image_path + " " + label + "\n")
							train_num[index1] = train_num[index1] + 1
						else:#if test_num[index1] < int(num_min*0.1):
							s = path_test + image_path
							cv2.imwrite(s, img)
							fw_test.write(image_path + " " + label + "\n")
							test_num[index1] = test_num[index1] + 1
						
		fw_test.close()
		fw_train.close()
		
	def test(self):
		'''
		
		image_path = path_train + "01667_0_王.jpg"
		#print (image_path.encode("utf-8"))
		img = cv2.imread(image_path)
		cv2.imwrite("/opt/maoshaojiang/myProject/simple-syntext/syndata_cn/01667_0_王_h.jpg", img)
		'''
		n = 0
		fw = codecs.open("/opt/yangmiao/synthdata/synthdata_30804/train_label_new.txt", 'w', 'utf-8')	
		path_train = "/opt/ligang/data/icdar2017rctw/train-word/"
		path_train_result = "/opt/ligang/data/icdar2017rctw/train-word_32*100/"
		with codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText_chinese.txt", 'r', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			#lines=[line.decode('utf-8') for line in ann_file1.readlines()]
			#random.shuffle(lines)
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2) > 1:
					image_path = lst2[0]
					s = path_train + image_path
					#img = Image.open(image_path)
					img = cv2.imread(s)#image_path)
					if img != None:
						#fw.write(image_path)
						img = cv2.resize(img, (100, 32))#img.resize((100, 32),Image.ANTIALIAS)	#	Image.BILINEAR) 
			
						'''img_bw = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
						img_bw = np.asarray(img_bw, dtype=np.uint8)
						img_bw = img_bw[np.newaxis, :]'''

						#s = path_train + "1.png"
						cv2.imwrite(path_train_result+image_path, img)
						n = n+1
					#return 
				
				print (n)	
				
	def get_train_test_txt(self):
		images = []
		labels = []
		with codecs.open("R_test_label.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2) > 1:
					images.append(lst2[0])
					labels.append(lst2[1])
					
		num_min = 2033
		path_train = ""
		path_test = ""
		fw_train = codecs.open(path_train + "R_train.txt", 'w', 'utf-8')
		fw_test = codecs.open(path_test+ "R_test.txt", 'w', 'utf-8')
		
		labels1 = list(set(labels))
		word_num = len(labels1) #词的个数
		train_num = np.zeros(word_num)
		test_num = np.zeros(word_num)
		#print (train_num)
		train_num[10] = train_num[10] + 1
		#print (train_num[10])
		
		lst = []
		with codecs.open("R_test_label.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			random.shuffle(lines)
			for l in lines:
				print ("\n")
				lst2 = l.strip().split() 
				if len(lst2) > 1:
					image_path = lst2[0]
					label = lst2[1]
					if label in labels1:
						index1 = labels1.index(label)
						print (index1 )#train_num[index1])
						if int(train_num[index1]) < int(num_min*0.9):#均衡的参数，nums[index1]-int(num_min*0.1)不均衡的参数
							fw_train.write(image_path + " " + label + "\n")
							train_num[index1] = train_num[index1] + 1
							print (train_num[index1])
						else:#if test_num[index1] < int(num_min*0.1):
							fw_test.write(image_path + " " + label + "\n")
							test_num[index1] = test_num[index1] + 1
							print ("11111")
						
		fw_test.close()
		fw_train.close()
		
	
	def get_folder_filename(self):
		image_path = []
		labels = []
		with codecs.open("/opt/ligang/data/pic2000_data_2017_6_15/zj/total/total.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2) > 1:
					image_path.append(lst2[0][:len(lst2[0])-4]) #假如图片名为11.jpg,只保存11
					labels.append(lst2[1])
					
		fw = codecs.open("/opt/ligang/data/pic2000_data_2017_6_15/zj/enhance/test/test.txt", 'w', 'utf-8')
		for root, dirs, files in os.walk("/opt/ligang/data/pic2000_data_2017_6_15/zj/enhance/test"):  
			#print(root) #当前目录路径  
			#print(dirs) #当前路径下所有子目录  
			#print(files) #当前路径下所有非目录子文件  
			for l in files:
				lst2 = l.strip().split("+")
				if len(lst2) > 1: #表示是对增强图像进行打标签，图片路径与原图之间用“+”连接
					ll = lst2[0]
				else :
					ll = l[:len(l)-4]
					
				if ll in image_path:
					index1 = image_path.index(ll)
					#print index1
					fw.write(l + " " + labels[index1] + "\n")
		fw.close()
		
	def compare_data(self):
		lst = [0]*3
		with codecs.open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/data.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			i = 0
			for l in lines:
				lst[i] = l.strip().split() 
				i = i + 1
		n = 0
		for j in range(len(lst[0])):
			if not (lst[0][j] == lst[1][j] and lst[0][j] == lst[2][j]):
				n = n + 1
		print (n)
		
	def get_equal_sample(self):
		lst = []
		fw = codecs.open("/opt/maoshaojiang/myProject/simple-syntext/syndata_cn/R_label_zj_0626.txt", 'w', 'utf-8')
		with codecs.open("/opt/maoshaojiang/myProject/simple-syntext/syndata_cn/R_label_11.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2)>1:
					lst.append(lst2[1])
					
		lst1 = list(set(lst)) #去重复的		
		lst_new = []
		for c in lst1:
			num = lst.count(c)
			if num==2033:
				lst_new.append(c)
				
		for l in lines:
			lst2 = l.strip().split() 
			if len(lst2)>1:
				if lst2[1] in lst_new:
					fw.write(lst2[0] + " " + lst2[1] + "\n")
		fw.close()
	
	def remove_some_sample(self):
		fw = codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText_new.txt", 'w', 'utf-8')
		with codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2)>1:
					img = cv2.imread("/opt/ligang/data/icdar2017rctw/train-word/" + lst2[0]) 
					lst = img.shape
					if float(lst[0]/lst[1])<1:
						fw.write(lst2[0] + " " + lst2[1] + " " + "\n")
		fw.close()		
	
	def get_image_label(self):
		fw = codecs.open("/opt/ligang/data/pic2000_data_2017_6_15/zj/enhance/2017_7/2017_7.txt", 'w', 'utf-8')
		for root, dirs, files in os.walk("/opt/ligang/data/pic2000_data_2017_6_15/zj/enhance/2017_7"):  
			#print(root) #当前目录路径  
			#print(dirs) #当前路径下所有子目录  
			#print(files) #当前路径下所有非目录子文件  
			s = u"血运重"
			for l in files:
				fw.write(l + " " + s + "\n")
		fw.close()
	
	def remove_letter_less(self):
		fw = codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText_new_50.txt", 'w', 'utf-8')
		lst = []
		with codecs.open("/opt/ligang/data/icdar2017rctw/letter_times_icdar2017chinese.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2)>1:
					print (lst2[1])
					if int(lst2[1]) < 50:
						lst.append( lst2[0] )
						print (lst2[0].encode("utf-8"))
						
		print (len(lst))
		with codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText_new.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				n = -1
				if len(lst2)>1:
					for c in lst2[1]:
						if c in lst:
							n = n + 1
				if n < 0 and len(lst2[1])<32:
					fw.write(lst2[0] + " "+ lst2[1] + " " + "\n")
						
	def get_idioms_explain(self): 
		#fw = codecs.open("idioms_31648_explain_.txt", 'w', 'utf-8')
		words = []
		explains = []
		with codecs.open("idioms_31648_explain.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				index1 = l.find("拼音")
				if index1 > -1:
					l1 = l[:index1].strip()
					l2 = l[index1:].strip()
					words.append( l1 )
					explains.append ( l2 )
					#fw.write(l1 + " " + l2 + "\n")
		
	def get_idioms_label(self): 
		fw = codecs.open("idioms_30804_freq.txt", 'w', 'utf-8')
		words = []
		freqs = []
		with codecs.open("THUOCL_chengyu.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2)>1:
					words.append( lst2[0] )
					freqs.append( lst2[1] )
		
		with codecs.open("idioms_30804.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip()
				if lst2 in words:
					index1 = words.index(lst2)
					if index1 > -1:
						fw.write(lst2 + " " + freqs[index1] + "\n")
				else:
					fw.write(lst2 + " " + str(10) + "\n")
	
	def copy_data(self):
		fw = codecs.open("/opt/ligang/data/icdar2017rctw/train_new.txt", 'w', 'utf-8')
	
		w_path = "/opt/ligang/data/icdar2017rctw/train_new/"
		i_path = "/opt/ligang/data/icdar2017rctw/test/"
		with codecs.open("/opt/ligang/data/icdar2017rctw/test.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2)>1:
					img = cv2.imread(i_path + lst2[0])
					for i in range(100):
						s = w_path + lst2[0][:len(lst2[0])-4] + "_" + str(i) + ".bmp"
						cv2.imwrite(s, img)
						fw.write(lst2[0][:len(lst2[0])-4] + "_" + str(i) + ".bmp" + " " + lst2[1] + "\n")
		
	def test_data(self):
		#字+字 或 词+词：
		fw = codecs.open("/opt/yangmiao/synthdata/finaldict_new_test_10.txt", 'w', 'utf-8')
		word = []
		with codecs.open("/opt/yangmiao/synthdata/word_label_10.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			random.shuffle(lines)
			for i in range(10):
				num = 0
				for l in lines:
					lst2 = l.strip().split() 
					if len(lst2)>1:
						if num < 1000*(i+1):
							num = num+1
							word.append( lst2[0] )
							if num%(i+1) == 0:
								s = "".join(word)
								fw.write(s + "\n")
								word = []
								
		word = []
		with codecs.open("/opt/yangmiao/synthdata/finaldict_new_10.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			random.shuffle(lines)
			for i in range(3):
				num = 0
				for l in lines:
					lst2 = l.strip().split() 
					if len(lst2)>0:
						if num < 1000*(i+1):
							num = num+1
							word.append( lst2[0] )
							if num%(i+1) == 0:
								s = "".join(word)
								if len(s)<10:
									fw.write(s + "\n")
								else:
									num = num-1
								word = []
								
		fw.close()
				
	def judge_is_study(self):
		fw = codecs.open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/imcorrect_process_10_13.txt", 'w', 'utf-8')
		
		words = []
		with codecs.open("/opt/yangmiao/synthdata/finaldict_new_10.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2)>1:
					words.append( lst2[1] )
		words1 = list(set(words))
		n0 = 0
		n1 = 0
		with codecs.open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/imcorrect.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2)>2:
					s = " ".join( lst2 )
					if lst2[1] in words1:
						fw.write(s + " " + "1" + "\n")
						n1 = n1+1
					else :
						fw.write(s + " " + "0" + "\n")
						n0 = n0+1
						
			fw.close()
		print (n0,n1)
	
	def test_sample(self):
		n = 0
		path = "/opt/yangmiao/synthdata/synthdata_900/test_4"
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_label_dict_10.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			random.shuffle(lines)
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					if len(lst[1])<5 and n<500:
						img = cv2.imread("/opt/yangmiao/synthdata/synthdata_900/syndata_dict/"+lst[0])
						#img = cv2.resize (img,(100,32)) 	
						lst1 = lst[0].strip().split("/")
						s = path + "/" + lst1[len(lst1)-1]
						print (s)
						cv2.imwrite(s, img)
						n = n+1
						
	def remove_sample1(self):
		letter = []
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/word_label_5.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					letter.append(lst[0])
					
		#fw1 =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_11.txt", 'w', "utf-8")
		fw =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_label_dict_51.txt", 'w', "utf-8") #'a' 追加模型
		path = "/opt/yangmiao/synthdata/synthdata_900/syndata_dict1"
		with codecs.open("/opt/yangmiao/synthdata/synthdata_test/zj_4853_10.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					if lst[1] in letter: #len(lst[1])==7 and n<100:
						img = cv2.imread("/opt/yangmiao/synthdata/synthdata_test/zj_4853_10/"+lst[0])
						#img = cv2.resize (img,(100,32)) 	
						lst1 = lst[0].strip().split("/")
						s = path + "/" + "0" + "_" + lst1[len(lst1)-1]
						print (s)
						cv2.imwrite(s, img)
						ss = "0" + "_" + lst1[len(lst1)-1]
						lst2 = []
						lst2.append(ss)
						lst2.append(lst[1])
						sss = " ".join(lst2)
						fw.write(sss + "\n")
					'''else:
						sss = " ".join(lst)
						fw1.write(sss + "\n")'''
		fw.close()
		
	def remove_sample2(self):
		letter = []
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/test_label_dict_5.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					letter.append(lst[0])
					
		#fw1 =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_11.txt", 'w', "utf-8")
		fw =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/test_label_dict_51.txt", 'w', "utf-8") #'a' 追加模型
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/test_label_dict_10.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					if lst[0] not in letter: #len(lst[1])==7 and n<100:
						s = "/opt/yangmiao/synthdata/synthdata_900/syndata_dict/" + lst[0]
						if os.path.exists(s):
							print s
							os.remove(s)
						

		fw.close()
		'''for dirpath, dirnames, filenames in os.walk('/opt/yangmiao/synthdata/synthdata_900/syndata_dict'):
			for filename in filenames:
				if filename not in letter:
					s = "/opt/yangmiao/synthdata/synthdata_900/syndata_dict/" + filename
						if os.path.exists(s):
							print s
							os.remove(s)'''
			
		
		
						
	def test_random_shuffle(self):
		fw =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_1.txt.txt", 'w', "utf-8")
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_label_dict_10.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for i in range(1):
				random.shuffle(lines)
			for l in lines:
				lst = l.strip().split() 
				s = " ".join(lst)
				fw.write(l + "\n")
		fw.close()

		
	def test_result(self):
		word_len = np.zeros(10)
		path = "/opt/yangmiao/synthdata/synthdata_900/test_5/"
		with codecs.open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/correct_process2.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 2:
					if int(lst[2])==1: #正确识别
						word_len[int(lst[1])] = word_len[int(lst[1])] + 1
		
		for i in range(10):
			print (i, word_len[i])
	
	def test_sample1(self):
		n = 0
		image = []
		isOK = []
		isTrain = []
		
		with codecs.open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/correct_process_10_2.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 3:
					lst1 = lst[0].strip().split("/")
					image_name = lst1[len(lst1)-1]
					image.append( str(image_name) )
					isOK.append( str(1) )
					isTrain.append(lst[3])
		with codecs.open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/result/imcorrect_process_10_2.txt", 'rb', "utf-8") as ann_file2:
			lines = ann_file2.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 3:
					lst1 = lst[0].strip().split("/")
					image_name = lst1[len(lst1)-1]
					image.append( str(image_name) )
					isOK.append( str(0) )
					isTrain.append(lst[3])
		
		words = []
		path = "/opt/yangmiao/synthdata/synthdata_900/test_word1"
		with codecs.open("/opt/yangmiao/synthdata/synthdata_30804/finaldict_new_word_10_test.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					if 1:#len(lst[1])==6 and n<100:
						#img = cv2.imread("/opt/yangmiao/synthdata/synthdata_30804/finaldict_new_word_10/"+lst[0])
						#img = cv2.resize (img,(100,32)) 	
						lst1 = lst[0].strip().split("/")
						image_path = lst1[len(lst1)-1]
						#print (type(str(image_path)))
						ss = str(image_path)
						if ss in image:
							n = image.index(ss)
							#print (n)
							if n > -1:
								if int(isTrain[n]) ==1:
									s = path + "/" + isOK[n] + "_" + isTrain[n] + "_" + lst1[len(lst1)-1]
									print (s)
									#cv2.imwrite(s, img)
									words.append(lst[1])
									
		lst2 = list(set(words)) #去重复的
		
		path2 = "/opt/yangmiao/synthdata/synthdata_900/test_test_1"
		fw =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/test_test_1.txt", 'w', "utf-8")
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/test_label_dict_10.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					if lst[1] in lst2:
						img = cv2.imread("/opt/yangmiao/synthdata/synthdata_900/syndata_dict/"+lst[0])
						img = cv2.resize (img,(100,32))
						lst1 = lst[0].strip().split("/")
						s = path2 + "/" + lst1[len(lst1)-1]
						print (s)
						cv2.imwrite(s, img)
						ss = " ".join(lst)
						fw.write(ss + "\n")
		fw.close()
						
	def test2(self):	
		n = 0
		fw =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/test_label_dict_5_new.txt", 'w', "utf-8")
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/test_label_dict_5.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			random.shuffle(lines)
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					#if #:len(lst[1])<5:# and len(lst[0])<10:
					n = n + 1
				if n<100000: 
					s = " ".join(lst)
					fw.write(s + "\n")
					#fw.write(lst[0] + "\n")
		print (n)
		
	def add_sample(self):
		fw =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/test_label_dict_5+10.txt", 'w', "utf-8")
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/test_label_dict_5.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					s = " ".join(lst)
					fw.write(s + "\n")
		
		with codecs.open("/opt/ligang/synthdata_test/test_label_dict.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					s = " ".join(lst)
					fw.write(s + "\n")			
					
	def random_sample(self):
		n = 0
		i = 0
		nn = 0
		ll = []
		fw =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_label_dict_random_10.txt", 'w', "utf-8")
		words = []
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_label_dict_10.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			for l in lines:
				lst2 = l.strip().split() 
				if len(lst2)>1:
					words.append( lst2[1] )
		words1 = list(set(words))
		print len(words1)
		
		with codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_label_dict_10.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for word in words1:
				for l in lines:
					lst = l.strip().split() 
					if len(lst) > 1:
						s = " ".join(lst)
						if lst[1] == word: 
							ll.append(s)
				if len(ll) > 0:
					id = int(np.floor(np.random.rand(5,(0.3,1))[0]*5)) #np.random.randint(5) 生成5个随机数（0,1,2,3,4）
					n = len(ll)-1
					id = int(id/n*n)
					#print id, len(ll)
					fw.write(ll[id] + "\n")
					ll = []
				i = i+1
				print i
				
	def get_imageAbsPath(self):
		path = []
		path.append("/opt/ligang/data/icdar2017rctw/train-word/")
		path.append("/opt/ligang/data/icdar2017rctw/augmented_dataset/other/img/")
		path.append("/opt/ligang/data/icdar2017rctw/augmented_dataset/ElasticDistortion/img/")
		
		file = []
		file.append("/opt/ligang/data/icdar2017rctw/WordBBText_chinese.txt")
		file.append("/opt/ligang/data/icdar2017rctw/augmented_dataset/other/label.txt")
		file.append("/opt/ligang/data/icdar2017rctw/augmented_dataset/ElasticDistortion/label.txt")
		
		
		#fw =  codecs.open("/opt/yangmiao/synthdata/datasets/zj/val_datasets_10_20170918.txt", 'w', "utf-8")
		fw =  codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText_chinese_augment.txt", 'w', "utf-8")
		
		n = 0
		for i in range(min(len(path),len(file))):
			print file[i]
			ann_file = codecs.open(file[i], 'rb', "utf-8")
			lines = ann_file.readlines()
			print len(lines)
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:# and n<20:
					w = path[i] + lst[0]
					ll = []
					ll.append(w)
					ll.append(lst[1])
					ss = " ".join(ll)
					#print ss
					fw.write(ss + "\n")
					n = n+1
		fw.close()
		print n
		
	def get_add_txt(self):
		path = "/opt/yangmiao/synthdata/datasets/train/finaldict_new_10_2017808/"
		file = []
		file.append("finaldict_new_10_train1.txt")
		file.append("finaldict_new_10_train2.txt")
		
		fw =  codecs.open("/opt/yangmiao/synthdata/datasets/train/finaldict_new_10_2017808/finaldict_new_10_train.txt", 'w', "utf-8")
		
		for i in range(2):
			ann_file = codecs.open(path+file[i], 'rb', "utf-8")
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:# and n<20:
					s = " ".join(lst)
					fw.write(s + "\n")

	def delete_col(self):
		fw =  codecs.open("/opt/yangmiao/synthdata/datasets/train/finaldict_new_1_20170821/dict_1.txt", 'w', "utf-8")
		path = "/opt/zhangjing/ocr/Attention-OCR-chinese-version/word_label.txt"
		
		with codecs.open(path, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:# and n<20:
					#s = " ".join(lst)
					fw.write(lst[0] + "\n")

	def arrange_plyFile(self):
		fw =  open("/opt/zhangjing/ocr/Attention-OCR-chinese-version/idioms/data.ply", 'w')
		
		for dirpath, dirnames, filenames in os.walk('/opt/zhangjing/ocr/Attention-OCR-chinese-version/idioms/data'):
			for filename in filenames:
				s = "/opt/zhangjing/ocr/Attention-OCR-chinese-version/idioms/data/" + filename
				print s
				if os.path.exists(s):
					'''print s
					os.remove(s)'''
					with codecs.open(s, 'rb', "utf-8") as ann_file:
						lines = ann_file.readlines()
						n = 0
						for l in lines:
							lst = l.strip().split() 
							if len(lst) > 1:# and n<20:
								n = n + 1
								if n > 9: 
									ss = " ".join(lst)
									fw.write(ss + "\n")
										
	def write_txt_1(self):
		fw =  open("/opt/zhangjing/ocr/svm/datasets/train/att_2_10_20170828/label.txt", 'w')
		
		for dirpath, dirnames, filenames in os.walk('/opt/zhangjing/ocr/svm/datasets/train/att_2_10_20170828/img'):
			for filename in filenames:
				l = filename[len(filename)-4:]
				print l
				if l == ".jpg":
					fw.write(filename + " " + "1" + "\n")
		
	def process_xml(self):
		dst_path = "/opt/zhangjing/ocr/error_analysis/process/labels1/"
		
		src_path = "/opt/zhangjing/ocr/error_analysis/process/labels/"
		for dirpath, dirnames, filenames in os.walk( src_path ):
			for filename in filenames:
				ll = filename[len(filename)-4:]
				print ll
				if ll == ".xml":
					xml_path = src_path + filename
					if os.path.isfile(xml_path):
						s = dst_path + filename
						fw =  open(s, 'w')
						with codecs.open(xml_path, 'r') as ann_file:
							lines = ann_file.readlines()
							for l in lines:
								lst = l.strip()
								lst1 = lst[:10]
								if lst1 !="<filename>":
									fw.write(l)# + "\n")
	
	def separate_0and1(self):
		fw_0 =  open("/opt/zhangjing/ocr/svm/datasets/train/att_2_10_20170828/img/label0.txt", 'w')
		fw_1 =  open("/opt/zhangjing/ocr/svm/datasets/train/att_2_10_20170828/img/label1.txt", 'w')
		with codecs.open("/opt/zhangjing/ocr/svm/datasets/train/att_2_10_20170828/label_all.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:# and n<20:
					s = " ".join(lst)
					if lst[1]=="0":
						fw_0.write(s + "\n")
					elif lst[1]=="1":
						fw_1.write(s + "\n")
		
	def resize(self):
		path_dst = '/opt/ligang/data/icdar2017rctw/train-word_64*200/'
		path_src = '/opt/ligang/data/icdar2017rctw/train-word/'
		for dirpath, dirnames, filenames in os.walk(path_src):
			for filename in filenames:
				if filename.endswith('.jpg'):
					s = path_src + filename
					#img = Image.open(image_path)
					img = cv2.imread(s)#image_path)
					if img != None:
						#fw.write(image_path)
						img = cv2.resize(img, (200, 64))#img.resize((100, 32),Image.ANTIALIAS)	#	Image.BILINEAR) 
			
						'''img_bw = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
						img_bw = np.asarray(img_bw, dtype=np.uint8)
						img_bw = img_bw[np.newaxis, :]'''

						s = path_dst + filename
						print s
						cv2.imwrite(s, img)
	
	def process1(self):
		path_dst = '/opt/ligang/data/icdar2017rctw/augmented_dataset/other/label_new.txt'
		path_src = '/opt/ligang/data/icdar2017rctw/augmented_dataset/other/label.txt'
		path_src1 = '/opt/ligang/data/icdar2017rctw/WordBBText_chinese.txt'
		
		fw =  codecs.open(path_dst, 'w', "utf-8")
		
		imgs = []
		words = []
		with codecs.open(path_src1, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:# and n<20:
					ll = lst[0]
					ll = ll[:len(ll)-4]
					imgs.append(ll)
					words.append(lst[1])
		
		dict1 = dict(zip(imgs,words))
		#print dict1
				
		with codecs.open(path_src, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split("_") 
				lst1 = []
				if len(lst) > 3:# and n<20:
					lst1 = lst[:3]
					#print lst1
					s = "_".join(lst1)
					#print s
					word = dict1[s]
					#print dict1[s]
					fw.write(l.strip() + " " + word + "\n")
					#break
					
					
	def process2(self):
		path_dst = '/opt/ligang/data/MSRA-TD500/crop_square/label_new.txt'
		path_src = '/opt/ligang/data/MSRA-TD500/crop_square/label.txt'
		
		fw =  codecs.open(path_dst, 'w', "utf-8")
		
		imgs = []
		words = []
		with codecs.open(path_src, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if 3 >len(lst) > 1:# and n<20:
					fw.write(l)
					
					
		'''
			#print "\n"
			for ll in lex:
				if ll in words:
					c = ll.encode("raw_unicode_escape")
					#print ll.encode("utf-8")  #.encode("raw_unicode_escape")
					if c.find("\u", 0) > -1:
						#print ll.encode("raw_unicode_escape")
						label = words.index(ll)
						#print label
						if label > -1:
							n = 1
							#print label
							#print labels[label]
					elif 96 < ord(ll) < 123 or 47 < ord(ll) < 58:
						#print ("ord(ll):{}".format(ord(ll)))
						label = words.index(ll)
						if label > -1:
							n = 2
							#print label
							#print labels[label]
		'''
			
		'''
			#print len(lex)
			lex1 = lex.encode("utf-8")
			#print lex1
			lst = []			
			for ll in lex:
				i = ll.encode("raw_unicode_escape")
				#print i
				if i.find("\u", 0) > -1:
					
					c = int(i[2:],16)
					#print ("c:{}".format(c) )
					c = hex(c)
					c = c[2:]
					c = "\u" + c
					#print c.decode("raw_unicode_escape").encode("utf-8")	
					lst.append ( c.decode("raw_unicode_escape").encode("utf-8")	 )
					
			s = "".join(lst)  
			#print s		
			#print ll.decode("raw_unicode_escape").encode("utf-8")
		'''
if __name__ == '__main__':
	inputpath = r'/opt/zhangjing/ocr/Attention-OCR-new-version/result/imcorrect.txt'
	outputpath = r'/opt/zhangjing/ocr/Attention-OCR-new-version/result/word_imcorrect_num.txt'
	c = chinese_process(inputpath, outputpath)
	#res = c.get_correctWord_num()
	#res = c.get_precision()  #按字统计的准确率，（字，正确数，错误数，总数， 正确率， class_time统计的个数）
	#res = c.get_word_precision() #按词统计的准确率 （词， 正确数， 错误数， 总数, 正确率, 该词样本个数）
	#res = c.draw_precision("/opt/zhangjing/ocr/Attention-OCR-new-version/result/word_precision.txt")		
	#res = c.get_incorrect_image() #获得识别错误的图片
	#res = c.get_letter_times() #统计测试数据集每个字符的个数
	#res = c.get_word_times()  #统计测试数据集每个word/label的样本个数
	#res = c.get_folder_filename() #获得文件夹图片路径并保存、打label
	#res = c.get_train_test_data()  #从总的txt中分出训练、测试样本，分别保存在train、test文件夹下面，并将图片路径、label写到相应的文件中。
	#res = c.get_train_test_txt()  #从总的txt中分出训练、测试样本，分别获得train.txt、test.txt
	#res = c.get_image_label()  #给图片打固定的label
	#res = c.compare_data()  
	#res = c.get_equal_sample() #只取合成数据集中类别数满足2033个。
	#res = c.test() #将原图转成32*100
	#res = c.remove_some_sample() 
	#res = c.remove_letter_less()
	#res = c.get_idioms_explain()#获得成语以及成语的解释
	#res = c.get_idioms_label()
	#res = c.copy_data()
	#res = c.test_data() #根据txt,生产字+字 或 词+词的随机组合数据
	#res = c.judge_is_study() #判断测试词是否之前学过，如果学过后面加1，否则加0.
	#res = c.test_sample() #从大样本的文件夹中取一些词长度为7的样本，另存
	#res = c.test_result()  #测试识别结果中正确识别的词的长度分布
	#res = c.test_sample1() #寻找识别率不高的原因，将测试图片压缩成32*100，并且图片重新命名成isOK_isTrain_imageName
	#res = c.test_random_shuffle()
	#res = c.remove_sample1() #
	#res = c.test2() 
	#res = c.remove_sample2() 
	#res = c.add_sample() 
	#res = c.random_sample()  #从每个词5个样本中随机取一个
	#res = c.get_imageAbsPath() #获得训练图片的全路径                                 !!!!!!!!!!!!!!!!!!!!!
	#res = c.get_add_txt() #将2个txt 合成一个，因为有汉字，快捷方式的合成会出现问题
	#res = c.delete_col() #只保存一列
	#res = c.arrange_plyFile()
	#res = c.write_txt_1() #将图片的label统一写成违建（1）
	res = c.process_xml()  #过滤xml中的乱码（因为图片路径中含有汉字导致的乱码）
	#res = c.separate_0and1() #从整个txt中分出违建1与非违建0的类别
	#res = c.resize()
	#res = c.process1() # 根据（image_0_3.jpg 城建店) 给image_0_3_noise0.02.jpg在标签
	#res = c.process2()