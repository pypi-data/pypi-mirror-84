#!/usr/local/bin/python3
import cv2
import numpy as np
import atexit
import pyzbar.pyzbar as pyzbar  #安装pyzbar：pip3 install pyzbar
from collections import  deque
import time
from PIL import Image
####
main_path = '/home/pi/class/'  # 读取和保存文件所用主文件夹
picture_path = main_path+'picture/'  # 图片文件夹
model_path = main_path+'model/'  # 识别模型文件夹

items_num= {0: '9', 1: '1', 2: '2', 3: '3',4: '4', 5: '5',6: '6', 7: '7',8: '8'}  #方向数字指示牌
items_dir={9: '左转',10: '右转'}
items_label={11: '语音'}
items_laji = {0: '易拉罐', 1: '纸团', 2: '塑料瓶', 3: '电池',4: '报纸', 5: '灯泡',6: '花生壳', 7: '香蕉皮'}

def read_cam(cam):
    ret, img = cam.read()
    ret, img = cam.read()
    ret, img = cam.read()
    ret, img = cam.read()
    ret, img = cam.read()
    if ret:
        return ret, img

class Camera():  # 摄像头基类
    def __init__(self, index):
        self.cam = cv2.VideoCapture(index)

    def read_camera(self):  # 连跳5帧可解决摄像头延时问题
        self.ret, self.img = self.cam.read()
        self.ret, self.img = self.cam.read()
        self.ret, self.img = self.cam.read()
        self.ret, self.img = self.cam.read()
        self.ret, self.img = self.cam.read()
        if self.ret:
            return self.img

    def show_image(self):
        if self.ret:
            cv2.imshow('img', self.img)

    def close_camera(self):
        self.cam.release()

    def close_allwindows(self):
        cv2.destroyAllWindows()

    def detect(self, img):
        pass

    def recognize(self, img):
        pass


class face_detect(Camera):  #检测人脸
    def __init__(self, model_name):  #初始化要输入模型名字
        self.path = model_path+model_name+'.xml'
        self.cascade = cv2.CascadeClassifier(self.path)
        self.data='no_people'

    def detect(self,img):
        self.data='no_people'
        self.img_new=img
        gray = cv2.cvtColor(self.img_new, cv2.COLOR_BGR2GRAY) # 转换灰色
        faces = self.cascade.detectMultiScale(gray, 2, 5)  #系数得调。
        #cv2.imshow('faces', faces)
        if len(faces): # 大于0则检测到人脸
            self.data='some_people'
            for (x, y, w, h) in faces:
                cv2.rectangle(self.img_new, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('face', self.img_new)
        cv2.waitKey(40)
'''

cam = cv2.VideoCapture(0)
#s = face_detect('eye')
while 1:
    ret, img = read_cam(cam)
    if ret == 1:
        cv2.imshow('img', img)
        cv2.waitKey(40)
        #s.detect(img)
        #print(s.data)
'''


class color_detect(Camera):  #颜色检测
    def __init__(self,color):
        self.data='none'  #保存颜色的检测结果
        if color=='red':
            self.color_list_lower = [50, 43, 46]  #这是红色的数值
            self.color_list_upper = [180, 255, 255]
        elif color=='green':
            self.color_list_lower = [35, 43, 46]
            self.color_list_upper = [77, 255, 255]
        elif color=='yellow':
            self.color_list_lower = [26, 43, 46]
            self.color_list_upper = [34, 255, 255]
        elif color=='blue':
            self.color_list_lower = [80, 43, 46]
            self.color_list_upper = [124, 255, 255]
        elif color=='orange':
            self.color_list_lower = [11, 43, 46]
            self.color_list_upper = [25, 255, 255]
        elif color=='black':
            self.color_list_lower = [0, 0, 0]
            self.color_list_upper = [180, 255, 46]
        elif color=='white':
            self.color_list_lower = [0, 0, 221]
            self.color_list_upper = [180, 30, 255]
        elif color=='gray':
            self.color_list_lower = [0, 0, 46]
            self.color_list_upper = [180, 43, 220]
        elif color=='purple':
            self.color_list_lower = [125, 43, 46]
            self.color_list_upper = [155, 255, 255]
        elif color=='qing':
            self.color_list_lower = [78, 43, 46]
            self.color_list_upper = [99, 255, 255]
        
            
        self.colorLower = np.array(self.color_list_lower)  #这是红色的数值
        self.colorUpper = np.array(self.color_list_upper)
        self.color=color
    # 初始化追踪点的列表
        self.mybuffer = 16
        self.pts = deque(maxlen=self.mybuffer)
        self.counter = 0
        
    def setcolorvalue(self, color, color_list_low, color_list_up):
        self.color_list_lower=color_list_low
        self.color_list_upper=color_list_up
        self.colorLower = np.array(self.color_list_lower)  #这是红色的数值
        self.colorUpper = np.array(self.color_list_upper)
        self.color=color
        print('设置阈值成功，当前阈值为：',self.color_list_lower,self.color_list_upper)
        
    def detect(self,frame):
        self.data='none'
        self.frame=frame
        self.img_new=frame
    # 转到HSV空间
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        # cv2.imshow('hsv',hsv)
        # cv2.waitKey(40)
    # 根据阈值构建掩膜
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
#         cv2.imshow('mask_original', mask)
#         cv2.waitKey(40)
    # 腐蚀操作
        mask = cv2.erode(mask, None, iterations=2)
    # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    # 初始化识别物体圆形轮廓质心
        center = None
    # 如果存在轮廓
        if len(cnts) > 0:
        # 找到面积最大的轮廓
            c = max(cnts, key = cv2.contourArea)
            x,y,w,h=cv2.boundingRect(c)  # 最大面积区域的外接矩形   x,y是左上角的坐标，w,h是矩形的宽和高
            #print('x,y,w,h',x,y,w,h)
            if w > 60 and h > 60:   # 宽和高大于一定数值的才要。
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
                cv2.rectangle(frame_bgr,(x,y),(x+w,y+h),(0,255,255),2)
                #print('x,y,w,h',x,y,w,h)
                if x < 0 or y < 0:
                    # self.img_new=frame_bgr
                    self.img_new = frame
                else:
                    #self.img_new=frame_bgr[y:y+h,x:x+w]
                    self.img_new=frame[y:y+h,x:x+w]
                # cv2.imshow('img_new', self.img_new)
                # cv2.waitKey(3)

        # 确定面积最大的轮廓的外接圆
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            self.x = x
            self.y = y
            self.radius = radius
        #计算轮廓的矩
            M = cv2.moments(c)
        #计算质心
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        #只有当半径大于100mm时，才执行画图
            if radius > 5:
                #img_circle=cv2.circle(self.frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                #cv2.circle(self.frame, center, 5, (0, 0, 255), -1)

            #把质心添加到pts中，并且是添加到列表左侧
                self.pts.appendleft(center)
                #cv2.imshow('color', self.frame)
                #cv2.waitKey(1)
                self.data=self.color

        else:#如果图像中没有检测到识别物体，则清空pts，图像上不显示轨迹。
            self.pts.clear()
            #cv2.imshow('color', self.frame)
            #cv2.waitKey(1)
            self.data='other_color'

class erweima_recognize(Camera):  #二维码检测类
    def __init__(self):
        self.data='none'

    def recognize(self,img):
        self.data='none'
        # 读取当前帧
        self.img=img
        #print('self.img',self.img)
        # 转为灰度图像
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.decodeDisplay(gray)
        cv2.imshow('erweima',gray)
        cv2.waitKey(1)

    def decodeDisplay(self,image):  #解码部分
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:
        # 提取条形码的边界框的位置
        # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # 条形码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
            barcodeData = barcode.data.decode("utf-8")
            self.data=barcodeData

class model_recognize(Camera):  #使用模型识别类,改一下item的名字就好
    #打开摄像头识别垃圾图片并返回对应文字
    def __init__(self,model_name):  #初始化要输入模型。传进来的模型必须是带后缀名的。
        self.model = cv2.dnn.readNetFromONNX(model_path+model_name)   #如'finally.proto'
        f=model_name.split(".")
        self.item=f[0]
        #print('self.item',self.item)
        self.pro=0
        self.data='none'

    def onnx_detect(self,img):
        #使用onnx模型进行预测
        img = cv2.resize(img,(224,224))

        img = np.asarray(img,dtype=np.float) / 255
        img = img.transpose(2,0,1)
        res = np.zeros_like(img,dtype=np.float)
        for i,(t, m, s) in enumerate(zip(img, [0.5,0.5,0.5], [0.5,0.5,0.5])):
            t = np.subtract(t,m)
            t = np.divide(t,s)
            res[i] = t
        img = res[np.newaxis,:]
        self.model.setInput(img)
        pro = self.model.forward()
        e_x = np.exp(pro.squeeze() - np.max(pro.squeeze()))
        self.pro = e_x / e_x.sum()


    def onnx_detect_new(self,img):
        img = np.asarray(img,dtype=np.float) / 255
        img = img.transpose(2,0,1)

        img = img[np.newaxis,:]
        self.model.setInput(img)
        pro = self.model.forward()
        e_x = np.exp(pro.squeeze() - np.max(pro.squeeze()))
        self.pro = e_x / e_x.sum()

    def recognize(self,img):
        # frame = cv2.resize(img,(224,224))
        frame = img.resize((224,224),Image.ANTIALIAS)
        # cv2.imshow("num_dir",img)
        # cv2.waitKey(1)
        self.onnx_detect_new(frame)
        if np.max(self.pro)>0.9:
            classNum = np.argmax(self.pro)
            if classNum in [0,1,2,3,4,5,6,7,8]:
                self.data=items_num[classNum]
            elif classNum in [9,10]:
                self.data=items_dir[classNum]
            elif classNum==11:
                self.data=items_label[classNum]
        else:
            self.data='none'

def take_photos(img,class_num_dir,name):
    filename = r'/home/pi/Desktop/camera_test/'+class_num_dir+'/' + str(name) + '.jpg'
    ret=cv2.imwrite(filename, img)
    if ret==1:
        print('图片成功保存到路径：',filename)
        return ret


# 检测类：人脸检测、颜色检测
# 识别类：数字方向识别、二维码识别、垃圾识别

'''
name=30
#测试数字和方向指示牌识别
cam = cv2.VideoCapture(0)  #打开摄像头
s=model_recognize('lxy1007.proto')  #现在是创建一个对象，就打开一个摄像头
blue=color_detect('blue')
img_path='/home/pi/camera_pos/'+str(name)+'.jpg'
while 1:
    ret,frame=cam.read()
    if ret:
        blue.detect(frame)
        # s.recognize(frame)
        frame_new=blue.img_new
        cv2.imshow("frame",frame)
        cv2.imshow("frame_new",frame_new)
        k=cv2.waitKey(40)
        if k==ord('s'):
            name=name+1
            cv2.imwrite(img_path,frame_new)
            img = Image.open(img_path)
            s.recognize(img)
            print(s.data)
'''
'''
# #测试二维码识别
# cam = cv2.VideoCapture(0)  #打开摄像头
# #er=erweima_recognize()
# while 1:
#     ret,img=read_cam(cam)
#     if ret==1:  #说明成功读取到了图片
#         cv2.imshow("img",img)
#         cv2.waitKey(1)
#         #er.recognize(img)
#         #print(er.data)

# cam = cv2.VideoCapture(0)
# while 1:
#     img = read_cam(cam)
#     cv2.imshow('img',img)
#     cv2.waitKey(1)
#     #cv2.destoryAllwindows()
'''
'''
#测试颜色阈值
cam = cv2.VideoCapture(0)  #打开摄像头
yu=color_detect('red')
t = [3,43,46]
s=[12,255,255]
m = yu.setcolorvalue('red', t, s)
#color_detect('red',[],[])
#num=model_recognize('8hao_1.proto')
while 1:
    ret,img=cam.read()
    if ret==1:  #说明成功读取到了图片
        cv2.imshow("img",img)
        cv2.waitKey(1)
        yu.detect(img)
        img_new=yu.img_new
        cv2.imshow('img_new',img_new)
        cv2.waitKey(40)
        #num.recognize(img_new)
        #print(s.data)
        #print(num.data)
'''
'''
#测试人脸检测
cam = cv2.VideoCapture(0)  #打开摄像头
s=face_detect('eye')
while 1:
    ret,img=read_cam(cam)
    if ret==1:  #说明成功读取到了图片
        cv2.imshow("img",img)
        cv2.waitKey(1)
        s.detect(img)
        print(s.data)
'''
'''
#测试蓝色检测
cam = cv2.VideoCapture(0)  #打开摄像头
blue=color_detect('blue')
#green = color_detect('green')
#white = color_detect('white')
black = color_detect('black')
#white = color_detect('white')
t = [80, 43, 46]
s=[124,255,255]
#blue.setcolorvalue('blue', t, s)
#num=model_recognize('8hao_1.proto')
while 1:
    ret,img=cam.read()
    if ret==1:  #说明成功读取到了图片
        cv2.imshow("img",img)
        cv2.waitKey(40)
        blue.detect(img)
    #green.detect(img)
        #white.detect(img)
        black.detect(img)
        #white.detect(img)
        img_0=blue.img_new
        #img_1=green.img_new
        #img_2=white.img_new
        img_3=black.img_new
        #img_4=white.img_new
        
        cv2.imshow('blue',img_0)
        #cv2.imshow('green',img_1)
        #cv2.imshow('wihte',img_2)
        cv2.imshow('black',img_3)
        #cv2.imshow('white',img_4)
        cv2.waitKey(40)
        #num.recognize(img_new)
        #print(s.data)
        #print(num.data)
'''
'''
#测试红绿色检测
cam = cv2.VideoCapture(0)  #打开摄像头
s=color_detect('red')
s.setcolorvalue('red',[156, 43, 46],[180, 255, 255])
while 1:
    ret,img=cam.read()
    if ret==1:  #说明成功读取到了图片
        cv2.imshow("img",img)
        cv2.waitKey(40)
        s.detect(img)
        print(s.data)
'''
'''
#整体检测
cam = cv2.VideoCapture(0)  #打开摄像头
num=model_recognize('num_dir.proto')
erweima=erweima_recognize()
face=face_detect('eye')
green=color_detect('green')
while 1:
    ret,img=read_cam(cam)
    if ret==1:  #说明成功读取到了图片
        #cv2.imshow("img",img)
        #cv2.waitKey(1)
        num.recognize(img)
        erweima.recognize(img)
        face.detect(img)
        green.detect(img)
        print('num.data',num.data)
        print('erweima.data',erweima.data)
        print('face.data',face.data)
        print('green.data',green.data)
'''


'''
#拍照程序
name=0
cam = cv2.VideoCapture(0)  #打开摄像头
#s=color_detect('blue')
while 1:
    img=read_cam(cam)
    cv2.imshow("img",img)
    k=cv2.waitKey(1)
    #s.detect(img)
    #img_new=s.img_new
    if k==ord('s'):
        r=take_photos(img,'people',name)
        print('r',r)
        if r==1:  #拍照成功s
            name+=1
       #print('name',name)
'''
'''
#测试数据集
i=0
size=(224,224)
cam = cv2.VideoCapture(0)  #打开摄像头
s=color_detect('blue')
num_dir=model_recognize('num_dir_3.proto')  #现在是创建一个对象，就打开一个摄像头
while 1:

    ret,img=read_cam(cam)
    if ret==1:  #成功读取到图片
        cv2.imshow("img",img)
        k=cv2.waitKey(40)
        s.detect(img)
        img_new=s.img_new
        #cv2.imwrite('/home/pi/Desktop/1.jpg',img_new)
        gray = cv2.cvtColor(img_new, cv2.COLOR_BGR2GRAY)
        ret,binary=cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
        #cv2.imwrite('/home/pi/Desktop/1.jpg',gray)
        if ret:
            cv2.imshow('binary',binary)
            cv2.waitKey(40)
            num_dir.recognize(img_new)
        #num_dir.recognize(img_new)
            print('num_dir',num_dir.data)
    #img_size=cv2.resize(img_new,size)
        #cv2.imwrite('/home/pi/Desktop/camera/save/1.jpg',img_size)

    img=cv2.imread('/home/pi/Desktop/1.jpg')
    cv2.imshow('img',img)
    cv2.waitKey(40)

        if i==2:

    img_n=cv2.imread('/media/pi/87DA-24D61/无人驾驶汽车/camera/7/50.jpg')
    num_dir.recognize(img_n)
    #num_dir.recognize(img_new)
    print('num_dir',num_dir.data)
   '''