#coding = UTF-8
import cv2
import os
import numpy as np

output = "DJI_0001" #'/data/zhangjing/ruike/handvideoDataset/1460'
if not os.path.exists(output):
	os.mkdir(output)
vc = cv2.VideoCapture('/opt/zhangjing/Detectron/data/videoData/DJI_0001.MOV')
		
c = 1
if vc.isOpened():
	rval,frame = vc.read()
else:
	rval = False
timeF = 30
print ("rval = ", rval)

isResize = True 
while rval:
	rval,frame = vc.read()
	print (c)
	if(c%timeF == 0):
		s = "/opt/zhangjing/Detectron/data/videoData/" + output+'/'+output+'_'+str(c)+'.jpg'
		#frame = cv2.flip(frame, -1)
		print (frame.shape)
		if isResize:
			frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_CUBIC)	#resize(1920*1080h)
			cv2.imwrite(s, frame)
		else:
			crop_img = np.zeros((1080,1920,3))	#(h,w,3)	(960*720h*3) ->(1920*1080h*3)
			print (crop_img.shape)
			h = frame.shape[0]
			w = frame.shape[1]
			crop_img[0:h,0:w,:] = frame[:,:,:]
			cv2.imwrite(s, crop_img)
			
		print (s)
	c = c+1
	cv2.waitKey(1)
vc.release()