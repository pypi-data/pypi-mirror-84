#!/usr/local/bin/python3

from aip.speech import AipSpeech
import os
import wave
import time
import pyaudio
import audioop
import pygame
import base64

main_path = '/home/pi/class/'#读取和保存文件所用主文件夹
txt_path = main_path+'txt/'#文本文件夹
audio_path = main_path+'speech/'#音频文件夹

def test():
    print('hello lxy!')
    
def hello():
    print('you successful twice')

class Yuyin():
    def __init__(self):
        self.app_id=self.TxtRead(txt_path+'APP_ID.txt')
        self.api_key=self.TxtRead(txt_path+'API_KEY.txt')
        self.secret_key=self.TxtRead(txt_path+'SECRET_KEY.txt')
        
        self.client=AipSpeech(self.app_id,self.api_key,self.secret_key)
    
    #读取文件并保存为字符串
    def TxtRead(self,filename):
        f = open(filename,"r")   
        txt=f.read()
        f.close() 
        return txt
    
    #修改成语音文件格式到适合百度语音api
    def downsampleWav(self,src, dst, inrate=48000, outrate=16000, inchannels=1, outchannels=1):
        if not os.path.exists(src):
            print ('没有旧音频文件')
            return False
 
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
 
        try:
            s_read = wave.open(src, 'rb')
            params = s_read.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            #print(nchannels,sampwidth, framerate,nframes)
            s_write = wave.open(dst, 'wb')
        except:
            print ('打开旧音频文件失败')
            return False
 
        n_frames = s_read.getnframes()
        data = s_read.readframes(n_frames)
 
        try:
            converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
            if outchannels == 1 and inchannels != 1:
                converted = audioop.tomono(converted[0], 2, 1, 0)
        except:
            print ('转换格式失败')
            return False
 
        try:
            s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
            s_write.writeframes(converted[0])
        except Exception as e:
            print(e)
            print ('保存新音频失败')
            return False
 
        try:
            s_read.close()
            s_write.close()
        except:
            print ('无法关闭音频文件')
            return False
        return True

    #录音file_name路径文件名,TIME录音时间长度
    def my_record(self,TIME,file_name):  #录音保存到.wav文件
        CHUNK = 2000 # 采样点
        FORMAT = pyaudio.paInt16
        CHANNELS = 1# 声道
        RATE = 48000 # 采样率
        RECORD_SECONDS = 2# 采样宽度2bytes
        file_name=audio_path+file_name+'.wav'
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

        print("开始录音,请说话......")

        frames = []
        t=time.time()
        while time.time() < t+TIME:
            data = stream.read(CHUNK)
            frames.append(data)

        print("录音结束!")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(file_name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    
        file_new_name=audio_path+'new.wav'
        self.downsampleWav(file_name, file_new_name)
        os.remove(file_name)
        os.rename(file_new_name,file_name)

    # 语音识别返回识别结果字符串   中文普通话识别的免费次数为50000次。            
    def stt(self,filename):  #识别.wav文件中的语音
        try:
            filename=audio_path+filename+'.wav'
            fp=open(filename, 'rb')
            FilePath=fp.read()
            fp.close()
        except:
            print(filename+"音频文件不存在或格式错误")
        finally:
            try:
            # 识别本地文件
                result = self.client.asr(FilePath,
                            'wav',
                            16000,
                            {'dev_pid': 1537,}  # dev_pid参数表示识别的语言类型，1536表示普通话
                            )
            # 解析返回值，打印语音识别的结果
                if result['err_msg']=='success.':
                    word = result['result'][0]      # utf-8编码
                    return word#返回识别结果值
                else:
                    print ("语音识别失败:"+filename)
                    return "语音识别失败"
            except:
                print("没有连接网络")
                return "没有连接网络"
        

    #将文本转为音频  语音合成免费额度只有5000次（未认证），认证之后有50000次，在180天内有效
    def tts(self,txt,filename):
        if len(txt) != 0:
            word = txt
        try:
            result  = self.client.synthesis(word,'zh',1, {
                'vol': 5,'per':0,
            })
            # 合成正确返回audio.mp3，错误则返回dict 
            if not isinstance(result, dict):
                with open(audio_path+filename+'.mp3', 'wb') as f:
                    f.write(result)
                print('文字转音频成功:'+txt)
                f.close()
            else :
                print(txt+'文字转音频失败:'+txt)
        except:
            print('没有连接网络')

    def play_bufen(self,filename,play_time):    
        pygame.mixer.init(frequency=16000,size=-16,channels=1,buffer=2000)
        track = pygame.mixer.music.load(audio_path+filename)
        pygame.mixer.music.play()
        time.sleep(play_time)
        pygame.mixer.music.stop()
    
    # 播放音频及音乐
    def play_music(self,filename,model=0,flag=0,time=0):  #只能播放.mp3文件  model=1是播放音乐，=0是播放音频文件  flag=0是播放全部，=1是播放部分。 time是播放音乐多长时间。
        try:
            try:
                pygame.mixer.init(frequency=16000,size=-16,channels=1,buffer=2000)
                f=filename.split('.')
                if f[1]=='wav':
                    track = pygame.mixer.Sound(audio_path+filename)
                    track.play()#循环次数loops，开始时间start
                
                elif f[1]=='mp3':
                    if model == 0: #播放音频
                        track = pygame.mixer.music.load(audio_path+filename)
                        pygame.mixer.music.play()#循环次数loops，开始时间start
                        
                    elif model==1:   #播放音乐
                        track = pygame.mixer.music.load(audio_path+filename)
                        if flag==0:  #播放全部
                            pygame.mixer.music.play()#循环次数loops，开始时间start
                            while (pygame.mixer.music.get_busy()):  #等待播放完毕
                                if pygame.mixer.music.get_busy()==0:
                                    break;
                                
                        else:  #播放部分
                            self.play_bufen(filename,time)
                
            except:
                print('没有这个音频文件:'+filename)
        except:
            print('没有打开音响')
'''
#测试录音+语音识别       
s=Yuyin()
s.my_record(3,"1")
txt=s.stt("1")
print(txt)
'''
'''
#测试文本转语音
s=Yuyin()
s.tts('你好',"2")  #tts保存为mp3格式
s.play_music('2.mp3')
'''