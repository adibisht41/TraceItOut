# -*- coding: utf-8 -*-
"""
Created on Thu May 17 21:49:50 2018

@author: Dell
"""

import argparse
import datetime
import imutils
import time
import cv2
import os

import tkinter
import tkinter.messagebox as tkMessageBox

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()  
      #  self.helloCallBack()
        

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Start Recording"
        self.hi_there["command"] = self.helloCallBack
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
    
    
    def helloCallBack(self):
        start_time = time.time()
        start_time 
        elapsed_time = time.time() - start_time
        elapsed_time
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
        args = vars(ap.parse_args())
    
        print(args["video"])
        # if the video argument is None, then we are reading from webcam
        if args.get("video",None) is None:
            camera = cv2.VideoCapture(0)
            print('hello')
            time.sleep(0.25)
    
        # otherwise, we are reading from a video file
        else:
            camera = cv2.VideoCapture(args["video"])
                 
        # initialize the first frame in the video stream
        firstFrame = None
    
        # get the loaction and create video folder if not created.
        location = os.getcwd()
        directory = 'video'
        if not os.path.exists(directory):
        	os.makedirs(directory)
        location = location + '/video\output.avi'
        print(location)
    
        # for setting of every video.
        width = camera.get(3)  # float
        height = camera.get(4)
        width = round(width)
        height = round(height)
        print("wirth of frame : "+str(width))
        print("height of frame : "+str(height))
    
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        out = cv2.VideoWriter(location,fourcc, 100.0, (width,height))
    
    
        # loop over the frames of the video
        while True:
            # grab the current frame and initialize the occupied/unoccupied
            # text
            (grabbed, frame) = camera.read()
            thisFrame = frame
            #out.write(thisFrame)
            text = "Unoccupied"
            
            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if not grabbed:
                break
            
            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21,21), 0)
            
            
            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                #out.write(thisFrame)
                continue
            
            elapsed_time = time.time() - start_time
            print(elapsed_time)
            if elapsed_time > 2:
                start_time = time.time()
                firstFrame = gray
            
            
            # compute the absolute difference between the current frame and
        	# first frame
            frameDelta = cv2.absdiff(firstFrame,gray)
            thresh = cv2.threshold(frameDelta, 25, 255,cv2.THRESH_BINARY)[1]
            
            # dilate the thresholded image to fill in holes, then find contours
        	# on thresholded image
            thresh = cv2.dilate(thresh,None,iterations = 2)
            _ , cnts, _ = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
            # loop over the contours
            for c in cnts:
                #  if the contour is too small, ignore it
                if cv2.contourArea(c) < args["min_area"]:
                    continue
                
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x + w,y + h), (0, 255, 0),2)
                text = "Occupied"
                print("hello")
                out.write(thisFrame)
            
            # writing on frame
            
            # draw the text and timestamp on the frame
            cv2.putText(frame, "Room Statis: {}".format(text), (10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10,frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0, 255),1)
            
            # show the frame and record if the user presses a key
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frameDelta)
            cv2.imshow("Security Feed",frame)
            key = cv2.waitKey(1) & 0xFF
            
            # if the `q` key is pressed, break from the lop
            if key== ord("q"):
                break
            
    
        # cleanup the camera and close any open windows
        camera.release()
        out.release()
        cv2.destroyAllWindows()

root = tk.Tk()
app = Application(master=root)
app.mainloop()