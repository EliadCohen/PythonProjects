from tkinter import *
import os
import subprocess
from tkinter.filedialog import askdirectory  

#globals
#dirname=os.curdir
dirname=os.getcwd()
dir_list=os.walk(dirname)
folderdictionary=['Select Folder']

def analyze_dir():
    #For each subfolder shows bulleted list of movies that can be created
    #Convention - each folder should have the name of the jpgs inside without the index
    os.chdir(dirname)
    global dir_list
    global FileSelector
    global folderdictionary
    global radval
    dir_list = os.walk('.')
    i=1
    for subdir,subdirlist,filelist in dir_list:
        for folder in subdirlist:
            FileSelector=Radiobutton(root, 
                        text=folder,
                        padx = 20, 
                        variable=radval, 
                        value=i).pack(anchor=W) 
            folderdictionary.append(folder)
            i+=1
            print(folder)
        
    print(folderdictionary)
    
def removescreenshots(dirname):
    for file in os.listdir(dirname):
        if file.endswith(".jpg"):
            os.remove(dirname+"/"+file)
    os.removedirs(dirname)
    
def make_movie_clean():
    #timestamp=str('{:%Y.%m.%d.%H%M}'.format(datetime.datetime.now()))
    outfilename="out"+folderdictionary[radval.get()]+".avi"
    print(outfilename)
    subprocess.call('ffmpeg -y -r 1/1 -i '+dirname+"/"+folderdictionary[radval.get()]+"/"+folderdictionary[radval.get()]+"-%d"+".jpg"+' -r 25 '+outfilename,shell=True)    
    
    removescreenshots(dirname+"/"+folderdictionary[radval.get()])
    
def make_movie():
    #timestamp=str('{:%Y.%m.%d.%H%M}'.format(datetime.datetime.now()))
    outfilename="out"+folderdictionary[radval.get()]+".avi"
    print(outfilename)
    subprocess.call('ffmpeg -y -r 1/1 -i '+dirname+"/"+folderdictionary[radval.get()]+"/"+folderdictionary[radval.get()]+"-%d"+".jpg"+' -r 25 '+outfilename,shell=True)    
    
def browse_folder():
    global dirname
    dirname=askdirectory()
    print(dirname)
    
root = Tk()
leftframe=Frame(root)
leftframe.pack(side=LEFT)
rightframe=Frame(root)
rightframe.pack(side=RIGHT)

#f1=tkinter.tix.DirSelectBox(leftframe)
#f1.pack()
browsebutton=Button(leftframe,text="Browse",command=browse_folder).pack()

AnalyzeButton=Button(rightframe,text="Analyze directory",command=analyze_dir)
AnalyzeButton.pack(side=TOP)

RunButton=Button(rightframe,text="Make Movie",command=make_movie).pack()
RunButton=Button(rightframe,text="Make Movie and clean frames",command=make_movie_clean).pack()

radval=IntVar()
FileSelector=Radiobutton(root,text="Select Folder",variable=radval,value=0).pack()
#fs = tkinter.tix.ExFileSelectBox(root, directory="C:/SCRShot")
#fs.pack()

root.mainloop()

