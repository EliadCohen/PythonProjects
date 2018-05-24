'''
Created on Jun 15, 2017

@author: eliad
'''
from PIL import ImageGrab
import os
import subprocess
from tkinter import *
import configparser 
from builtins import int
import cmd
from subprocess import Popen
import time
import datetime



#ConfigParser
print(os.getcwd())
os.chdir("C:\\Users\\eliad\\Desktop\\Gits\\PythonProjects\\FFMPEGCapture")
print(os.getcwd())
config=configparser.ConfigParser()
config.read("settings.ini")
#print(config)
controllocation=config.get('Locations','controlsoftware' )
#print(controllocation)
movieextension=config.get('FFMPEG_Settings','Extension')
recordingmode=config.get('Settings','RecordingMode')
snaprate=config.get('Settings','SnapRate')


def start_button_click():
    try:
        sec=int(E1.get())
        if sec>=5:
            lb2.set("Capturing "+str(sec)+" seconds")
            Tk.update_idletasks(Label2)
            if str(recordingmode).lower()=='movie':
                ffmpeg_command(sec)
            elif str(recordingmode).lower()=="snapshots":
                takescreenshots(sec)
        else:
            lb2.set("Should be at least 5 seconds to allow for encoder to start")
            Tk.update_idletasks(Label2)
            
    except ValueError:
        lb2.set("Capture period should be numbers only")
        Tk.update_idletasks(Label2)

        
def start_minimized_click():
    
    try:
        os.startfile(controllocation)
        root.wm_state('iconic')
        sec=int(E1.get())
        if sec>=5:
            lb2.set("Capturing "+str(sec)+" seconds")
            #Tk.update_idletasks(Label2)
            if str(recordingmode).lower()=='movie':
                ffmpeg_command(sec)
            elif str(recordingmode).lower()=="snapshots":
                takescreenshots(sec)
                
        else:
            lb2.set("Should be at least 5 seconds to allow for encoder to start")
            Tk.update_idletasks(Label2)
        
    except FileNotFoundError:
        lb2.set("Could not locate control software installation")
        Tk.update_idletasks(Label2)
    
def gen_filename_from_timestamp_and_extension():
    timestamp=str('{:%Y.%m.%d.%H%M}'.format(datetime.datetime.now()))
    return timestamp+movieextension

def ffmpeg_command(sec):
    #cmd1 = ['ffmpeg', '-i','slide.mp4','-y','-vf','fade=in:0:30','slide_fade_in.mp4']
    #ffmpeg -f gdigrab -framerate 6 -i desktop out.mkv
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    cmd1 = ['ffmpeg', '-f','gdigrab','-framerate',config.get('FFMPEG_Settings','Framerate'),'-i','desktop',gen_filename_from_timestamp_and_extension()]
    #cmd2=['ffmpeg', '-f','gdigrab','-framerate','6','-i','desktop',gen_filename_from_timestamp_and_extension()]
    # Starts encoding in a subprocess
    
    proc = subprocess.Popen(cmd1,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,startupinfo=startupinfo)
    #proc = subprocess.Popen(cmd1)
    
    duration = sec
    sleeptime = 0
    while proc.poll() is None and sleeptime < duration: 
        # Wait for the specific duration or for the process to finish
        time.sleep(1)
        sleeptime += 1
    #proc.communicate("q")
    proc.terminate()
  
#     # If process is not terminated
#     if proc.poll() is None:
#         # Cancels process, waits for it to complete
#         proc.communicate("q")
        
    


def takescreenshots(sec):
    #5 second delay followed by save. Should be looped
    i=1
    irange=range(1,sec+1)
    timestamp=str('{:%Y.%m.%d.%H%M}'.format(datetime.datetime.now()))
    #global filename
    #global dirname
    filename=timestamp
#    os.chdir(dirname)
    try:
        os.mkdir(timestamp)
    except FileExistsError:
        timestamp=timestamp+"_rep"
        filename=timestamp
        os.mkdir(timestamp)
    #dirname=dirname+"/"+timestamp+"/" #When using hardcoded
    dirname=os.getcwd()+"\\"+timestamp+"\\" #When using ini file
    os.chdir(dirname)
    
    try:
        for i in irange:
            lb2.set("Frame "+str(i)+"/"+str(sec))
            Tk.update_idletasks(Label2)
            time.sleep(snaprate)
            #ImageGrab.grab().save(dirname+filename+"-"+str(i)+movieextension, "JPEG")
            ImageGrab.grab().save(dirname+filename+"-"+str(i)+".jpg", "JPEG")
            #print(i)
            i+=1
    except:
        lb2.set("Error")

#tkinter constructor

root=Tk()
topframe=Frame(root)
topframe.pack(side=TOP)
midframe=Frame(root)
midframe.pack(side=LEFT)
bottomframe=Frame(root)
bottomframe.pack(side=BOTTOM)

Button1=Button(topframe,text="Start unencoded",command=start_button_click).pack(side=LEFT)

# Button3=Button(topframe,text="Start Minimized",command=start_minimized_click).pack(side=RIGHT)


Button4=Button(topframe,text="Minimized + Mucell control",command=start_minimized_click).pack()
# Button2=Button(topframe,text="Delete all frames",command=removescreenshots).pack(side=BOTTOM)

Label1=Label(midframe,text="Capture Period (seconds):")
Label1.pack(side=LEFT)
E1=Entry(midframe)
E1.pack(side=RIGHT)
lb2=StringVar()
lb2.set("Server/Error Message goes in here")
Label2=Label(bottomframe,textvariable=lb2,justify=LEFT)
Label2.pack(side=BOTTOM)

lb3=StringVar()
lb3.set("Control software installed at: "+controllocation)
Label3=Label(bottomframe,textvariable=lb3,justify=LEFT)
Label3.pack(side=BOTTOM)

root.mainloop()