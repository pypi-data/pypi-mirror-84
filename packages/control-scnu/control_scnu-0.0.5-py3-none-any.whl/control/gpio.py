#!/usr/local/bin/python3
from __future__ import division
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import cv2
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

main_path='/home/pi/class/'
# 读取和保存文件所用主文件夹

io2gpio={0:0,1:1,2:4,3:5,4:6,5:12,6:13,7:16,8:17,  11:20,12:21,13:23,14:24}
motor2gpio={1:20,2:21,3:23,4:24}

class io():  #最基本的GPIO控制基类
    def __init__(self,io_num):  #初始化的时候要输入IO几
        #加个判断的，普通IO，电机IO，PWMIO要区分开。
        self.gpio=io2gpio[io_num]   #IO号转为GPIO号
        self.ioin=404  #表示IO口没有输入
        #一些初始化的代码
        print("IO 库")

    def setmode(self,gpiomode):    #设置GPIO的模式,bcm或者board
        if gpiomode=='BCM':
            GPIO.setmode(GPIO.BCM)
        elif gpiomode=='BOARD':
            GPIO.setmode(GPIO.BOARD)

    def setinout(self,inorout):#设置GPIO的输入或者输出
        if inorout=='IN':
            GPIO.setup(self.gpio, GPIO.IN)
        elif inorout=='OUT':
            GPIO.setup(self.gpio, GPIO.OUT)

    def setioout(self,dianping):  #GPIO输出高or低电平
        if dianping=='HIGH':
            GPIO.output(self.gpio,GPIO.HIGH)
        elif dianping=='LOW':
            GPIO.output(self.gpio,GPIO.LOW)

    def getioin(self):  #获取GPIO口的输入电平
        if GPIO.input(self.gpio)==0:  #低电平,返回false
            time.sleep(0.01)
            if GPIO.input(self.gpio)==0: #防抖设计
                self.ioin=0  #输入为低电平
        else:
            self.ioin=1

    def cleanio(self):  #清理io口
        GPIO.cleanup(self.gpio)

class beep():  #普通io口的蜂鸣器
    def __init__(self,beepio):
        self.gpio=io2gpio[beepio]
        GPIO.setup(self.gpio, GPIO.OUT)
        GPIO.output(self.gpio,GPIO.HIGH)
        self.data=0

    def beep_s(self,seconds):
        GPIO.output(self.gpio,GPIO.LOW)
        time.sleep(seconds)
        GPIO.output(self.gpio,GPIO.HIGH)

    def beep(self):
        GPIO.output(self.gpio,GPIO.LOW)
'''
#测试蜂鸣器   VCC只能接3.3V
b=beep(2)
b.beep_s(0)  #关闭蜂鸣器beep_s(0)
'''

class led():
    def __init__(self,ledio):
        self.gpio=io2gpio[ledio]
        GPIO.setup(self.gpio, GPIO.OUT)
        GPIO.output(self.gpio,GPIO.HIGH)

    def openled(self):   #灯亮
        GPIO.output(self.gpio,GPIO.HIGH)

    def closeled(self):
        GPIO.output(self.gpio,GPIO.LOW)

'''
l=led(1)
l.closeled()
'''

class tmp_hum():
    def __init__(self,t_h_io):
        self.gpio=io2gpio[t_h_io]
        GPIO.setup(self.gpio, GPIO.IN)
        self.temp='none'
        self.humi='none'

    def getTemp_Humi(self):
        tmp=Adafruit_DHT.DHT11
        humi,temp=Adafruit_DHT.read_retry(tmp,self.gpio)
        if temp==None or humi==None:
            self.data="获取温湿度失败"
        else:
            self.temp=str(temp)+'。c'
            self.humi=str(humi)+'%'

'''
#测试温湿度，成功
t=tmp_hum(1)
t.getTemp_Humi()
print('t.humi',t.humi)
print('t.temp',t.temp)
'''

class hongwai(io):  #红外检测模块
    def __init__(self,hongwaiio):  #初始化要输入模型名字
        super().__init__(hongwaiio)
        super().setinout('IN')  #红外IO设置为输入模式
        self.data=0  #没有东西遮挡为False

    def getOcclusion(self):
        super().getioin()    #获取hongwaiio的值

'''
h=hongwai(5)
while 1:
    h.getOcclusion()
    print('self.ioin',h.ioin)
'''

class pwm():
    #pwm={40:0,41:1,42:2,43:3,44:4,45:5,46:6,47:7,48:8}
    def __init__(self,pwm_io):  #初始化,必须提供是哪个pwm口，即打开pwm功能,pwm_io>40
        self.pw = Adafruit_PCA9685.PCA9685()
        self.io_pwm=pwm_io

    def pwm_start(self,duty=50):      #pw产生的PWM波发生器
        self.pw.set_pwm(self.io_pwm, 0, int((100-duty)*40.95))   #对于低电平有效的RGB灯而言

    def setduty():
        pass

    def setfreq():
        pass

'''
#测试pca9685产生的PWM波
p=pwm(6)
while 1:
    p.pwm_start()
'''

class servo(pwm):
    def __init__(self,servo_io):
        super().__init__(servo_io)
        self.io=servo_io
        self.duty=0
        self.pw.set_pwm(self.io, 0, int(0*40.95))

    def setServoAngle(self,angle):   #设置舵机角度
#         duty=4096*((angle*11)+500)/20000   #由角度算占空比
#         print('duty',duty)
#         self.duty=int(duty)
        self.duty=(angle/18+3)-0.5
        print('duty',self.duty)
        self.pw.set_pwm(self.io, 0, int(self.duty*40.95))
'''
s=servo(6)
s.setServoAngle(60)
'''
class motor():  #单个电机的类
    def __init__(self,motor_io):  #初始化要输入模型名字
        #super().__init__(motor_io)
        self.io=motor2gpio[motor_io]
        self.pw = Adafruit_PCA9685.PCA9685()
        
            #使能端
        GPIO.setup(19,GPIO.OUT)
        GPIO.output(19,GPIO.HIGH)
        GPIO.setup(22,GPIO.OUT)
        GPIO.output(22,GPIO.LOW)
            #电机口端
        GPIO.setup(20,GPIO.OUT)
        GPIO.output(20,GPIO.LOW)
        GPIO.setup(21,GPIO.OUT)
        GPIO.output(21,GPIO.LOW)

    def motor_single(self,mdir,speed):
        # 11之后是电机IO对应的GPIO
        io1 = 14   #20
        io2 = 15   #21
        io3 = 12   #23
        io4 = 13   #24
        #电机1、2初始化并使能
        if self.io==20:
        #电机1
            if mdir == 0:   #0是向前转动，1是向后转动
                GPIO.output(20,GPIO.HIGH)
                self.pw.set_pwm(io1, 0, int((100-speed)*40.95))
                #GPIO.output(21,GPIO.LOW)
            else:
                GPIO.output(20,GPIO.LOW)
                self.pw.set_pwm(io1, 0, int(speed*40.95))
                #GPIO.output(21,GPIO.LOW)
        elif self.io==21:
        #电机2
            if mdir == 1:
                GPIO.output(21,GPIO.LOW)
                self.pw.set_pwm(io2, 0, int(speed*40.95))
                #GPIO.output(20,GPIO.LOW)
            else:
                GPIO.output(21,GPIO.HIGH)
                self.pw.set_pwm(io2, 0, int((100-speed)*40.95))
                #GPIO.output(20,GPIO.LOW)
                
   


class car():  #小车类，包含小车的基本运动，前进，后退，左转，右转，还有寻线
    def __init__(self,io_1,io_2,hw_1=1,hw_2=2,led0=0,led1=1):  #初始化要输入模型名字
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(18000)
        # 11之后是电机IO对应的GPIO
        io1 = 14   #20
        io2 = 15   #21
        io3 = 12   #23
        io4 = 13   #24
        GPIO.setup(20, GPIO.OUT) #设置引脚2为输出通道
        GPIO.setup(19, GPIO.OUT) #设置引脚2为输出通道
        GPIO.output(19,GPIO.HIGH)
        GPIO.setup(1, GPIO.IN) #设置引脚1（BCM编号）为输入通道
        GPIO.setup(4, GPIO.IN) #设置引脚1（BCM编号）为输入通道1GPIO.setup(0, GPIO.IN) #设置引脚1（BCM编号）为输入通道
        GPIO.setup(21, GPIO.OUT) #设置引脚2为输出通道
        self.came=0  #识别到等待线之后才把cam置为1.
        self.go_1=22
        self.go_2=22
        self.left_1=9.7
        self.left_2=22
        self.right_1=22
        self.right_2=9.7
        self.dec = 0

    def go(self):
        self.go1()
        if GPIO.input(1)==1 and GPIO.input(4)==1:
            self.dec='yes'
        else:
            self.dec='no'
            
    def go1(self):
        self.pwm.set_pwm(14,0,int(self.go_1*40.95))  #900
        self.pwm.set_pwm(15,0,int(self.go_2*40.95))  #900

    def turn_left(self):
        self.turn_left1()
        time.sleep(0.2)
        if GPIO.input(1)==1 and GPIO.input(4)==1:
            self.dec='yes'
        else:
            self.dec='no'
                
    def turn_right(self):
        self.turn_right1()
        time.sleep(0.2)
        if GPIO.input(1)==1 and GPIO.input(4)==1:
            self.dec='yes'
        else:
            self.dec='no'
    
    def turn_left1(self):
        
        self.pwm.set_pwm(14,0,int(self.left_1*40.95))  #400
        self.pwm.set_pwm(15,0,int(self.left_2*40.95))  #900

    def turn_right1(self):
        
        self.pwm.set_pwm(14,0,int(self.right_1*40.95))
        self.pwm.set_pwm(15,0,int(self.right_2*40.95))

    def stop(self,d1=0,d2=0):
        self.pwm.set_pwm(14,0,0)
        self.pwm.set_pwm(15,0,0)

    def setspeed(self, direction, s_1, s_2):   #car_1.setspeed('go',22,22)
        # 改变小车1前进的速度为：22,22
        if direction=='go':
            self.go_1=s_1
            self.go_2=s_2
        elif direction=='turn_right':
            self.right_1=s_1
            self.right_2=s_2
        elif direction=='turn_left':
            self.left_1=s_1
            self.left_2=s_2

    def xunxian(self):
        self.came=0
#         #包括寻线和停在等待线、十字路口部分代码.在等待线后停止，break寻线函数，且设置camera=1,操作完后要camera=0;
#         self.hw_1.getOcclusion()
#         self.hw_2.getOcclusion()
#
#         IR1=self.hw_1.ioin
#         IR2=self.hw_2.ioin
        #前进
        if GPIO.input(1)==1 and GPIO.input(4)==1:
            self.go1()
            print("前进")
        #左转
        if GPIO.input(1)==1 and GPIO.input(4)==0:
            self.turn_left1()
            print("左转")
        #右转
        if GPIO.input(1)==0 and GPIO.input(4)==1:
            self.turn_right1()
            print("右转")
        #停止
        if GPIO.input(1)==0 and GPIO.input(4)==0:
            self.stop()
            #print("停止")
            self.came=1
            
'''
# test autofinding
m = car(1,2)
m.setspeed('turn_left', 2, 50)
m.xunxian()
'''

'''
#测试单个电机的。
m=motor(2)   #这两句代码不能放在同一个编程块中
while 1:
    m.motor_single(1,00)
'''
'''
#单个电机组成小车运动
m_left=motor(1)
m_right=motor(2)  #一定得先初始化完对象，再转，不然会报错。
m_left.motor_single(1,00)  #0是往后转，1是往前转。
m_right.motor_single(1,00)
'''
#测试
'''
m=car(1,2)
m.setspeed('go', 80, 00)
m.go()
time.sleep(3)
m.stop()
'''
'''
i=1
m=car(1,2)
m.turn_right()
time.sleep(30)
m.stop()
'''
'''
m=car(1,2)
m.stop()
'''
'''
m=car(1,2)
# m.setspeed('go',23, 23)
# m.setspeed('turn_left', 2, 23)
# m.setspeed('turn_right', 23, 2)
m.turn_right()
while 1:
    m.xunxian()
    #if m.came==1:
     #   m.turn_left()
     '''
'''
m=car(1,2)
while(1):
    m.turn_right()
    print(m.dec)
    if m.dec=='yes':
        print('m.dec:',m.dec)
        m.stop()
        break
'''
'''
m=car(1,2)
m.stop()
cap = cv2.VideoCapture(0)   #实例化摄像头
center=320  #刚开始假设黑线中心在图像中心
empty=[]
while True:
    ret,frame = cap.read()  #capture frame_by_frame
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   #获取灰度图像
    ret,dst=cv2.threshold(gray,70,255,cv2.THRESH_BINARY)#对灰度图像进行二值化
    dst=cv2.erode(dst,None,iterations=6)  #腐蚀操作，黑线中间的白色区域变小。
    #cv2.imshow('BINARY',dst)        #树莓派桌面显示二值化图像，比较占资源默认
    #cv2.waitKey(40)
    color_1=dst[380]  #单看1/4高度的那一行像素
    color_2=dst[430]
    #cv2.imshow('color',color)
    black_count_1=np.sum(color_1==0)  #统计黑色的像素点个数
    black_index_1=np.where(color_1==0)

    black_count_2=np.sum(color_2==0)  #统计黑色的像素点个数
    black_index_2=np.where(color_2==0)
    #print('black_index',black_index)

    if black_count_1==0:
        black_count_1=1
    if black_count_2==0:
        black_count_2=1
    if list(black_index_1[0])==empty:
        center_1=0
        m.stop()
    else:
        center_1=(black_index_1[0][0]+black_index_1[0][black_count_1-1])/2

    if list(black_index_2[0])==empty:
        center_2=0
        m.stop()
    else:
        center_2=(black_index_2[0][0]+black_index_2[0][black_count_2-1])/2
    center=(center_1+center_2)/2
    print('center',center)
#     #找到黑色点的中心点位置
    #direction=center-320  #于标准中心的偏移量
    #print('direction',direction)
    if center==-320:  #相差太多，说明冲出去了，则小车停止
        #time.sleep(0.007)
        m.stop()
    elif center>370:  #说明中心在右边320+150=430
        #time.sleep(0.007)
        print('turn_right')
        m.turn_left(10,45)
    elif center<270:  #说明中心在左边320-150=170
        #time.sleep(0.007)
        print('turn_left')
        m.turn_right(45,10)
    else:
        print('go')
        #time.sleep(0.007)
        m.go(25,25)
cap.release()
cv2.destroyAllWindows()
'''