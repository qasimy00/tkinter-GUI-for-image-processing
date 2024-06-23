from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image,ImageOps
import numpy as np
import cv2
import os
global frameno

root=Tk()
root.title("DIP")
root.geometry("1280x720")
root.configure(bg='#8b63d2')
my_image_label=Label()
modifiedimage_label=Label()
averagefilter_img_label=Label()
laplacian_img_label=Label()
hist_img_label=Label()
prevbutton=Label()
nextbutton=Label()
frameno=0

def buttons():
    global w
    global w1
    global w2
    thresholding_button=Button(root,text="Thresholding",command=threshold)
    thresholding_button.place(x=0,y=300)
    w = Scale(root, from_=0, to=255,orient=HORIZONTAL,label="Select threshold")
    w.place(x=120,y=300)
    filtering_button=Button(root,text="Average Filtering",command=averagefilter)
    filtering_button.place(x=0,y=400)
    w1 = Scale(root, from_=1, to=50,orient=HORIZONTAL,label="kernel size")
    w1.place(x=140,y=400)
    w2 = Scale(root, from_=1, to=31,orient=HORIZONTAL,label="kernel size(odd)")
    w2.place(x=100,y=500)
    laplacian_button=Button(root,text="Laplacian",command=laplacian)
    laplacian_button.place(x=0,y=500)
    histogram_button=Button(root,text="Histogram Equalization",command=histequal)
    histogram_button.place(x=0,y=600)

def vidbuttons():
    global prevbutton,nextbutton
    prevbutton=Button(root,text="Previous Frame",command=prevframe)
    prevbutton.place(x=500,y=350)
    nextbutton=Button(root,text="Next Frame",command=nextframe)
    nextbutton.place(x=700,y=350)

def displayimg():
    global img,my_image_label
    my_image_label.destroy()
    height=300
    width=img.width/img.height*height
    img=img.resize((int(width),int(height)))
    tkimg=ImageTk.PhotoImage(img)
    my_image_label=Label(image=tkimg)
    my_image_label.image=tkimg
    my_image_label.pack()

def nextframe():
    global frameno
    global img
    if frameno==len(frames)-1:
        frameno=0
    else:
        frameno+=1
    img=Image.fromarray(frames[frameno][:, :, ::-1])
    displayimg()

def prevframe():
    global frameno
    global img
    if frameno==0:
        frameno=len(frames)-1
    else:
        frameno-=1
    img=Image.fromarray(frames[frameno][:, :, ::-1])
    displayimg()

def histequal():
    global hist_img_label
    global hist_img
    hist_img_label.destroy()
    hist_img=cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    hist_img=cv2.equalizeHist(hist_img)
    hist_img=ImageTk.PhotoImage(Image.fromarray((hist_img).astype(np.uint8)))
    hist_img_label=Label(image=hist_img)
    hist_img_label.image=hist_img
    hist_img_label.place(x=640-(img.width/2),y=400)


def laplacian():
    global laplacian_img_label
    global laplacian_img
    laplacian_img_label.destroy()
    laplacian_img=img.convert('RGB')
    laplacian_img=np.array(laplacian_img)
    ksize=w2.get()
    laplacian_img=cv2.Laplacian( src=laplacian_img,ddepth=cv2.CV_16S,ksize=ksize);

    
    laplacian_img=ImageOps.grayscale(Image.fromarray((laplacian_img).astype(np.uint8)))
    laplacian_img=ImageTk.PhotoImage(laplacian_img)
    laplacian_img_label=Label(image=laplacian_img)
    laplacian_img_label.image=laplacian_img
    laplacian_img_label.place(x=640-(img.width/2),y=400)


def averagefilter():
    global averagefilter_img_label
    global averagefilter_img
    averagefilter_img_label.destroy()
    averagefilter_img=img.convert('RGB')
    averagefilter_img=np.array(averagefilter_img)
    ksize=(w1.get(),w1.get())
    averagefilter_img=cv2.blur(averagefilter_img,ksize)
    averagefilter_img=ImageTk.PhotoImage(Image.fromarray(averagefilter_img))
    averagefilter_img_label=Label(image=averagefilter_img)
    averagefilter_img_label.image=averagefilter_img
    averagefilter_img_label.place(x=640-(img.width/2),y=400)


def threshold():
    global modifiedimage_label
    global threshold_img
    modifiedimage_label.destroy()
    threshold_img=ImageOps.grayscale(img)
    threshold_img=np.array(threshold_img)
    for i in range(threshold_img.shape[0]):
        for j in range(threshold_img.shape[1]):
            if threshold_img[i][j]<w.get():
                threshold_img[i][j]=0
            else:
                threshold_img[i][j]=255
    threshold_img=ImageTk.PhotoImage(Image.fromarray(threshold_img))
    modifiedimage_label=Label(image=threshold_img)
    modifiedimage_label.image=threshold_img
    modifiedimage_label.place(x=640-(img.width/2),y=400)
    

def uploadfile():
    global my_image_label
    global img
    global frames
    global prevbutton,nextbutton
    prevbutton.destroy()
    nextbutton.destroy()
    hist_img_label.destroy()
    laplacian_img_label.destroy()
    averagefilter_img_label.destroy()
    modifiedimage_label.destroy()
    my_image_label.destroy()
    root.filename=filedialog.askopenfilename(initialdir=os.getcwd(),title="Upload video or picture",filetypes=(("png files","*.png"),("jpg files","*.jpg"),("mp4 files","*.mp4"),("mov files","*.mov")))
    if ".png" in root.filename or ".jpg" in root.filename: 
        img=Image.open(root.filename)
    else:
        frames=[]
        video=cv2.VideoCapture(root.filename)
        frame_id=0
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        while(True):
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            ret, frame = video.read()
            frames.append(frame)
            if(ret==False):
                break
            frame_id+=1
        img=Image.fromarray(frames[0][:, :, ::-1])
        vidbuttons()
        
    #resizing
    height=300
    width=img.width/img.height*height
    img=img.resize((int(width),int(height)))

    tkimg=ImageTk.PhotoImage(img)
    my_image_label=Label(image=tkimg)
    my_image_label.image=tkimg
    my_image_label.pack()
    buttons()
    



upload_button=Button(root,text="Select image or video",command=uploadfile)
upload_button.place(x=120,y=150)

root.mainloop()