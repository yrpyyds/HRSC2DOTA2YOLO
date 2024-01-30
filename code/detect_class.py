"""
查看YOLO格式或HRSC格式标注文件所包含的类别
"""

import os
import xml.etree.ElementTree as ET
from collections import Counter
DOTA_train = r'..\train\labelTxt-v1.0\YOLO_labels' #放你需要检测的标注文件的目录
DOTA_val = r'..\labelTxt-v1.0\YOLO_labels'
HRSC_train = r"YOLO_labels"
HRSC_test = r"DOTA_labels"

def detect_class(labels_path):
    label_names = os.listdir(labels_path)
    classes = []
    for i in range(len(label_names)):
        label_name = label_names[i]
        label_path = os.path.join(labels_path,label_name)
        with open(label_path,'r') as f:
            lines = f.readlines()
        for line in lines:
            data = line.strip().split()
            classes.append(int(data[-1]))
            # if int(data[-1]) == 40:
            #     print(label_names[i])
    print(set(classes))

def detect_hrsc_class(xmls_path):
    xml_names = os.listdir(xmls_path)
    classes = []
    for i in range(len(xml_names)):
        xml_name = xml_names[i]
        xml_path = os.path.join(xmls_path,xml_name)
        in_file = open(xml_path)
        tree=ET.parse(in_file)
        root = tree.getroot()
        for obj in root.iter('HRSC_Object'):
            class_id = int(obj.find('Class_ID').text)
            classes.append(int(class_id))
    count = Counter(classes)
    classes_dict = dict()
    for item, cnt in count.items():
        classes_dict[item] = cnt
    sorted_keys = sorted(classes_dict.keys())
    classes_dict_new = dict()
    for i in range(len(sorted_keys)):
        classes_dict_new[sorted_keys[i]] = classes_dict[sorted_keys[i]]
    print(classes_dict_new)
        



detect_class(DOTA_train)
# detect_hrsc_class(r"HRSC2016\Train\Annotations")