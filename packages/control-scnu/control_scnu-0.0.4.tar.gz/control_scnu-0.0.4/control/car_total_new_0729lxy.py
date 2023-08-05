import shijue
import gpio
import yuyin
import time
import cv2
from PIL import Image

start = 0  # 是否启动车的标记
camera = 0  # 是否开启摄像头的标记
xunxian_mark = 0  # 是否打开寻线模式的标记

park_enter = 0  # 是否到达停车场入口标记
park_num = 'none'  # 目标停车区域
i = 0
j=0
j_color=0
red_is_gone=0
speak = 0
img_path = '/home/pi/Desktop/camera_pos/'
# name=0  #存储异常识别的情况
car_1 = gpio.car(1, 2)
car_1.setspeed('go',20,20)
car_1.setspeed('turn_left',3,20.5)
car_1.setspeed('turn_right',20.5,3)
cam = cv2.VideoCapture(0)  # 初始化摄像头0，整个过程摄像头一直开着，只是平时不识别，到等待线才开始识别而已。
er = shijue.erweima_recognize()   # 实例化一个二维码识别器
red = shijue.color_detect('red')  # 实例化一个红色检测器
t = [1, 210, 200]
s=[6,255,255]
red.setcolorvalue('red', t, s)
blue = shijue.color_detect('blue')
num = shijue.model_recognize('lxy1007.proto')  # 实例化一个数字检测器  数字和方向是两个模型文件
mdir = shijue.model_recognize('lxy1007.proto')
speaker = yuyin.Yuyin()
car_1.stop()
while 1:
    #car_1.stop()
    if start == 0:
        ret, img = cam.read()
        er.recognize(img)
        print('er.data', er.data)
        if er.data =="none":
            print(1)
        else:
            #print(2)
            cv2.destroyAllWindows()
            xunxian_mark = 1
            time_start = time.time()
            start = 1
        
    if xunxian_mark == 1:
        car_1.xunxian()
    camera = car_1.came

    if camera == 1 and park_enter == 0:  # camera==1,说明是遇到等待线了, prak_enter=0,说明还没进入停车场，所以只能是十字路口，红绿灯、语音控制区
        ret, img = cam.read()
        blue.detect(img)
        #red.detect(img)
        #red_detect=red.data
        img_new = blue.img_new
        cv2.imshow('img', img)
        cv2.imshow('img_new', img_new)
        cv2.waitKey(40)
        img_path_pre = '/home/pi/Desktop/camera_pos/0.jpg'
        cv2.imwrite(img_path_pre, img_new)
        frame = Image.open(img_path_pre)
        xunxian_mark = 0
        i = i+1
        print('i:',i)
        if i == 20:
            print('开始检测红色和方向')
            if red_is_gone==0:
                red.detect(img)  # 检测红色
                red_detect = red.data
            img_path_color = '/home/pi/Desktop/camera_pos/'+red_detect+'/'+str(j_color)+'.jpg'
            cv2.imwrite(img_path_color, img)
            j_color=j_color+1
            
            num.recognize(frame)
            mdir.recognize(frame) 
            i = 0
            print('mdir:', mdir.data)
            #保存识别到的数字方向图片到对应的文件夹
            img_path_mdir = '/home/pi/Desktop/camera_pos/'+mdir.data+'/'+str(j)+'.jpg'
            print('img_path_mdir',img_path_mdir)
            cv2.imwrite(img_path_mdir, img_new)
            j=j+1
            
            speaker.tts('识别到'+mdir.data, 'car')
            speaker.play_music('car.mp3')
            time.sleep(2)
            if mdir.data == '左转':
                print('小车左转')
                car_1.turn_left()  # 小车左转
                time.sleep(1)
                camera = 0  # 最后处理完都得关掉摄像头
                xunxian_mark = 1
                cv2.destroyAllWindows()

            elif mdir.data == '右转':
                print('小车右转')
                car_1.turn_right()  # 小车右转
                time.sleep(1)
                camera = 0  # 最后处理完都得关掉摄像头
                xunxian_mark = 1
                cv2.destroyAllWindows()
                
            elif num.data == '语音':
                # 寻线标志一直都是打开的
                print('语音控制区')
                speaker.tts('请发出指令', 'car')
                speaker.play_music('car.mp3')
                time.sleep(2)

                speaker.my_record(3, "car_yuyin")
                txt = speaker.stt("car_yuyin")
                print('识别到的指令为：', txt)
                if "一" in txt or "1" in txt:
                    park_num = '1'
                elif "二" in txt or "2" in txt:
                    park_num = '2'
                elif "三" in txt or "3" in txt:
                    park_num = '3'
                    
                if park_num != 'none':  # 说明已经得到了停车位的数字
                    print('目标区域', park_num)
                    speaker.tts('目标停车位为：'+park_num+',进入停车场', 'car')
                    speaker.play_music('car.mp3')
                    time.sleep(4)
                    car_1.go()
                    time.sleep(1)
                    camera = 0
                    xunxian_mark = 1
                    park_enter = 1  # 已进入停车区，下次不会再进来这里
                    # 然后关闭摄像头
                    cv2.destroyAllWindows()
                    
            if red_detect == 'red':
                 if num.data != 'none' and num.data != '左转' and num.data != '右转':
                    car_1.stop()  #小车停止相应秒数
                    speaker.tts('识别到红灯，小车停止'+num.data+'秒', 'car')
                    speaker.play_music('car.mp3')
                    time.sleep(4)
                    print('小车停止'+num.data+'秒')
                    time.sleep(int(num.data))
                    print('停止完毕')
                    car_1.go()
                    time.sleep(1.2)
                    red_detect = 'none'
                    red_is_gone=1  #标记红色检测已经过了
                    camera = 0  # 然后关闭摄像头
                    xunxian_mark = 1  # 停止后，打开寻线
                    cv2.destroyAllWindows()
            
    elif camera==1 and park_enter==1:  # 停到等待线了，而且得到了停车区的数字,就开始匹配了
        j=100  #100以后的照片是停车场拍摄的
        xunxian_mark = 0
        ret, img = cam.read()
        blue.detect(img)
        img_new = blue.img_new
        img_path_pre = '/home/pi/Desktop/camera_pos/0.jpg'
        cv2.imwrite(img_path_pre, img_new)
        frame = Image.open(img_path_pre)
        cv2.imshow('img_new', img_new)
        cv2.waitKey(40)
        #print('进入停车区')
        i = i+1
        if i == 20:
            num.recognize(frame)   # 识别停车场内的数字
            print('停车区域的数字：', num.data)
            
            #保存停车场拍摄的照片
            img_path_num = '/home/pi/Desktop/camera_pos/'+num.data+'/'+str(j)+'.jpg'
            cv2.imwrite(img_path_num, img_new)
            j=j+1
            
            speaker.tts('当前停车位为：'+num.data, 'car')
            speaker.play_music('car.mp3')
            time.sleep(2)
            i = 0
            if num.data != 'none' and num.data != '左转' and num.data != '右转':
                if num.data == park_num:  # 匹配到了
                    speaker.tts('匹配', 'car')
                    speaker.play_music('car.mp3')
                    time.sleep(1)
                    car_1.turn_left()
                    time.sleep(1.2)
                    xunxian_mark = 1
                    park_enter = 2 # 匹配到，打开寻线之后就不会再进入这个elif了
                    print('匹配')
                    cv2.destroyAllWindows()
                else:
                    speaker.tts('不匹配', 'car')
                    speaker.play_music('car.mp3')
                    time.sleep(1)
                    car_1.go()
                    time.sleep(2.1)
                    xunxian_mark = 1
                    # park_enter=1  #不匹配，就继续寻找
                    print('不匹配')
                    cv2.destroyAllWindows()

    elif camera == 1 and park_enter == 2:  # 说明车停好了
        ret, img = cam.read()
        xunxian_mark = 0  # 关闭寻线
        camera = 1   # 供多次扫描二维码
        print('停车完成')
        print('开始扫描停车二维码')
        if speak == 0:
            speaker.tts('停车完成，开始扫描停车二维码', 'car')
            speaker.play_music('car.mp3')
            time.sleep(4)
            speak = 1
        er.recognize(img)  
        if er.data != 'none':
            time_end = time.time()
            cv2.destroyAllWindows()
            car_time = int(time_end-time_start)
            print("小车运动时间为：", car_time)
            # 语音播报运动时间
            time_total = "所用总时间为："+str(car_time)+"秒"
            speaker.tts(time_total, 'car')
            speaker.play_music('car.mp3')
            time.sleep(3)
            break    

