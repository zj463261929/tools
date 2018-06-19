#__author__ = 'lg 2018-3-14'


import numpy as np
import os
import json
import cv2


def store(data,name):
    with open(name, 'w') as json_file:
        json_file.write(json.dumps(data))

def load(name):
    with open(name) as json_file:
        data = json.load(json_file)
        return data

def caculate_area(x,y):
    flag = 0
    if len(x) != len(y):
        flag = -1
        return flag,None
    if len(x) < 3:
        flag = -2
        return flag,None
    x.append(x[0])
    y.append(y[0])
    s = 0
    #print x
    #print y
    for k in range(len(x)-1):
        a=x[k]*y[k+1]-x[k+1]*y[k]
        s=s+a
    S = s/2
    if S < 0:
        s = 0
        for k in range(len(x)-1):
            a=y[k]*x[k+1]-y[k+1]*x[k]
            s=s+a
        S = s/2
    S = float('%.2f' % S)        
    return flag ,S
    
    
def segmentation(fn,cat_single_dict,annotations_id,width,height):
    annotations_dict = {}
    
    if (cat_single_dict['label'] == 'front' or cat_single_dict['label'] == 'side' or cat_single_dict['label'] == 'back') is not True:
        print ('filename is {}'.format(fn))
        print ('label is {}'.format(cat_single_dict['label']))
        return -4,None
    
    points_list = cat_single_dict['points']
    
    # add segmentation
    x = []
    y = []
    seg_list = []
    seg_cat_list = []
    for j in range(len(points_list)):
        if len(points_list[j]) != 2:
            print ('filename is {}'.format(fn))
            print ('shapes num is {}'.format(i))
            print ('points num is {}'.format(j))
            print ('the points is wrong!!!')
            return -1,None
        temp_x = float('%.2f' % points_list[j][0])
        temp_y = float('%.2f' % points_list[j][1])
        x.append(temp_x)
        y.append(temp_y)
        seg_cat_list.append(temp_x)
        seg_cat_list.append(temp_y)
    seg_list.append(seg_cat_list)
    annotations_dict['segmentation'] = seg_list
    
    # add image_id
    n = len(fn)
    annotations_dict['image_id'] = fn[0:n-5]
    
    # add category_id
    cat_num = 0
    if 'front' == cat_single_dict['label']:
        cat_num = 1
    if 'side' == cat_single_dict['label']:
        cat_num = 2
    if 'back' == cat_single_dict['label']:
        cat_num = 3
    annotations_dict['category_id'] = cat_num
    
    # add bbox
    bbox_list = []
    bbox_list.append(max((min(x) - 0.0*(max(x) - min(x))),0))
    bbox_list.append(max((min(y) - 0.0*(max(y) - min(y))),0))
    bbox_list.append(float('%.2f' % (min(width,(max(x) - min(x)) * 1.0))))
    bbox_list.append(float('%.2f' % (min(height,(max(y) - min(y)) * 1.0))))
    annotations_dict['bbox'] = bbox_list
    
    # add area
    flag,S = caculate_area(x,y)
    if flag < 0:
        if flag == -1:
            print 'the num of x and y are not same!!!'
            return -2,None
        if flag == -2:
            print 'the num of x and y are less than 3!!!'
            return -3,None
    annotations_dict['area'] = S
    
    # add id
    annotations_dict['id'] = annotations_id
    # add iscrowd ignore
    annotations_dict['iscrowd'] = 0
    annotations_dict['ignore'] = 0
    return 0,annotations_dict
    
def image(fn,fullfilename):
    I = cv2.imread(fullfilename)
    n = len(fn)
    images_dict = {}
    images_dict['id'] = fn[0:n-4]
    images_dict['file_name'] = fn
    images_dict['width'] = I.shape[1]
    images_dict['height'] = I.shape[0]
    return images_dict
    
def main():
    data_path = './body_front_side_back/results/benchmark'
    out_path = './body_front_side_back/results'
    out_name = 'instances_body_minival.json'
    out_dict = {}
    out_dict['images'] = []
    out_dict['annotations'] = []
    
    #add 
    out_dict['type'] = 'instances'
    #add categories
    out_dict['categories'] = [
        {"supercategory":"none","id":1,"name":"front"},
        {"supercategory":"none","id":2,"name":"side"},
        {"supercategory":"none","id":3,"name":"back"}]

    
    # add images
    # add annotations
    images_list = []
    annotations_list = []
    annotations_id = 0
    if os.path.exists(data_path):
        if os.path.isdir(data_path):
            filenames = os.listdir(data_path)
            #print filenames
            num = len(filenames)
            if num % 2 != 0:
                print 'the num of image and json are not same!!!'
                return 
            for fn in filenames:
                fullfilename = os.path.join(data_path,fn)
                if os.path.isfile(fullfilename):
                    if fn.endswith('.jpg'):
                        images_dict = {}
                        images_dict = image(fn,fullfilename)
                        images_list.append(images_dict)
                    #print('wwwwwwwwwwwwwwwwwwwwwww',width)
                    #print('hhhhhhhhhhhhhhhhhhhhhhh',height)
                    if fn.endswith('.json'):
                        single_img_dic = load(fullfilename)
                        seg_num_list = single_img_dic['shapes']
                        #width = 0#temp_I.shape[1]
                        #height = 0#temp_I.shape[0]
                        n = len(fullfilename)
                        imagepath = fullfilename[0:n-5]
                        imagepath = imagepath + '.jpg'
                        print imagepath
                        temp_I = cv2.imread(imagepath)
                        width = temp_I.shape[1]
                        height = temp_I.shape[0]
                        print width
                        print height
                        for i in range(len(seg_num_list)):
                            annotations_dict = {}
                            cat_single_dict = seg_num_list[i]
                            flag,annotations_dict = segmentation(fn,cat_single_dict,annotations_id,width,height)
                            if flag < 0:
                                return
                            annotations_list.append(annotations_dict)
                            annotations_id = annotations_id + 1
            out_dict['images'] = images_list
            out_dict['annotations'] = annotations_list
    else:
        print '{} is not exist'.format(data_path)
        
    # save
    out_json = os.path.join(out_path,out_name)
    store(out_dict,out_json)
if __name__ == '__main__':
    main()
    