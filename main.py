from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from PIL import Image, ImageEnhance
from PIL.ImageFilter import SHARPEN, BLUR

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('ULTIMATE EDITOR 9000')

folder = QPushButton('Folder')
imglist = QListWidget()
Img = QLabel('Image')
rotate_left = QPushButton('Left')
rotate_right = QPushButton('Right')
Mirroring = QPushButton('Mirror')
Sharpness = QPushButton('Sharpness')
BNW = QPushButton('B&W')
Blur = QPushButton('Blur')
Gray = QPushButton('Grayscale')
contrast_up = QPushButton('Contrast Up')
contrast_down = QPushButton('Contrast Down')

Layout = QHBoxLayout()
LayoutV1 = QVBoxLayout()
LayoutH1 = QHBoxLayout()
LayoutH1V = QVBoxLayout()

LayoutV1.addWidget(folder)
LayoutV1.addWidget(imglist)

LayoutH1.addWidget(rotate_left)
LayoutH1.addWidget(rotate_right)
LayoutH1.addWidget(Mirroring)
LayoutH1.addWidget(Sharpness)
LayoutH1.addWidget(BNW)
LayoutH1.addWidget(Gray)
LayoutH1.addWidget(contrast_up)
LayoutH1.addWidget(contrast_down)
LayoutH1.addWidget(Blur)

LayoutH1V.addWidget(Img)

LayoutH1V.addLayout(LayoutH1)

Layout.addLayout(LayoutV1, 20)
Layout.addLayout(LayoutH1V, 80)

directory = ''

def filter(files, format_img):
    hasil = []
    for name in files:
        for i in format_img:
            if name.endswith(i):
                hasil.append(name)
    return hasil

class imgprocess():
    def __init__(self):
        self.image = None 
        self.dir = None
        self.filename = None
        self.save_dir = 'bestmodif/'
        self.value_contrast = 1
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        imagepath = os.path.join(dir, filename)
        self.image = Image.open(imagepath)
    def showImage(self, imagepath):
        Img.hide()
        showimg = QPixmap(imagepath)
        width = Img.width()
        height = Img.height()
        showimg = showimg.scaled(width, height, Qt.KeepAspectRatio)
        Img.setPixmap(showimg)
        Img.show()
    def saveimg(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def BandW_img(self):
        self.image = self.image.convert('1')
        self.saveimg()
        imgpath = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(imgpath)
    def sharpen_img(self):
        self.image = self.image.filter(SHARPEN)
        self.saveimg()
        imgpath = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(imgpath)
    def mirror_img(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveimg()
        imgpath = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(imgpath)
    def rotate_left_img(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveimg()
        imgpath = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(imgpath)
    def rotate_right_img(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveimg()
        imgpath = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(imgpath)
    def Blur_img(self):
        self.image = self.image.filter(BLUR)
        self.saveimg()
        imgpath = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(imgpath)
    def Grayscale_img(self):
        self.image = self.image.convert('L')
        self.saveimg()
        imgpath = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(imgpath)
    def Contrast_up_img(self):
        self.value_contrast += 0.2
        img_contrast = ImageEnhance.Contrast(self.image)
        self.image = img_contrast.enhance(self.value_contrast)
        self.saveimg()
        imgpath = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(imgpath)
        print(self.value_contrast)
    def Contrast_down_img(self):
        self.value_contrast -= 0.2
        img_contrast = ImageEnhance.Contrast(self.image)
        self.image = img_contrast.enhance(self.value_contrast)
        self.saveimg()
        imgpath = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(imgpath)
        print(self.value_contrast)

def openfolder():
    format_img = ['.jpg']
    global directory
    directory = QFileDialog.getExistingDirectory()
    filenames = filter(os.listdir(directory), format_img)
    imglist.clear()
    for filename in filenames:
        imglist.addItem(filename)

def imgchoosen():
    print(imglist.currentRow())
    if imglist.currentRow() >= 0:
        filename = imglist.currentItem().text()
        boximage.loadImage(directory, filename)
        imagepath = os.path.join(boximage.dir, boximage.filename)
        boximage.showImage(imagepath)
boximage = imgprocess()
folder.clicked.connect(openfolder)
imglist.currentRowChanged.connect(imgchoosen)
BNW.clicked.connect(boximage.BandW_img)
Sharpness.clicked.connect(boximage.sharpen_img)
Mirroring.clicked.connect(boximage.mirror_img)
rotate_left.clicked.connect(boximage.rotate_left_img)
rotate_right.clicked.connect(boximage.rotate_right_img)
Blur.clicked.connect(boximage.Blur_img)
Gray.clicked.connect(boximage.Grayscale_img)
contrast_up.clicked.connect(boximage.Contrast_up_img)
contrast_down.clicked.connect(boximage.Contrast_down_img)

win.setLayout(Layout)
win.show()
app.exec()