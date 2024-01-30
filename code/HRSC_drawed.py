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
        class_id = int(obj.find('Class_ID').text) % 100 + 14
        # class_id = 0 # 标签对应关系自行修改
        if int(difficult) == 1:
            continue
        mbox_cx, mbox_cy, mbox_w, mbox_h, mbox_ang = (
            float(obj.find('mbox_cx').text),
            float(obj.find('mbox_cy').text),
            float(obj.find('mbox_w').text),
            float(obj.find('mbox_h').text),
            float(obj.find('mbox_ang').text)
        )
        labels.append([class_id,mbox_cx, mbox_cy, mbox_w, mbox_h,mbox_ang])
    return labels

def draw_labels(img_path,labels):
    img = cv2.imread(img_path)
    for i in range(len(labels)):
        label = labels[i] #x,y,w,h,rad
        class_id,mbox_cx, mbox_cy, mbox_w, mbox_h,angle_rad= label
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
        cv2.polylines(img, [rotated_vertices], isClosed=True, color=(0, 255, 0), thickness=2)
    return img

def main(img_path,xml_path):
    img = draw_labels(img_path,get_label(xml_path))
    return img


if __name__ == '__main__':
    img_root = r'Train\AllImages'
    xml_root = r'HRSC2016\Train\Annotations'
    img_name = '100000693'
    img_path = os.path.join(img_root,img_name+'.bmp')
    xml_path = os.path.join(xml_root,img_name+'.xml')
    img = main(img_path,xml_path)
    cv2.imshow('test',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()