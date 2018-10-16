import os
import random

from os import path

SPLIT_RATIOS=974
train_image_dir="/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/ImageSets/Main/train_org.txt"
val_image_dir="/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/ImageSets/Main/val_org.txt"
orig_image_dir="/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations" #JPEGImages"

train = open(train_image_dir,'w+')
val = open(val_image_dir,'w+')
files = [x for x in os.listdir(orig_image_dir) if path.isfile(orig_image_dir+os.sep+x) and x.endswith('.xml')]
random.shuffle(files)
random.shuffle(files)
#print files
print("org total image num:",len(files))

for i in xrange(len(files)): 
    file=files[i]
    #print file     
    basename = os.path.splitext(file)[0]
    #result = 'pictures'+os.sep+file+' '+ 'labels'+os.sep+basename+'.xml\n'
    result = basename+'\n'
    if (i% 1000) > SPLIT_RATIOS:
        val.write(result)
    else:
        train.write(result)
train.close()
val.close()        

benchmark1_dir="/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/benchmark_day_49.txt"
benchmark1 = open(benchmark1_dir,'rb')
benchmark1_files = benchmark1.readlines()
print("benchmark1 image num:",len(benchmark1_files))

'''benchmark2_dir="/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/benchmark_new.txt"
benchmark2 = open(benchmark2_dir,'rb')
benchmark2_files = benchmark2.readlines()
print("benchmark2 image num:",len(benchmark2_files))'''


train = open(train_image_dir,'rb')
train_files = train.readlines()
print("train image num:",len(train_files))

train_image_new_dir="/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/ImageSets/Main/train.txt"
train_new = open(train_image_new_dir,'w+')

num=0
for i in xrange(len(train_files)):    
    file = train_files[i]
    basename = os.path.splitext(file)[0]
    same_flag = False
    for ii in xrange(len(benchmark1_files)):
        benchmark1_name = benchmark1_files[ii].strip()
        if benchmark1_name in basename:
                num = num + 1
                same_flag = True
                #os.remove(path.join(image_dir,file))
                break
    '''if  same_flag==False:
        for jj in xrange(len(benchmark2_files)):
            benchmark2_name = benchmark2_files[jj].strip()
            if benchmark2_name in basename:
                    num = num + 1
                    same_flag = True
                    #os.remove(path.join(image_dir,file))
                    break'''

    if same_flag==False:
        train_name = str(basename)
        #print(train_name)
        train_new.write(train_name)
            
print("train img(benchmark and blur related) num:",num)
train_new.close()
train_new = open(train_image_new_dir,'rb')
train_files = train_new.readlines()
print("final train img num:",len(train_files))

#train_val dataset
trainval_image_dir="/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/ImageSets/Main/trainval.txt"
train_val = open(trainval_image_dir,'w+')

num=0
trainvalnum=0
for i in xrange(len(train_files)):    
    file = train_files[i]
    basename = os.path.splitext(file)[0]
    same_flag = False
    num = num+1
    if (num% 1000) > SPLIT_RATIOS:         
        train_val.write(basename)
        trainvalnum = trainvalnum+1
print("final trainval img num:",trainvalnum)            

#####val dateset
val = open(val_image_dir,'rb')
val_files = val.readlines()
print("val image num:",len(val_files))

val_image_new_dir="/opt/zhangjing/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/ImageSets/Main/val.txt"
val_new = open(val_image_new_dir,'w+')

num=0
for i in xrange(len(val_files)):    
    file = val_files[i]
    basename = os.path.splitext(file)[0]
    same_flag = False
    for ii in xrange(len(benchmark1_files)):
        benchmark1_name = benchmark1_files[ii].strip()
        if benchmark1_name in basename:
                num = num + 1
                same_flag = True
                #os.remove(path.join(image_dir,file))
                break
    '''if  same_flag==False:
        for jj in xrange(len(benchmark2_files)):
            benchmark2_name = benchmark2_files[jj].strip()
            if benchmark2_name in basename:
                    num = num + 1
                    same_flag = True
                    #os.remove(path.join(image_dir,file))
                    break'''                    

    if same_flag==False:
        val_name = str(basename)
        #print(train_name)
        val_new.write(val_name)
            
print("val img(benchmark related) num:",num)
val_new.close()
val_new = open(val_image_new_dir,'rb')
val_files = val_new.readlines()
print("final val img num:",len(val_files))



