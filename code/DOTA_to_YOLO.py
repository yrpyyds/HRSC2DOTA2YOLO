import xml.etree.ElementTree as ET
import os
import math
import cv2
import dota_utils
"""
get_normalization_dota:DOTA转YOLO v8格式,具体格式参照官网:https://docs.ultralytics.com/zh/datasets/obb/
get_normalization_hrscHRSC:转换后的DOTA转YOLO v8格式,先配合HRSC_to_DOTA使用
"""
def get_hrsc_wh(xml_path):
    in_file = open(xml_path)
    tree=ET.parse(in_file)
    root = tree.getroot()
    image_width = int(root.find('Img_SizeWidth').text)
    image_height = int(root.find('Img_SizeHeight').text)
    return image_width,image_height

def get_dota_wh(img_path):
    img = cv2.imread(img_path)
    image_height, image_width, channels = img.shape
    return image_width,image_height

def get_normalization_hrsc(image_width,image_height,dota_label_path,yolo_label_path):
    with open(dota_label_path,'r') as f:
        lines = f.readlines()
    normalized_data = []
    aircraft_carrier = [2,5,6,12,13,31,32,33]
    warcraft = [3,7,8,9,10,11,14,15,16,17,19,28,29]
    merchant_ship = [4,18,20,22,24,25,26,30]
    submarine = [27]
    aircraft_carrier = [x + 14 for x in aircraft_carrier]
    warcraft = [x + 14 for x in warcraft]
    merchant_ship = [x + 14 for x in merchant_ship]
    submarine = [x + 14 for x in submarine]

    for line in lines:
        data = line.strip().split()
        x1, y1, x2, y2, x3, y3, x4, y4, class_label = map(int, data)
        if class_label in aircraft_carrier:
            class_label = 14
        elif class_label in warcraft:
            class_label = 15
        elif class_label in merchant_ship:
            class_label = 16
        elif class_label in submarine:
            class_label = 17
        else:
            continue        
        x1_normalized = x1 / image_width
        y1_normalized = y1 / image_height
        x2_normalized = x2 / image_width
        y2_normalized = y2 / image_height
        x3_normalized = x3 / image_width
        y3_normalized = y3 / image_height
        x4_normalized = x4 / image_width
        y4_normalized = y4 / image_height
        normalized_line = "{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {}\n".format(
        class_label,x1_normalized, y1_normalized, x2_normalized, y2_normalized,
        x3_normalized, y3_normalized, x4_normalized, y4_normalized,
        
    )
        normalized_data.append(normalized_line)
    with open(yolo_label_path,'w') as f:
        f.writelines(normalized_data)

def get_normalization_dota(image_width,image_height,dota_label_path,yolo_label_path):
    with open(dota_label_path,'r') as f:
        lines = f.readlines()
    normalized_data = []
    for line in lines[2:]:
        data = line.strip().split()
        if data[-2] in dota_utils.wordname_14_noship and data[-2] != 'ship':
            data[-2] = dota_utils.wordname_14_noship.index(data[-2])
        elif data[-2] == 'ship':
            continue
        else:
            print("发生重大错误,格式\标注不正确")
            print(data[-2])
            break
        x1, y1, x2, y2, x3, y3, x4, y4, class_label,difficult = map(int, data)
        x1_normalized = x1 / image_width
        y1_normalized = y1 / image_height
        x2_normalized = x2 / image_width
        y2_normalized = y2 / image_height
        x3_normalized = x3 / image_width
        y3_normalized = y3 / image_height
        x4_normalized = x4 / image_width
        y4_normalized = y4 / image_height
        normalized_line = "{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {}\n".format(
        class_label,x1_normalized, y1_normalized, x2_normalized, y2_normalized,
        x3_normalized, y3_normalized, x4_normalized, y4_normalized,
    )
        normalized_data.append(normalized_line)
    with open(yolo_label_path,'w') as f:
        f.writelines(normalized_data)


if __name__ == '__main__':
    """
    HRSC
    """
    hrsc_root = r"Train\Annotations"
    dota_root = r"Train\DOTA_labels"
    yolo_root = r"Train\YOLO_labels"
    dota_label_names = os.listdir(dota_root)
    for i in range(len(dota_label_names)):
        dota_label_name = dota_label_names[i]
        hrsc_label_path = os.path.join(hrsc_root,dota_label_name.split('.')[0]+'.xml')
        dota_label_path = os.path.join(dota_root,dota_label_name)
        yolo_root_path = os.path.join(yolo_root,dota_label_name.split('.')[0]+'.txt')
        image_width,image_height = get_hrsc_wh(hrsc_label_path)
        get_normalization_hrsc(image_width,image_height,dota_label_path,yolo_root_path)

# if __name__ == "__main__":
#     """
#     DOTA
#     """
#     dota_root = r"labelTxt-v1.0\labelTxt"
#     yolo_root = r"labelTxt-v1.0\YOLO_labels"
#     img_root = r"images\images"
#     dota_label_names = os.listdir(dota_root)
#     for i in range(len(dota_label_names)):
#         dota_label_name = dota_label_names[i]
#         img_path = os.path.join(img_root,dota_label_name.split('.')[0]+'.png')
#         dota_label_path = os.path.join(dota_root,dota_label_name)
#         yolo_root_path = os.path.join(yolo_root,dota_label_name.split('.')[0]+'.txt')
#         image_width,image_height = get_dota_wh(img_path)
#         get_normalization_dota(image_width,image_height,dota_label_path,yolo_root_path)






