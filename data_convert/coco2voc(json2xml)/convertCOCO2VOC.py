#__author__ = 'lg 2018-4-24'


#coding=utf-8

import xml.dom
import xml.dom.minidom
import os
import cv2
import json

# xml文件规范定义

#表头图片地址 不修改
_IMAGE_PATH= 'opt/ligang/data/coco'

_INDENT= ''*4
_NEW_LINE= '\n'
_FOLDER_NODE= 'COCO2014'
_ROOT_NODE= 'annotation'
_DATABASE_NAME= 'LOGODection'
_ANNOTATION= 'COCO2014'
_AUTHOR= 'HHJ'
_SEGMENTED= '0'
_DIFFICULT= '0'
_TRUNCATED= '0'
_POSE= 'Unspecified'
_CLASSNAME = ["person","bicycle","car","motorbike","aeroplane","bus","train","truck","boat","traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball","kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket","bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","sofa","pottedplant","bed","diningtable","toilet","tvmonitor","laptop","mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors","teddy bear","hair drier","toothbrush"]

#xml输出路径
_ANNOTATION_SAVE_PATH= '/home/ligang/data_convert/coco_voc-json_xml/xml/'
# _IMAGE_CHANNEL= 3

# 封装创建节点的过�?
def createElementNode(doc,tag, attr):  # 创建一个元素节点
    element_node = doc.createElement(tag)

    # 创建一个文本节点
    text_node = doc.createTextNode(attr)

    # 将文本节点作为元素节点的子节点
    element_node.appendChild(text_node)

    return element_node

# 封装添加一个子节点的过
def createChildNode(doc,tag, attr,parent_node):

    child_node = createElementNode(doc, tag, attr)

    parent_node.appendChild(child_node)


# object节点比较特殊
def createObjectNode(doc,attrs):

    object_node = doc.createElement('object')

    createChildNode(doc, 'name', _CLASSNAME[attrs['category_id']-1],
                    object_node)

    createChildNode(doc, 'pose',
                    _POSE, object_node)

    createChildNode(doc, 'truncated',
                    _TRUNCATED, object_node)

    createChildNode(doc, 'difficult',
                    _DIFFICULT, object_node)

    bndbox_node = doc.createElement('bndbox')

    createChildNode(doc, 'xmin', str(int(attrs['bbox'][0])),
                    bndbox_node)

    createChildNode(doc, 'ymin', str(int(attrs['bbox'][1])),
                    bndbox_node)

    createChildNode(doc, 'xmax', str(int(attrs['bbox'][0]+attrs['bbox'][2])),
                    bndbox_node)

    createChildNode(doc, 'ymax', str(int(attrs['bbox'][1]+attrs['bbox'][3])),
                    bndbox_node)

    object_node.appendChild(bndbox_node)

    return object_node

# 将documentElement写入XML文件�?
def writeXMLFile(doc,filename):

    tmpfile =open(os.path.join(_ANNOTATION_SAVE_PATH, ('tmp' + '.xml')),'w')
    doc.writexml(tmpfile, addindent=''*4,newl = '\n',encoding = 'utf-8')

    tmpfile.close()

    # 删除第一行默认添加的标记

    fin =open(os.path.join(_ANNOTATION_SAVE_PATH, ('tmp' + '.xml')))
    # print(filename)
    fout =open(filename, 'w')
    # print(os.path.dirname(fout))

    lines = fin.readlines()

    for line in lines[1:]:

        if line.split():
            fout.writelines(line)

        # new_lines = ''.join(lines[1:])

        # fout.write(new_lines)

    fin.close()

    fout.close()


if __name__ == "__main__":
    ##读取图片列表
    img_path = "/home/ligang/data_convert/coco_voc-json_xml/benchmark"
    fileList = os.listdir(img_path)
    if fileList == 0:
        os._exit(-1)
    ##json路径
    with open("/home/ligang/data_convert/coco_voc-json_xml/instances_body_minival.json", "r") as f:
        ann_data = json.load(f)

    current_dirpath = os.path.dirname(os.path.abspath('__file__'))

    if not os.path.exists(_ANNOTATION_SAVE_PATH):
        os.mkdir(_ANNOTATION_SAVE_PATH)

    for imageName in fileList:
        if os.path.splitext(imageName)[1] == '.jpg':
            saveName= imageName.strip(".jpg")
            print(saveName)
            
            # 在文件夹中挑选json中标记的图片
            bflag_img_exist = False
            images_dict = ann_data["images"]
            for ann in images_dict:
                if(saveName==ann["id"]):
                    bflag_img_exist = True
                    break #图片在json中存在
                else:
                    continue
            
            #json文件中不包括此图片
            if not bflag_img_exist:
                continue
            
            # pos = fileList[xText].rfind(".")
            # textName = fileList[xText][:pos]

            # ouput_file = open(_TXT_PATH + '/' + fileList[xText])
            # ouput_file =open(_TXT_PATH)

            # lines = ouput_file.readlines()

            xml_file_name = os.path.join(_ANNOTATION_SAVE_PATH, (saveName + '.xml'))
            # with open(xml_file_name,"w") as f:
            #     pass

            img=cv2.imread(os.path.join(img_path,imageName))
            print(os.path.join(img_path,imageName))
            # cv2.imshow(img)
            height,width,channel=img.shape
            print(height,width,channel)



            my_dom = xml.dom.getDOMImplementation()

            doc = my_dom.createDocument(None,_ROOT_NODE,None)

            # 获得根节�?
            root_node = doc.documentElement

            # folder节点

            createChildNode(doc, 'folder',_FOLDER_NODE, root_node)

            # filename节点

            createChildNode(doc, 'filename', saveName+'.jpg',root_node)

            # source节点

            source_node = doc.createElement('source')

            # source的子节点

            createChildNode(doc, 'database',_DATABASE_NAME, source_node)

            createChildNode(doc, 'annotation',_ANNOTATION, source_node)

            createChildNode(doc, 'image','flickr', source_node)

            createChildNode(doc, 'flickrid','NULL', source_node)

            root_node.appendChild(source_node)

            # owner节点

            owner_node = doc.createElement('owner')

            # owner的子节点

            createChildNode(doc, 'flickrid','NULL', owner_node)

            createChildNode(doc, 'name',_AUTHOR, owner_node)

            root_node.appendChild(owner_node)

            # size节点

            size_node = doc.createElement('size')

            createChildNode(doc, 'width',str(width), size_node)

            createChildNode(doc, 'height',str(height), size_node)

            createChildNode(doc, 'depth',str(channel), size_node)

            root_node.appendChild(size_node)

            # segmented节点

            createChildNode(doc, 'segmented',_SEGMENTED, root_node)

            
            #添加图片的 类别
            annotation_dict = ann_data["annotations"]
            for ann in annotation_dict:
                if(saveName==ann["image_id"]):
                    # object节点
                    object_node = createObjectNode(doc, ann)
                    root_node.appendChild(object_node)
                else:
                    continue


            # 构建XML文件名称

            print('xml_file_name',xml_file_name)

            # 创建XML文件

            # createXMLFile(attrs, width, height, xml_file_name)


            # # 写入文件
            #
            writeXMLFile(doc, xml_file_name)