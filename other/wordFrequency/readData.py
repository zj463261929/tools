#coding=utf-8
import jieba 
from collections import Counter
import codecs
import random
import numpy as np

stopword_path = r'stopwords.dat'
class seg_word(object):
	def __init__(self, inputpath, outputpath):
		self.inputpath = inputpath
		self.outputpath = outputpath

	def cut_data(self):
		with codecs.open(inputpath, 'r', 'utf-8') as fr:
			res = jieba.cut(fr.read())
		return res

	def output_file(self):
		outcome = self.cumpute_word_count()
		with codecs.open(outputpath, 'w', 'utf-8') as fw:
			for k,v in outcome.items():
				fw.write(k +  + '\n')#' ' + str(v) + '\n')

	def filter_data(self):
		with codecs.open(stopword_path,'r','utf-8') as f:
			stopword_list = f.read()
		seg_res = self.cut_data()
		res_list = [word.strip() for word in seg_res if word not in stopword_list] #strip() 方法用于移除字符串头尾指定的字符（默认为空格）。
		return res_list

	def cumpute_word_count(self):
		res_word = self.filter_data()
		word_freq = dict(Counter(res_word))
		return word_freq
	
	def get_cut_data(self):
		with codecs.open(stopword_path,'r','utf-8') as f:
			stopword_list = f.read()
		seg_res = self.cut_data()
		res_list = [word.strip() for word in seg_res if word not in stopword_list] #strip() 方法用于移除字符串头尾指定的字符（默认为空格）。
		
		with codecs.open(outputpath, 'w', 'utf-8') as fw:
			n = 0
			for i in range(len(res_list)):
				if n%20 == 0:
					fw.write(res_list[i] + " " + '\n')
				else:
					fw.write(res_list[i] + " ")
				n = n + 1
						
	def is_chinese(self, uchar): #判断一个unicode是否是汉字	例如：uchar = \u4e00
		if uchar.find("\u", 0) > -1:
			#print "chinese"
			uchar = uchar[2:] #4e00
			#print uchar
			uchar = int(uchar,16) #转成10进制，4e00->19968	9fa5->40869
			if uchar >= 19968 and uchar<=40869:#if uchar >= u'\u4e00' and uchar<=u'\u9fa5':		
				return True
			else:
				return False
				
	def is_alphabet(self, uchar):#判断一个unicode是否是英文字母"""	
		if not uchar.find("\u", 0) > -1:
			if (uchar>="a" and uchar<="z") or (uchar>="A" and uchar<="Z"):#(uchar>=65 and uchar<=90) or (uchar>=97 and uchar<=122): #(uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
				#print uchar.lower()
				return True
			else:
				return False

	def is_number(self, uchar):#判断一个unicode是否是数字"""  
		if not uchar.find("\u", 0) > -1:
			#print ("uchar:{}".format(uchar))
			#print type(uchar) #str
			if uchar>=str(0) and uchar<=str(9): 
				return True
			else:
				return False
				
	def is_other(self, uchar):#判断是否非汉字，数字和英文字符"""	  
		if not (self.is_chinese(uchar) or self.is_number(uchar) or self.is_alphabet(uchar)):
			
			return True
		else:
			return False
			
	def cut_word(self):
		outcome = self.cumpute_word_count()
		lst = []
		with codecs.open(outputpath, 'w', 'utf-8') as fw:
			n = 3
			for c in range(10): #写数字0-9
				fw.write(str(c) + ' ' + str(n) + '\n')
				n = n + 1
			
			for c in range(26): #写字母a-z
				c = c + 97	#97->a	122->z
				fw.write(chr(c) + ' ' + str(n) + '\n')
				n = n + 1
				
			for k,v in outcome.items():
				for c in k:
					lst.append(c)
					
			lst = list(set(lst))#list(set(lst)) 去除列表中重复的元素
			for c in lst: 
				cc = c.encode("raw_unicode_escape")
				#print "\n"
				#print cc
				if self.is_chinese(cc):
					fw.write(c + ' ' + str(n) + '\n')
					n = n + 1
			print ("dict count:{}\n".format(n))
			
	def unified_symbol(self, uchar):#中英文符号统一转成中文符号,前提该字符本身就是符号（标点符号等）
		if not uchar.find("\u", 0) > -1: 
			s = str(hex(ord(uchar) + 65248)) #65248->0xfee0 
			print "11111"
			#print s
			lst = list(s)
			lst = lst[2:]
			#print lst
			s = "\u" + "".join(lst)
			print "1111112"
			print s
			return s.decode('unicode_escape')
		else:
			return uchar.decode('unicode_escape')
		'''if uchar.find("\u", 0) > -1: #中文输入法输入的符号, （》\u300b，12299会报错）
			uchar = uchar[2:] #4e00
			#print uchar
			uchar = int(uchar,16)
			uchar = uchar - 65248
			return chr(uchar)
		else: #英文输入法输入的符号
			#print "11111"
			return uchar #ord(uchar)'''
			
	def cut_word_all(self):
		words = []
		with codecs.open("/opt/ligang/data/MSRA-TD500/crop_square/label_new_new_icdar.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					for c in lst[1]:
						words.append(c)
						#print (c.encode("utf-8")) 

		#print len(words)
		lst = list(set(words)) #去重复的
		#print len(lst)

		#lst.sort()
		#print (len(lst))
		fw =  codecs.open("/opt/ligang/data/MSRA-TD500/crop_square/label_new_new_icdar_letter.txt", 'w', "utf-8")
		n = 3
		lst_chinese = []
		lst_alphabet = []
		lst_number = []
		lst_other = []
		for c in lst: 
			cc = c.encode("raw_unicode_escape")
			#print "nnnnnnnnnnnn"
			#print (c.encode("utf-8")) 
			#print ord(c)
			#
			#print cc #如果是英文对应的是字符串，中文对应的是\u300b
			#print "22222222222"
			if self.is_chinese(cc):
				lst_chinese.append(c)
			elif self.is_alphabet(cc):
				lst_alphabet.append(c.lower()) #大小写全转成小写
			elif self.is_number(cc):
				lst_number.append(c)
			elif self.is_other(cc):
				continue
				#c_other = self.unified_symbol(cc)
				#lst_other.append(c) #中英文符号统一转成英文符号
		
		
		lst_alphabet = list(set(lst_alphabet)) 	
		lst_other = list(set(lst_other)) 		
		print ("n_chinese:{}".format(len(lst_chinese)))	
		print ("n_alphabet:{}".format(len(lst_alphabet)))	
		print ("n_number:{}".format(len(lst_number)))
		print ("n_other:{}".format(len(lst_other)))	
		
		for c in lst_number:
			fw.write(c + ' ' + str(n) + '\n')
			n = n + 1
		for c in lst_alphabet:
			fw.write(c + ' ' + str(n) + '\n')
			n = n + 1
		for c in lst_other:
			fw.write(c + ' ' + str(n) + '\n')
			n = n + 1
		for c in lst_chinese:
			fw.write(c + ' ' + str(n) + '\n')
			n = n + 1
			
		print ("dict count:{}\n".format(n))	
						
	def cut_word_new(self):
		words = []
		with codecs.open("/opt/ligang/data/pic2000_15_data_2017_5_31/result_img_word/WordBBText_new.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					for c in lst[1]:
						words.append(c)
					
		lst = list(set(words)) #去重复的
		#lst.sort()
		#print (len(lst))
		fw =  codecs.open("/opt/ligang/data/pic2000_15_data_2017_5_31/result_img_word/word_label_new1.txt", 'w', "utf-8")
		c_words = []
		n = 3
		for c in range(10): #写数字0-9
			fw.write(str(c) + ' ' + str(n) + '\n')
			n = n + 1
			
		for c in range(26): #写字母a-z
			c = c + 97	#97->a	122->z
			fw.write(chr(c) + ' ' + str(n) + '\n')
			n = n + 1
				
			
		for c in lst: 
			cc = c.encode("raw_unicode_escape")
			#print "\n"
			#print cc
			if self.is_chinese(cc):
				fw.write(c + ' ' + str(n) + '\n')
				n = n + 1
		print ("dict count:{}\n".format(n))	
	

	def cut_word_new_new(self):
		words = []
		#with codecs.open("/opt/yangmiao/synthdata/synthdata_900/train_label_dict_5+10.txt", 'rb', "utf-8") as ann_file:
		with codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText_chinese.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					for c in lst[1]:
						words.append(c)
					
		lst = list(set(words)) #去重复的
		#lst.sort()
		#print (len(lst))
		#fw =  codecs.open("/opt/yangmiao/synthdata/synthdata_900/word_label_5+10.txt", 'w', "utf-8")
		fw =  codecs.open("/opt/ligang/data/icdar2017rctw/word_label_chinese.txt", 'w', "utf-8")
		c_words = []
		n = 3
				
		for c in lst: 
			cc = c.encode("raw_unicode_escape")
			#print "\n"
			#print cc
			if self.is_chinese(cc):
				fw.write(c + ' ' + str(n) + '\n')
				n = n + 1
			else :
				fw.write(c.lower() + ' ' + str(n) + '\n')
				n = n + 1
		print ("dict count:{}\n".format(n))	
		
	def get_label_num(self):
		n = 0
		fw =  codecs.open("/opt/yangmiao/synthdata/finaldict_new_test.txt", 'w', "utf-8")
		with codecs.open("/opt/yangmiao/synthdata/finaldict_new.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 0:
					n = len(lst[0])
					if n<10:
						s =" ".join(lst)
						fw.write(s + "\n")
		fw.close()
		
		'''
		num = [0]*50
		with codecs.open("/opt/yangmiao/synthdata/finaldict_new.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 0:
					n = len(lst[0])
					num[n] = num[n] + 1
					
					if len(lst[0])>32:
						for c in lst[0]:
							print c.encode("utf-8")
						print "\n"
						n = n + 1
		#print n
		for i in range(50):
			print (i, num[i])
		'''

					
	def remove_word(self):
		words = []
		with codecs.open("/opt/ligang/data/MSRA-TD500/crop_square/label.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					words.append(lst[1])
					
		lst = list(set(words)) #去重复的
		#lst.sort()
		#print (len(lst))
		fw =  codecs.open("/opt/ligang/data/MSRA-TD500/crop_square/label_word.txt", 'w', "utf-8")
		for l in lst:
			lst1 = l.strip().split() 
			s = " ".join(lst1)
			fw.write(s + '\n')
			
		fw.close()
		
	def filter_sample(self):
		letters = []
		with codecs.open("/opt/zhangjing/ocr/attention_ocr/attention_ocr_64/word_label.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					for c in lst[1]:
						letters.append(c)
		print len(letters)
						
		fw = codecs.open("/opt/ligang/data/MSRA-TD500/crop_square/label_icdar.txt", 'w', "utf-8")
		n = -1
		with codecs.open("/opt/ligang/data/MSRA-TD500/crop_square/label.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			for l in lines:
				lst = l.strip().split()
				n = -1
				if len(lst) > 1:
					for c in lst[1]:
						if c not in letters:
							n = n + 1
				if n < 0:
					s = " ".join(lst)
					fw.write(s + "\n")
					print "1111111"
					
		fw.close()				
		
						
	def filter_sample_letter(self):
		letters = []
		with codecs.open("/opt/zhangjing/ocr/attention_ocr/attention_ocr_32/word_label.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					letters.append(lst[0])
					#print (lst[0].encode("utf-8"))
		print len(letters)
						
		fw = codecs.open("/opt/ligang/data/MSRA-TD500/crop_square/label_new_new_icdar.txt", 'w', "utf-8")
		n = -1
		with codecs.open("/opt/ligang/data/MSRA-TD500/crop_square/label_new_new.txt", 'rb', "utf-8") as ann_file1:
			lines = ann_file1.readlines()
			for l in lines:
				lst = l.strip().split()
				n = -1
				if len(lst) > 1:
					for c in lst[1]:
						if c not in letters:
							n = n + 1
				if n < 0:
					s = " ".join(lst)
					fw.write(s + "\n")
					#print "1111111"
					
		fw.close()				
		
		
	def get_english_word(self):

		fw =  codecs.open("/opt/ligang/data/pic2000_15_data_2017_5_31/result_img_word/WordBBText_english.txt", 'w', "utf-8")
		with codecs.open("/opt/ligang/data/pic2000_15_data_2017_5_31/result_img_word/WordBBText.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				word = []
				n = 0
				if len(lst) > 1:
					for c in lst[1]:
						cc = c.encode("raw_unicode_escape")
						#print "\n"
						#print cc
						if self.is_chinese(cc):
							n = -1
						else:
							if 96 < ord(c) < 123:
								word.append( c.lower() )
							else:
								n = -1
				if n > -1:
					s = "".join(word)
					fw.write(lst[0] + " " + s + '\n')
		fw.close()
	
	def get_chinese_word(self):

		fw =  codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText_new_new.txt", 'w', "utf-8")
		with codecs.open("/opt/ligang/data/icdar2017rctw/WordBBText_new.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				word_only = []
				n = 0
				other = 0
				if len(lst) > 1:
					for c in lst[1]:
						cc = c.encode("raw_unicode_escape")
						#print "\n"
						#print cc
						if self.is_chinese(cc) or self.is_number(cc):
							n = n + 1
							word_only.append(c)
						elif self.is_alphabet(cc):
							n = n + 1
							word_only.append(c.lower())
						else:
							other = -1	#表示文本中还含除中文、数字、英文外其它符号
	
				if n>0 and other>-1:
					s = "".join(word_only)
					fw.write(lst[0] + " " + s + '\n')
				elif n>0 and other<0:
					s = "".join(word_only)
					fw.write(lst[0] + " " + s + " " + lst[1] + '\n')
					
				#break
		fw.close()
	
	def get_random_file(self):
		fw =  codecs.open("/opt/ligang/data/pic2000_data_2017_6_15/train.txt", 'w', "utf-8")
		with codecs.open("/opt/ligang/data/pic2000_data_2017_6_15/train1.txt", 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			random.shuffle(lines)
			for l in lines:
				fw.write(l)
		fw.close()
			
			
	def val_word(self):
		lst = []
		with codecs.open(outputpath, 'r', 'utf-8') as fr:
			lines = fr.readlines()
			for l in lines:
				word, index1 = l.strip().split() 
				lst.append(word)
		n = 0
		for c in lst:
			if lst.count(c)>1:
				n = n + 1
				
		print ("repeat word num:{}\n".format(n-1-3))
		
	
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
				if len(lst) > 2:# and n<20:
					s = lst[0] +  " " + lst[2] + " " + lst[1]
					fw.write(s + "\n")	
				else:
					fw.write(l)
	
	def statistics_sample_word(self):
		path_src = '/opt/ligang/data/MSRA-TD500/crop_square/label_new_new_icdar.txt'#'/opt/ligang/data/icdar2017rctw/WordBBText_new_new.txt'
		path_dst = '/opt/ligang/data/MSRA-TD500/crop_square/label_new_new_icdar_wordLength.txt'#'/opt/ligang/data/icdar2017rctw/WordBBText_new_new_wordLength.txt'
			
		fw =  codecs.open(path_dst, 'w', "utf-8")
		letter_len= 31 #词中字符的最大个数
		num = np.zeros((letter_len))
		words = []
		with codecs.open(path_src, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:# and n<20:
					words.append( lst[1] )
					
		print ("样本总个数：%d" % (len(words)))
		lst = list(set(words))#list(set(lst)) 去除列表中重复的元素
		print ("词的个数：%d" % (len(lst)))
		
		#统计词中字符的个数分布
		for i in range(len(lst)):
			n = len(lst[i])
			if n < letter_len:
				num[n] = num[n] + 1

		for i in range(letter_len):
			fw.write(str(i) + " " + str(int(num[i])) + "\n")
		fw.close()
		
		letter = []
		#统计样本中类别的个数
		for i in range(len(lst)):
			for c in lst[i]:
				letter.append( c )
				
		letter1 = list(set(letter))
		print ("类别(字符)个数：%d" % (len(letter1)))
		
	def analysis_sample_word(self):
		path_train = '/opt/ligang/data/icdar2017rctw/WordBBText_new_new.txt'
		path_test = '/opt/ligang/data/MSRA-TD500/crop_square/label_new_new_icdar.txt'
			
		words = []
		with codecs.open(path_train, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					words.append( lst[1] )
					
		words = list(set(words))#list(set(lst)) 去除列表中重复的元素
		print ("训练集中词的个数：%d" % (len(words)))
		
		n = 0
		tests = []
		with codecs.open(path_test, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				lst = l.strip().split() 
				if len(lst) > 1:
					tests.append( lst[1] )
		
		tests = list(set(tests))	
		for i in range(len(tests)):
			if tests[i] in words:
				n = n + 1
		print ("测试集中词的个数：%d" % (len(tests)))
		print ("测试集中词在训练集中的个数：%d %.2f" % (n, n/(len(tests)+0.0)))
		
					
			
	
if __name__ == '__main__':
	inputpath = r'newsgroup.txt'
	outputpath = r'dict11.txt'
	c = seg_word(inputpath, outputpath)
	#res = c.output_file() #从语料库txt中分词及统计词频
	#res = c.get_cut_data() #从语料库txt中 只分词，每行存储20个词
	#res = c.cut_word() #从语料库中，切分成一个个字，去重，加label(从3开始)
	#res = c.cut_word_new() #从样本集的文档中对单个字重新进行编码，label(从3开始)
	#res = c.cut_word_new_new() #从样本集的txt中对单个字重新进行编码，label(从3开始) 111111111111111111111111
	#res = c.cut_word_all() #从样本集的txt中对单个字（中文、英文、数字、符号（有点问题）等）重新进行编码，label(从3开始) 111111111111111111111111
	#res = c.val_word() #验证word_label.txt中字是否有重复
	#res = c.get_english_word()	 #从样本集的文档中只获得全英文的样本 
	#res = c.get_chinese_word() #从样本集的txt中获得含有中文、英文、数字的样本，比如：image_2265_8.jpg （各种汤类）-> image_2265_8.jpg 各种汤类 （各种汤类）
	#res = c.get_random_file()	#将txt文件的行重新打乱
	#res = c.filter_sample() #过滤掉字不在某个文件中的样本
	#res = c.filter_sample_letter() #过滤掉字不在某个文件中的样本,根据word_label.txt,过滤掉不存在的词
	#res = c.remove_word() #去除重复的词				 1111111111111111
	#res = c.get_label_num() #查看180万词中词长度超过32的
	#res = c.process2()  #将第三列的标签与第二列的标签互换
	#res = c.statistics_sample_word() #统计文本识别训练集的情况：如词的长度分布、总样本个数、词的个数
	res = c.analysis_sample_word() #分析测试集，主要是统计测试集中有多少个词是在训练集中