import xml.etree.ElementTree as ET
import os
import math
import cv2
import numpy as np
import dota_utils as util
import random

# 手动输入cx cy w h angle进行绘制
# from HRSC_to_DOTA import get_rotated_box_vertices
# cx = 569.5045
# cy = 263.4875
# w = 261.0578
# h = 65.08137
# angle = -1.562451
# vertices = get_rotated_box_vertices(cx, cy, w, h, angle)
# vertices = np.array(vertices,dtype=np.int32)
# img = cv2.imread(r'AllImages\100000640.bmp')
# cv2.polylines(img,[vertices], isClosed=True, color=(255, 0, 0), thickness=2)
# cv2.imshow('test',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

img_root = r"Train\AllImages"
label_root = r"Train\DOTA_labels"
drawed_img_root = r"Train\DOTA_labels_drawed"
image_name = os.listdir(img_root)
for i in range(len(image_name)):
    img_path = os.path.join(img_root,image_name[i])
    label_path = os.path.join(label_root,image_name[i].split('.')[0]+'.txt')
    drawed_img_path = os.path.join(drawed_img_root,image_name[i])
    objects = util.parse_dota_poly(label_path)
    # print(objects)
    img = cv2.imread(img_path)
    poly = []
    for i in range(len(objects)):
        poly.append(np.array(objects[i]['poly'],dtype=np.int32))
    print(poly)
    # cv2.polylines(img,poly, isClosed=True, color=(255, 0, 0), thickness=2)
    # cv2.imwrite(drawed_img_path,img)