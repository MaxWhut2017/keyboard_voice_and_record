from pynput import keyboard,mouse
import time
import os
from datetime import date
import threading
import win32api,win32con
import re
import pygame
import tkinter
#from pydub import AudioSebment
#from pydub.playback import play
from playsound import playsound


#global values
today=date.today()
fw=open("niki.txt","a",encoding="utf-8")
this_time_doc=""
time_last_typedin=0
bscnt=0
entercnt=0
spccnt=0
new_mesg=False
pm="music_stater"
CapsLkCnt=0
is_bb=1
x=0
y=0
click_renzoku=0
last_key_pressed=""

def is_should_voice(change_state_of_bb):
    global is_bb
    global CapsLkCnt
    if change_state_of_bb==True:#cl:
        if CapsLkCnt==1:#按过一次capslock了，time to改变bb状态
            CapsLkCnt=0;
            is_bb=1-is_bb
        else:
            CapsLkCnt=1 #下次再按再改
    else:#没按capslock
        CapsLkCnt=0
    #大部分时候返回未经修饰的is_bb
    print(is_bb,CapsLkCnt)
    return is_bb==1
    
class Clock_show(threading.Thread):#Clock feature
    def __init__(self):
        super(Clock_show, self).__init__()  # 重构run函数必须要写
    def run(self):
        root =tkinter.Tk()
        root.title('入门案例')
        timestr=tkinter.StringVar() 
        timestr=tkinter.StringVar()
        timestr.set(time.strftime('%H:%M:%S', time.localtime(time.time())))
        w = tkinter.Label(root, bg='black', textvariable=timestr,fg='white',font=("微软雅黑",40))  
        w.pack()  
    
        root.overrideredirect(1)                 # 去除窗口边框
        root.wm_attributes("-alpha", 1)        # 透明度(0.0~1.0)
        root.wm_attributes("-toolwindow", True)  # 置为工具窗口(没有最大最小按钮)
        root.wm_attributes("-topmost", True)     # 永远处于顶层
        #root.image = tkinter.PhotoImage(file='black.png')
        #root.overrideredirect(True)#图片设置
    
        def StartMove(event):
            global x, y
            x = event.x
            y = event.y
 
        def StopMove(event):
            global x, y
            x = None
            y = None
 
        def OnMotion(event):
            global x, y
            deltax = event.x - x
            deltay = event.y - y
            root.geometry("+%s+%s" % (root.winfo_x() + deltax, root.winfo_y() + deltay))
            root.update()
            print(event.x,event.y,root.winfo_x(),root.winfo_y(),root.winfo_width(),root.winfo_height())
 
        root.bind("<ButtonPress-1>", StartMove) #监听左键按下操作响应函数
        root.bind("<ButtonRelease-1>", StopMove) #监听左键松开操作响应函数
        root.bind("<B1-Motion>", OnMotion)   #监听鼠标移动操作响应函数
    

        def gettime():
            print("getting")
            timestr.set(time.strftime('%H:%M:%S', time.localtime(time.time())))
            #time.sleep(1)
            root.after(1000,gettime) 
        
        root.after(1000,gettime) 
    
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        ww=220
        wh=60
        x = (sw-ww)*0.85
        y = (sh-wh)*0.85  
        root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
    
        root.mainloop()
    
class play_oyasumi(threading.Thread):#and show warning box
    def __init__(self):
        super(play_oyasumi, self).__init__()  # 重构run函数必须要写
        
    def run(self):
        
        print("pygame init")
        global pm  
        pm=pygame.mixer
        filepath = os.getcwd()+"/"+"music/Startup.mp3"
        pm.init(buffer=10)#buffer越大，播放延迟就越大
 

        # 加载音乐
        pm.music.load(filepath)
        pm.music.play(start=0)
        #播放时长，没有此设置，音乐不会播放，会一次性加载完
        time.sleep(10)
        pm.music.stop() 
        
        win32api.MessageBox(0, "Big Panda is WATCHING you!", "１９８４",win32con.MB_ICONWARNING)
        #第一键一定不是点击中央就是Enter         
        
class time_press_click_sound(threading.Thread):
    def __init__(self,press):
        super(time_press_click_sound, self).__init__()  # 重构run函数必须要写
        self.press=press
        
    def run(self):  
        global pm
        global click_renzoku
        global last_key_pressed
        global time_last_typedin
        time_num=time.time()
        
        if self.press==last_key_pressed and self.press!="Click" and float(time_num)-time_last_typedin<0.1:
            if click_renzoku<3:
                click_renzoku+=1
            elif click_renzoku==3:
                pm.music.load(os.getcwd()+"/"+"music/guruguru.mp3")
                pm.music.play(start=0.0)
                click_renzoku+=13
                return
            elif click_renzoku<45: 
                click_renzoku+=1
                return
            else:
                click_renzoku=3
                return
        else:
            click_renzoku=0
        last_key_pressed=self.press
        
        if self.press=="Click":
            pm.music.load(os.getcwd()+"/"+"music/Click.mp3")
            pm.music.play(start=0.0)
        else:
            if self.press=="Key.space":#空格
                pm.music.load(os.getcwd()+"/"+"music/space.mp3")
                pm.music.play(start=0.0)
            elif self.press=="Key.backspace":#退格
                pm.music.load(os.getcwd()+"/"+"music/backspace.mp3")
                pm.music.play(start=0.0)
            elif self.press=="Key.enter":#回车
                pm.music.load(os.getcwd()+"/"+"music/enter.mp3")
                pm.music.play(start=0.0)  
            elif self.press=="Key.ctrl_l" or self.press=="Key.ctrl_r":#ctrl
                pm.music.load(os.getcwd()+"/"+"music/ctrl.mp3")
                pm.music.play(start=0.0)      
            elif self.press=="Key.shift":#shift left
                pm.music.load(os.getcwd()+"/"+"music/shift.mp3")
                pm.music.play(start=0.0)  
            elif self.press=="Key.shift_r":#shift right
                pm.music.load(os.getcwd()+"/"+"music/shift_on.mp3")
                pm.music.play(start=0.0) 
            elif self.press=="Key.tab":#tab
                pm.music.load(os.getcwd()+"/"+"music/tab.mp3")
                pm.music.play(start=0.0) 
            elif (self.press=="Key.alt_l" or self.press=="Key.alt_r"):#alt
                pm.music.load(os.getcwd()+"/"+"music/tab.mp3")
                pm.music.play(start=0.0) 
            elif self.press=="Key.delete":#delete
                pm.music.load(os.getcwd()+"/"+"music/delete.mp3")
                pm.music.play(start=0.0) 
            elif self.press=="Key.caps_lock":#capslock
                pm.music.load(os.getcwd()+"/"+"music/capslock_on.mp3")
                pm.music.play(start=0.0)   
            elif self.press=="Key.esc":#esc
                pm.music.load(os.getcwd()+"/"+"music/exit.mp3")
                pm.music.play(start=0.0)    
                
            elif self.press=="Key.up":#上
                pm.music.load(os.getcwd()+r"/"+r"music/up.mp3")
                pm.music.play(start=0.0) 
            elif self.press=="Key.down":#下
                pm.music.load(os.getcwd()+"/"+"music/down.mp3")
                pm.music.play(start=0.0) 
            elif self.press=="Key.left":#左
                pm.music.load(os.getcwd()+"/"+"music/left.mp3")
                pm.music.play(start=0.0) 
            elif self.press=="Key.right":#右
                pm.music.load(os.getcwd()+"/"+"music/right.mp3")
                pm.music.play(start=0.0)     
            
            elif ((self.press in ['q','w','e','r','t','a','s','d','f','g','z','c','x','v','b'])):#左手字母
                #playsound('music/music/normal_type.mp3')
                pm.music.load(os.getcwd()+"/"+"music/normal_type.mp3")
                pm.music.play(start=0.0) 
                
                    
                    
            elif ((self.press in ['y','u','i','o','p','h','n','j','m','k','l'])):#右手字母
                #playsound('music/music/blank.mp3')
                pm.music.load(os.getcwd()+"/"+"music/blank.mp3")
                pm.music.play(start=0.0)
            
            elif ((self.press in ['Q','W','E','R','T','A','S','D','F','G','Z','C','X','V','B'])):#左手字母大写
                #playsound('music/music/normal_type.mp3')
                pm.music.load(os.getcwd()+"/"+"music/normal_type.mp3")
                pm.music.play(start=0.0) 
            elif ((self.press in ['Y','U','I','O','P','H','N','J','M','K','L'])):#右手字母大写
                #playsound('music/music/blank.mp3')
                pm.music.load(os.getcwd()+"/"+"music/blank.mp3")
                pm.music.play(start=0.0)                 
            elif (self.press<="9" and self.press>="0"):#数字
                pm.music.load(os.getcwd()+"/"+"music/capslock_off.mp3")
                pm.music.play(start=0.0)    
                
            elif self.press==";" or self.press==":":
                pm.music.load(os.getcwd()+"/"+"music/semicolon.mp3")#分号
                pm.music.play(start=0.0)
            elif self.press=="," or self.press==".":
                pm.music.load(os.getcwd()+"/"+"music/semicolon.mp3")#逗号
                pm.music.play(start=0.0)   
            else:#啥也不是，最有可能是符号，小概率是某个未收录快捷键
                pm.music.load(os.getcwd()+"/"+"music/symbol.mp3")
                pm.music.play(start=0.0)
               
def small_keyboard_handle(k):
    #pynput对小键盘支持不足，所以不再处理任何小键盘输入。一些人不喜欢用小键盘，还有些人电脑根本没有小键盘所以影响不大
    print(k)
    pressed=str('{0}'.format(k))
    #判断小键盘,如果是，写入文件，返回是
    
    return False#不是小键盘
    
def handle_backspace(cmd):#其实还handle了enter和space，懒得改函数名
    global bscnt
    global entercnt
    global spccnt
    global fw
    if cmd=="clrbs" and bscnt!=0:
        fw.write("「Backspace*"+str(bscnt)+"」") 
        bscnt=0;
    elif cmd=="clrspc" and spccnt!=0:
        fw.write("「Space*"+str(spccnt)+"」") 
        spccnt=0
    elif cmd=="clrent" and entercnt!=0:
        fw.write("「Enter*"+str(entercnt)+"」") 
        entercnt=0
    elif cmd=="plusent":
        entercnt+=1
    elif cmd=="plusbs":
        bscnt+=1
    elif cmd=="plusspc":
        spccnt+=1
       
def on_press(key):
    time_num=time.time()
    global fw
    global time_last_typedin 
    global new_mesg
    try:#一般键
        pressed=str(format(key.char))
        print(pressed)
        if not small_keyboard_handle(key) and is_should_voice(False):#当且仅当可以发出声音而且不是小键盘特殊声音
            t=time_press_click_sound(pressed)
            t.start()
        
        handle_backspace("clrbs")
        handle_backspace("clrent")
        handle_backspace("clrspc")
        #if float(time_num)-time_last_typedin>4.0: #条件：键盘敲击隔了4.7s以上
        if new_mesg==True:    
            new_mesg=False
            if time_last_typedin!=0:
                fw.write("\n")
            fw.write(str(time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())))+"\n  ")
        if pressed!="None":
            fw.write(pressed)


            
            
    except AttributeError:#特殊键
        pressed=str('{0}'.format(key))
        print(pressed)
        if is_should_voice(pressed=="Key.caps_lock"):
            print("bb")
            t=time_press_click_sound(pressed)
            t.start()
        else:print("不bb")
            
        is_write=False
        if pressed!="Key.backspace":
            handle_backspace("clrbs")
        if pressed!="Key.space":
            handle_backspace("clrspc")
        if pressed!="Key.enter":
            handle_backspace("clrent") 
        
        #if float(time_num)-time_last_typedin>4.7: #条件：键盘敲击隔了2s以上
        if new_mesg==True:    
            new_mesg=False
            if time_last_typedin!=0:
                fw.write("\n")           
            fw.write(str(time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())))+"\n  ") 
        
        if pressed=="Key.backspace":
            handle_backspace("plusbs")
        elif pressed=="Key.enter":
            handle_backspace("plusent")
        elif pressed=="Key.space":
            handle_backspace("plusspc")
        else:
            is_write = True
        
        if is_write:
            if pressed!="None":
                fw.write("「"+pressed[4:]+"」")
            
            
    time_last_typedin=time_num
  

def on_release(key):
    do_nothing=True
    #松开什么键不重要
    #global fw
    #global time_last_typedin
    #try:
    #    do_nothing=True
    #except AttributeError:
        #    
        #time_num=time.time()
        #print('{0} rls'.format(key))
        #release_info=str('{0} rls'.format(key))
        # 
        #if int(time_num)-time_last_typedin>2:
        #    if time_last_typedin!=0:
        #       fw.write("\n")
        #    fw.write(str(int(time_num)))
        #time_last_typedin=time_num
        # 
        # fw.write(release_info)

def on_click(x, y , button, pressed):
    if pressed: 
        if is_should_voice(False):
            t=time_press_click_sound("Click")
            t.start()            
        global new_mesg
        new_mesg=True

    #global fw
    #global time_last_typedin
    #if pressed:     
    #    if time_last_typedin!=0:
    #       fw.write("\n")           
    #       #fw.write("「"+pressed[4:]+"」"+"\n  ") 
    #    fw.write(str(time.strftime('%m.%d %H:%M:%S ',time.localtime(time.time())))+"\n  ")
    #    fw.write('{0} at {1}'.format('Pressed: ', (x, y)))
    #    if time_last_typedin==0:
    #        fw.write("\n")

   
#def on_move(key):
#   do_nothing=True
  
def doc_save(): #
    global fw        #Notice: use global variable! 
    fw.flush()
    print("saved!")  
    #if is_should_voice(False):    
    #   t=time_press_click_sound(-1)
    #   t.start()
    
    
class RepeatingTimer(threading.Timer): 
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)

class mouse_listen(threading.Thread):
    def __init__(self):
        super(mouse_listen, self).__init__()  # 重构run函数必须要写

    def run(self):
        print("mouse listen\n")
        with mouse.Listener( on_click = on_click ) as listener:
            while True:
                listener.join() 
        #第一键一定不是点击中央就是Enter     


        
def main():
    t3=play_oyasumi()
    t3.start()
    #time.sleep(10)
    t1 = RepeatingTimer(4.8, doc_save)   
    t1.start() 
    #加鼠标之后效率明显变低，也将导致记录文件大小过大  
    t2 = mouse_listen()
    t2.start() 
    t4=Clock_show()
    t4.start()
    
    with keyboard.Listener(
        on_press = on_press,
        on_release = on_release)as listener:
        global fw
        localtime=time.asctime( time.localtime(time.time()) )
        fw.write(localtime+"\n")
        fw.close()
        global today
        if not os.path.exists(str(today)):
            os.mkdir(str(today))
        os.chdir(str(today))
        global this_time_doc
        for i in time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())):
            if i==" ":
                this_time_doc+="_"
            elif i==":":
                this_time_doc+="."
            else:
                this_time_doc+=i
        this_time_doc+=".txt"
        fw=open(this_time_doc,"w",encoding="utf-8")
        fw.write(localtime+"\n")
        os.chdir("../")
        print("醒了，开始监听:")
        while True:
            listener.join()
       
   
    
        
if __name__ == "__main__":
    main()
  
  
  
  

  
