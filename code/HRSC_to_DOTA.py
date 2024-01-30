import xml.etree.ElementTree as ET
import os
import math
import cv2
import numpy as np
def get_label(xml_path):
    in_file = open(xml_path)
    tree=ET.parse(in_file)
    root = tree.getroot()
    labels = []
    for obj in root.iter('HRSC_Object'):
        difficult = obj.find('difficult').text
        class_id = int(obj.find('Class_ID').text) % 100
        # class_id = 0 # 标签对应关系自行修改
        # if int(difficult) == 1:
        #     continue
        mbox_cx, mbox_cy, mbox_w, mbox_h, mbox_ang = (
            float(obj.find('mbox_cx').text),
            float(obj.find('mbox_cy').text),
            float(obj.find('mbox_w').text),
            float(obj.find('mbox_h').text),
            float(obj.find('mbox_ang').text)
        )
        labels.append([class_id,mbox_cx, mbox_cy, mbox_w, mbox_h,mbox_ang])
    return labels
# 计算旋转框四个顶点的坐标
def get_rotated_box_vertices(labels,label_path):
    with open(label_path,'w') as f:
        for i in range(len(labels)):
            class_id,mbox_cx, mbox_cy, mbox_w, mbox_h,angle_rad= labels[i]
            rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                    [np.sin(angle_rad), np.cos(angle_rad)]])
            box_half_width = mbox_w / 2
            box_half_height = mbox_h / 2
            box_vertices = np.array([[-box_half_width, -box_half_height],
                                    [box_half_width, -box_half_height],
                                    [box_half_width, box_half_height],
                                    [-box_half_width, box_half_height]])
            rotated_vertices = np.dot(box_vertices, rotation_matrix.T)
            rotated_vertices[:, 0] += mbox_cx
            rotated_vertices[:, 1] += mbox_cy
            rotated_vertices = np.round(rotated_vertices).astype(np.int32)
            # print(rotated_vertices)
            # f.write(" ".join([str(a) for a in rotated_vertices]) + '\n')
            rotated_vertices = rotated_vertices.reshape(-1)
            f.write(" ".join([str(a) for a in rotated_vertices]) + " " + str(class_id) + '\n')


    # return rotated_vertices_list

xml_root = r"HRSC2016\Test\Annotations"
txt_root = r"HRSC2016\Test\DOTA_labels"

xml_name = os.listdir(xml_root)
# print(len(xml_name))
for i in range(len(xml_name)):
    xml_path = os.path.join(xml_root,xml_name[i])
    txt_path = os.path.join(txt_root,xml_name[i].split('.')[0]+'.txt')
    get_rotated_box_vertices(get_label(xml_path),txt_path)