#coding=utf-8
import os
from os import path
import numpy as np
import  xml.dom.minidom
import shutil

merge_class_name = ["bicycle", "motorcycle", "tricycle", "car", "minibus", "suv", "bus", "minitruck", "minitruckbox", "boxtrucksmall", "smalltruck", "boxtruckbig", "autotruck", "roadroller","digger", "forklift", "mixer", "tanker", "tractor", "crane", "farmMachine"]

move_class_name =["blender", "tower", "brickspile", "sandpile", "cylinderpile", "bagpile", "boardpile"]
single_class_name = ["person"]
merge_class_name_result = 'person' #'car'

pro_orig_xml_dir = "/opt/ligang/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/xml_77669/" #xml
pro_save_xml_dir = "/opt/ligang/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations_1class_30_77610/" 

orig_xml_dir = "/opt/ligang/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/Annotations/"  #判断文件是否在该数据集中
orig_img_dir = "/opt/ligang/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/JPEGImages/" 

null_num = 0
error_num = 0
no_bbox_num = 0
filter_area = 30*30
def protectXY(x,w):
    x_new = x
    if x<1:
        x_new=1
    elif x>w-1:
        x_new=w-1
    return x_new
    
def writeNode(node, key, value):
    temp = doc.createElement(key) #'folder'
    node.appendChild(temp)
    node_text = doc.createTextNode(value) #'VOC2007'
    temp.appendChild(node_text)


if not os.path.exists(pro_save_xml_dir):
    os.mkdir(pro_save_xml_dir)

files = [x for x in os.listdir(pro_orig_xml_dir) if path.isfile(pro_orig_xml_dir+os.sep+x) and x.endswith('.xml')]

for i in xrange(len(files)): 
    file = files[i]
    basename = os.path.splitext(file)[0]
    print basename
    #print i, len(files)
            
    if os.path.exists(orig_img_dir+basename+".jpg") and os.path.exists(orig_xml_dir+basename+".xml"): #只处理该文件夹下面有的文件
        dom = xml.dom.minidom.parse(pro_orig_xml_dir+basename+".xml") #用于打开一个xml文件，并将这个文件对象dom变量。
        root = dom.documentElement #用于得到dom对象的文档元素，并把获得的对象给root
        
        #filename
        filename = str( root.getElementsByTagName("filename")[0].firstChild.data )
        #size
        width = int( root.getElementsByTagName("width")[0].firstChild.data )
        height = int( root.getElementsByTagName("height")[0].firstChild.data )
        depth = int( root.getElementsByTagName("depth")[0].firstChild.data )
        
        #print filename, width, height, depth
       
        #class name
        name_lst = []
        lst_temp = root.getElementsByTagName("name")
        for i in range(len(lst_temp)):
            temp = str (lst_temp[i].firstChild.data )
            if (temp in merge_class_name) or (temp in move_class_name) or (temp in single_class_name):
                name_lst.append( temp )
        
        name_lst_temp = []
        for i in range(len(name_lst)):
            temp = name_lst[i]
            if temp in merge_class_name:
                name_lst_temp.append(merge_class_name_result)
            if temp in single_class_name:
                name_lst_temp.append(single_class_name[0])
        
        #print name_lst
        
        #pose
        pose_lst_temp = root.getElementsByTagName("pose")
        truncated_lst_temp = root.getElementsByTagName("truncated")
        difficult_lst_temp = root.getElementsByTagName("difficult")
        occluded_lst_temp = root.getElementsByTagName("occluded")  
        
        #box
        bbox_lst = []
        xmin_lst_temp = root.getElementsByTagName("xmin")
        ymin_lst_temp = root.getElementsByTagName("ymin")
        xmax_lst_temp = root.getElementsByTagName("xmax")
        ymax_lst_temp = root.getElementsByTagName("ymax")
        for i in range(len(xmin_lst_temp)):
            x1 = int(xmin_lst_temp[i].firstChild.data)
            y1 = int(ymin_lst_temp[i].firstChild.data)
            x2 = int(xmax_lst_temp[i].firstChild.data)
            y2 = int(ymax_lst_temp[i].firstChild.data)
            area = (x2-x1+1)*(y2-y1+1)
            if area>filter_area:
                #bbox_num = bbox_num + 1
                bbox_lst.append(x1)
       
       #增强的数据 xml中没有occluded属性  #len(pose_lst_temp)==len(truncated_lst_temp)==len(difficult_lst_temp)==len(occluded_lst_temp)==
        if len(name_lst)==len(xmin_lst_temp)==len(ymin_lst_temp)==len(xmax_lst_temp)==len(ymax_lst_temp):
            print len(name_lst)
        else:
            error_num = error_num + 1
            print "error:",basename
            '''shutil.copy("/opt/ligang/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/xml_filter/"+basename+".xml" , "/opt/ligang/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/xml_filter2/"+basename+".xml" )
            shutil.copy("/opt/ligang/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/JPEGImages/"+basename+".jpg" , "/opt/ligang/Detectron/data/oil_vehicle_person_10cls/VOCdevkit2007/VOC2007/img_filter2/"+basename+".jpg" )'''
            continue
        
        if 0==len(name_lst_temp):
            null_num = null_num + 1
            print "null:",basename
            continue
         
        if len(bbox_lst)<1:
            no_bbox_num = no_bbox_num + 1
            print "no bbox:",basename
            continue
            
        ##################### write xml ##########################
        #创建dom文档
        doc = xml.dom.minidom.Document()
        #创建根节点
        root_node = doc.createElement('annotation')
        #根节点插入dom树
        doc.appendChild(root_node)
        
        #创建folder节点
        writeNode(root_node, 'folder', "VOC2007")
        writeNode(root_node, 'filename', root.getElementsByTagName("filename")[0].firstChild.data)
        
        #创建source
        source_node = doc.createElement('source')
        root_node.appendChild(source_node)
        writeNode(source_node, 'database', root.getElementsByTagName("database")[0].firstChild.data)
        writeNode(source_node, 'annotation', root.getElementsByTagName("annotation")[0].firstChild.data)
        writeNode(source_node, 'image', root.getElementsByTagName("image")[0].firstChild.data)
        writeNode(source_node, 'flickrid', root.getElementsByTagName("flickrid")[0].firstChild.data)
        
        #创建owner
        owner_node = doc.createElement('owner')
        root_node.appendChild(owner_node)
        writeNode(owner_node, 'flickrid', root.getElementsByTagName("flickrid")[0].firstChild.data)
        writeNode(owner_node, 'name', root.getElementsByTagName("name")[0].firstChild.data)
        
        #创建size
        size_node = doc.createElement('size')
        root_node.appendChild(size_node)
        writeNode(size_node, 'width', root.getElementsByTagName("width")[0].firstChild.data)
        writeNode(size_node, 'height', root.getElementsByTagName("height")[0].firstChild.data)
        writeNode(size_node, 'depth', root.getElementsByTagName("depth")[0].firstChild.data)
        
        #创建segmented
        segmented_node = doc.createElement('segmented')
        root_node.appendChild(segmented_node)
        
        #创建object
        for i in range(len(name_lst)):
            temp = single_class_name[0]
            name_temp = name_lst[i]
            if name_temp in merge_class_name: #
                temp = merge_class_name_result
            if name_temp in move_class_name:
                continue
            
            x1 = int(root.getElementsByTagName("xmin")[i].firstChild.data)
            x1 = protectXY(x1,width)
            y1 = int(root.getElementsByTagName("ymin")[i].firstChild.data)
            y1 = protectXY(y1,height)
            x2 = int(root.getElementsByTagName("xmax")[i].firstChild.data)
            x2 = protectXY(x2,width)
            y2 = int(root.getElementsByTagName("ymax")[i].firstChild.data)
            y2 = protectXY(y2,height)
            area = (x2-x1+1)*(y2-y1+1)
            if area<=filter_area:
                continue
                
            object_node = doc.createElement('object')
            root_node.appendChild(object_node)
            #name
            writeNode(object_node, 'name', temp)
            #pose
            writeNode(object_node, 'pose', root.getElementsByTagName("pose")[i].firstChild.data)
            writeNode(object_node, 'truncated', root.getElementsByTagName("truncated")[i].firstChild.data)
            writeNode(object_node, 'difficult', root.getElementsByTagName("difficult")[i].firstChild.data)
            if len(occluded_lst_temp)>0:
                writeNode(object_node, 'occluded', root.getElementsByTagName("occluded")[i].firstChild.data)
            
            #创建bndbox
            bndbox_node = doc.createElement('bndbox')
            object_node.appendChild(bndbox_node)
            writeNode(bndbox_node, 'xmin', str(x1))
            writeNode(bndbox_node, 'ymin', str(y1))
            writeNode(bndbox_node, 'xmax', str(x2))
            writeNode(bndbox_node, 'ymax', str(y2))
        
        with open(pro_save_xml_dir+ basename +".xml", 'w' ) as f:
            f.write(doc.toprettyxml(indent='\t',encoding='utf-8'))
print null_num, error_num, no_bbox_num       