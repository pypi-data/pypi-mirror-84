import shijue
import gpio
import yuyin
import time
import cv2
from PIL import Image

start = 0           # 是否启动车的标记
camera = 0          # 是否开启摄像头的标记
xunxian_mark = 0    # 是否打开寻线模式的标记
park_enter = 0      # 是否到达停车场入口标记
park_num = 'none'   # 目标停车区域
ret = 0             # 用来标记是否播报总时间
i = 0               # 用于给检测图像产生时延
j = 0               # 用于给数字识别的图片命名
j_color = 0         # 用于给红色识别的图片命名
red_is_gone = 0     # 用于判断是否已经过了红绿灯
speak = 0           # 用于结束时播报语音
k = 'none'
# 照片存储的绝对路径
img_path ='/home/pi/camera_pos/'
# 车子进入停车场后所拍摄数字图像的保存路径 
img_path_pre = img_path+'3.jpg'
# name=0  #存储异常识别的情况
car_1 = gpio.car(1, 2)
car_1.setspeed('go',25,25)                      # 设置车子的前进速度，第一个数字参数是左轮速度
car_1.setspeed('turn_left', 3, 23)            # 设置车子的左转速度，同上
car_1.setspeed('turn_right', 23, 3)           # 设置车子的右转速度，同上
cam = cv2.VideoCapture(0)                       # 初始化摄像头0，整个过程摄像头一直开着，只是平时不识别，到等待线才开始识别而已。
er = shijue.erweima_recognize()                 # 实例化一个二维码识别器
red = shijue.color_detect('red')                # 实例化一个红色检测器
red.setcolorvalue('red', [1, 210, 200], [6,255,255])    # 对红色检测的阈值进行设置，分别对应h s v
blue = shijue.color_detect('blue')              # 实例化一个蓝色检测器
num = shijue.model_recognize('lxy1007.proto')   # 实例化一个数字检测器  数字和方向是两个模型文件
mdir = shijue.model_recognize('lxy1007.proto')  # 实例化一个方向检测器
speaker = yuyin.Yuyin()                         # 实例化一个语音交互器
car_1.stop()                                    # 使小车停止

#vo = {'左转' : 'turn_left', '右转' : 'turn_right'}# 用于将mdir.data的文本对应为响应的英文
ddir = ['左转','右转']                            # 用来判断 mdir.data 是不是其中的字符串
ndir = ['none','左转','右转']

def begin(s):
    global xunxian_mark
    global start
    
    if s==0:
        ret, img = cam.read()
        er.recognize(img)
        print('er.data', er.data)
        if er.data =="none":
            print("nothing")
        else:
            cv2.destroyAllWindows()
            xunxian_mark = 1
            time_start = time.time()
            start = 1
            return  time_start

def run(mdir, car_1):
    global xunxian_mark
    global camera
    global k
    if mdir in ddir:
        print('小车'+mdir)
        if mdir =='左转':
            print(mdir)
            car_1.turn_left()
        elif mdir =='右转':
            car_1.turn_right()
            print(car_1.dec)
        if car_1.dec =='yes':
            car_1.stop()
            camera = 0
            xunxian_mark = 1
            print('xunxian_mark', xunxian_mark)
        cv2.destroyAllWindows()
        k = car_1.dec
    # return camera, xunxian_mark
 
def run1(num, car_1):
    global xunxian_mark
    global park_enter
    global park_num
    if num not in ndir:
        if num == park_num:  #匹配到了
            speaker.tts('匹配','car')
            speaker.play_music('car.mp3')
            time.sleep(1)
            car_1.turn_left()
            if car_1.dec == 'yes':
                car_1.stop()
                xunxian_mark = 1
                park_enter = 2
                print('匹配')
            cv2.destroyAllWindows()
        else:
            speaker.tts('不匹配','car')
            speaker.play_music('car.mp3')
            time.sleep(1)
            car_1.go()
            if car_1.dec == 'yes':
                car_1.stop()
                xunxian_mark = 1
                park_enter = 1
                print('不匹配')
                # cv2.destroyAllWindows()
            cv2.destroyAllWindows()   

def commun(num, car_1):
    global xunxian_mark
    global park_num
    global park_enter
    global camera
    if num == '语音':
            #寻线标志一直都是打开的
            print('语音控制区')
            speaker.tts('请发出指令','car')
            speaker.play_music('car.mp3')
            time.sleep(2)

            speaker.my_record(3, "car_yuyin")
            txt=speaker.stt("car_yuyin")
            print('识别到的指令为：',txt)
            if "一" in txt or "1" in txt:
                park_num = '1'
            elif "二" in txt or "2" in txt:
                park_num = '2'
            elif "三" in txt or "3" in txt:
                park_num = '3'
                
            if park_num != 'none':  #说明已经得到了停车位的数字
                print('目标区域',park_num)
                speaker.tts('目标停车位为：'+park_num+'进入停车场','car')
                speaker.play_music('car.mp3')
                time.sleep(4)
                car_1.go()
                if car_1.dec == 'yes':
                    car_1.stop()
                    camera = 0
                    xunxian_mark = 1
                    park_enter = 1
                    cv2.destroyAllWindows()
    # return xunxian_mark, camera, park_enter, park_num

def red_det(red, car_1, num):
    global xunxian_mark
    global red_detect
    global camera
    if red == 'red':
        if num not in dir:
            car_1.stop()  #小车停止相应秒数
            speaker.tts('识别到红灯，小车停止'+num+'秒','car')
            speaker.play_music('car.mp3')
            time.sleep(4)
            print('小车停止'+num+'秒')
            time.sleep(int(num))
            print('停止完毕')
            car_1.go()
            if car_1.dec =='yes':
                car_1.stop()
                red_detect = 'none'
                xunxian_mark = 1
                camera = 0
                cv2.destroyAllWindows()
    # return red_detect, xunxian_mark, camera  
            

def end(car_1, time_start):
    global xunxian_mark
    global camera
    global speak
    global ret
    ret,img = cam.read()
    xunxian_mark=0  #关闭寻线
    camera=1   #供多次扫描二维码
    
    print('停车完成')
    print('开始扫描停车二维码')
    if speak == 0:
        speaker.tts('停车完成，开始扫描停车二维码','car')
        speaker.play_music('car.mp3')
        time.sleep(4)
        speak=1
    er.recognize(img)  
    if er.data == 'stop':
        time_end = time.time()
        cv2.destroyAllWindows()
        car_time = int(time_end-time_start)
        print("小车运动时间为：",car_time)
        #语音播报运动时间
        time_total = "所用总时间为："+str(car_time)+"秒"
        speaker.tts(time_total,'car')
        speaker.play_music('car.mp3')
        time.sleep(3)
        ret = 1
    # return xunxian_mark, camera, ret
    
if __name__=="__main__":
    y = 0
    car_1.stop()
    while y == 1:
        time_start = begin(start)
        if xunxian_mark == 1:
            car_1.xunxian()
        camera = car_1.came
        if camera == 1 and park_enter == 0:
            ret,img=cam.read()
            blue.detect(img)
            img_new=blue.img_new
            cv2.imshow('img_new',img_new)
            cv2.waitKey(40)
            cv2.imwrite(img_path_pre, img_new)
            frame = Image.open(img_path_pre)
            xunxian_mark=0
            i+=1
            #print('i:',i)
            if i==1:
                cv2.destroyAllWindows()
                print('开始检测红色和方向')
                if red_is_gone == 0:
                    red.detect(img)  #检测红色
                    red_detect=red.data
                img_path_color = img_path+red_detect+'/'+str(j_color)+'.jpg'
                cv2.imwrite(img_path_color, img)
                j_color +=1
                
                num.recognize(frame)
                mdir.recognize(frame)  #检测数字
                i=0
                print('mdir:',mdir.data)
                # 保存识别到的数字方向图片到对应的文件夹
                img_path_mdir = img_path+mdir.data+'/'+str(j)+'.jpg'
                print('img_path_mdir', img_path_mdir)
                cv2.imwrite(img_path_mdir, img_new)
                j+=1
                
                speaker.tts('识别到'+mdir.data,'car')
                speaker.play_music('car.mp3')
                time.sleep(2)
                run(mdir.data, car_1)
                commun(num.data, car_1) 
                red_det(red_detect, car_1, num.data)
        elif camera == 1 and park_enter == 1:
            j = 100
            xunxian_mark=0
            ret,img=cam.read()
            ret,img=cam.read()
            ret,img=cam.read()
            ret,img=cam.read()
            ret,img=cam.read()
            blue.detect(img)
            img_new=blue.img_new
            cv2.imwrite(img_path,img_new)
            frame = Image.open(img_path)
            cv2.imshow('img_new',img_new)
            cv2.waitKey(40)
            print('进入停车区')
            i=i+1
            if i==23:
                
                cv2.imwrite(img_path_pre, img_new)
                frame = Image.open(img_path_pre)
                
                num.recognize(frame)   #识别停车场内的数字
                print('停车区域的数字：', num.data)
                cv2.destroyAllWindows()
                # 保存停车场拍摄的照片
                img_path_num =img_path+num.data+'/'+str(j)+'.jpg'
                cv2.imwrite(img_path_num, img_num)
                j += 1
                speaker.tts('当前停车位为：'+num.data,'car')
                speaker.play_music('car.mp3')
                time.sleep(2)
                i=0
                
                run1(num.data, park_num, car_1)
        elif camera == 1 and park_enter ==2:
            end(car_1, time_start)
            if ret == 1:
                break