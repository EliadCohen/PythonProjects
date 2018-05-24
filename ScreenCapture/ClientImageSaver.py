#Screen capture script for Python 3 Requires FFMPEG executable from:
#http://ffmpeg.zeranoe.com/builds/ Requires Pillow (Python PIL fork)

from PIL import ImageGrab
import time
import os
import subprocess
import datetime
import configparser
from tkinter import *
import winerror

#Read ini
config=configparser.ConfigParser()
config.read(os.path.realpath("settings.ini"))

#Populating globals from config file
filename=config.get('SaveLocation','FileName')

dirname=config.get('SaveLocation','Folder')
if dirname=="":
    dirname=os.getcwd()+"\\"

ext=config.get('CaptureSettings','Extension')

seconds=0


#Global declaration Hardcoded
#filename="screen_capture"
#ext=".jpg"
#dirname="C://SCRShot//"
#seconds=0

#os.chdir('C://SCRShot')

def takescreenshots(sec,dirname):
    #5 second delay followed by save. Should be looped
    i=1
    irange=range(1,sec+1)
    timestamp=str('{:%Y.%m.%d.%H%M}'.format(datetime.datetime.now()))
    global filename
    #global dirname
    filename=timestamp
    os.chdir(dirname)
    try:
        os.mkdir(timestamp)
    except FileExistsError:
        timestamp=timestamp+"_rep"
        filename=timestamp
        os.mkdir(timestamp)
    #dirname=dirname+"/"+timestamp+"/" #When using hardcoded
    dirname=dirname+timestamp+"/" #When using ini file
    os.chdir(dirname)
    
    try:
        for i in irange:
            lb2.set("Frame "+str(i)+"/"+str(sec))
            Tk.update_idletasks(Label2)
            time.sleep(1)
            #ImageGrab.grab().save(dirname+filename+"-"+str(i)+ext, "JPEG")
            ImageGrab.grab().save(dirname+filename+"-"+str(i)+ext, "JPEG")
            #print(i)
            i+=1
    except:
        Label.text="Error"
        

#Save to avi
#subprocess.call(['ffmpeg', '-i', 'picture%d0.png', 'output.avi'])
#subprocess.call('ffmpeg -y -r 1/1 -i '+dirname+filename+"%02d"+ext+' -r 25 output.avi',shell=True)
def exportmovie():
    timestamp=str('{:%Y.%m.%d.%H%M}'.format(datetime.datetime.now()))
    outfilename="out"+str(timestamp)+".avi"
    print(outfilename)
    subprocess.call('ffmpeg -y -r 1/1 -i '+dirname+filename+"-%d"+ext+' -r 25 '+outfilename,shell=True)

def removescreenshots():
    for file in os.listdir(dirname):
        try:
            if file.endswith(".jpg"):
                os.remove(file)
            
        except:
            Label2.text="error"
            pass
        lb2.set("All frames deleted")
def start_minimized_click():
    root.wm_state('iconic')
    start_button_click()
    
def start_button_click():
    global seconds
    try:
        seconds=int(E1.get())
        print(seconds)
        takescreenshots(int(seconds),dirname)
    except ValueError:
        lb2.set("Error! use numbers only and never an empty value")
    #pass

root=Tk()
topframe=Frame(root)
topframe.pack(side=TOP)
midframe=Frame(root)
midframe.pack(side=LEFT)
bottomframe=Frame(root)
bottomframe.pack(side=BOTTOM)

Button1=Button(topframe,text="Start",command=start_button_click)
Button1.pack(side=LEFT)
Button3=Button(topframe,text="Start Minimized",command=start_minimized_click)
Button3.pack(side=RIGHT)
Button4=Button(topframe,text="Minimized + control",command=start_minimized_click).pack()
Button2=Button(topframe,text="Delete all frames",command=removescreenshots)
Button2.pack(side=BOTTOM)

Label1=Label(midframe,text="Capture Period (seconds):")
Label1.pack(side=LEFT)
E1=Entry(midframe)
E1.pack(side=RIGHT)
lb2=StringVar()
lb2.set("Server/Error Message goes in here")
Label2=Label(bottomframe,textvariable=lb2,justify=LEFT)
Label2.pack(side=BOTTOM)

root.mainloop()
