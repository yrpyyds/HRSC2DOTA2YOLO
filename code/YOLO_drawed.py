import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QListWidget, QVBoxLayout, QWidget,QScrollArea
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor,QImage
from PyQt5.QtCore import Qt
import cv2
import dota_utils as util
import numpy as np

class AnnotationViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLO旋转框查看")  # 设置窗口标题
        self.setGeometry(100, 100, 1200, 800)  # 设置窗口大小和位置

        # 创建图像标签和文件列表
        self.image_label = QLabel(self)
        self.file_list = QListWidget(self)
        self.file_list.clicked.connect(self.show_image_with_annotation)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.file_list)
        layout.addWidget(self.image_label)
        

        # 创建一个Widget来放置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 创建打开按钮
        self.open_button = QPushButton("打开", self)
        self.open_button.clicked.connect(self.open_folder)
        layout.addWidget(self.open_button)

        self.image_folder = None  # 图像文件夹路径
        self.annotation_folder = None  # 标注文件夹路径
        self.image_files = []  # 图像文件列表
        self.annotation_files = []  # 标注文件列表

    def open_folder(self):
        # 打开图像和标注文件夹
        self.image_folder = QFileDialog.getExistingDirectory(self, '打开图像文件夹')
        self.annotation_folder = QFileDialog.getExistingDirectory(self, '打开标注文件夹')

        if self.image_folder and self.annotation_folder:
            self.load_image_and_annotation_files()  # 如果成功选择文件夹，则加载图像和标注信息

    def load_image_and_annotation_files(self):
        # 获取图像和标注文件列表
        self.image_files = [f for f in os.listdir(self.image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        self.annotation_files = [f for f in os.listdir(self.annotation_folder) if f.endswith('.txt')]

        # 在左侧列表中显示文件名
        self.file_list.clear()
        self.file_list.addItems(self.image_files)

    def show_image_with_annotation(self):
        # 显示选定图像及其标注
        selected_file = self.file_list.currentItem().text()
        image_path = os.path.join(self.image_folder, selected_file)
        drawed_image_path = os.path.join(self.image_folder,"drawed"+os.path.basename(selected_file))
        annotation_path = os.path.join(self.annotation_folder, selected_file.replace('.jpg', '.txt').replace('.png', '.txt').replace('.jpeg', '.txt').replace('.bmp', '.txt'))
        image_cv = cv2.imread(image_path)
        image_height, image_width, channels = image_cv.shape
        if os.path.exists(annotation_path):
            with open(annotation_path, 'r') as file:
                annotations = file.readlines()  # 读取标注文件的所有行
                if not annotations:
                    drawed_image_path = image_path
                    pixmap = QPixmap(drawed_image_path)
                    self.image_label.setPixmap(pixmap)  # 在标签上显示图像
                    self.image_label.setScaledContents(True)  # 图像自适应大小
                else:    
                    # 逐行读取标注信息并绘制标注框
                    objects = []
                    for annotation in annotations:
                        data = annotation.split()  # 按空格分割每一行
                        coords = [float(coord) for coord in data[1:9]]  # 8个数字是坐标
                        class_id = int(data[0])  # 第一个数字是类别编号
                        x1 = coords[0] * image_width
                        y1 = coords[1] * image_height
                        x2 = coords[2] * image_width
                        y2 = coords[3] * image_height
                        x3 = coords[4] * image_width
                        y3 = coords[5] * image_height
                        x4 = coords[6] * image_width
                        y4 = coords[7] * image_height
                        objects.append([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
                    poly = []
                    for i in range(len(objects)):
                        poly.append(np.array(objects[i],dtype=np.int32))
                    # color可以根据类别自行设置,本人没有此需求,统一用的蓝色
                    cv2.polylines(image_cv,poly, isClosed=True, color=(255, 0, 0), thickness=2)
                    cv2.imwrite(drawed_image_path,image_cv)
                    pixmap = QPixmap(drawed_image_path)
                    self.image_label.setPixmap(pixmap)  # 在标签上显示图像
                    self.image_label.setScaledContents(True)  # 图像自适应大小
                    os.remove(drawed_image_path)

        else:
            raise AttributeError(f"没有对应的{annotation_path}")
             


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnnotationViewer()
    window.show()
    sys.exit(app.exec_())
