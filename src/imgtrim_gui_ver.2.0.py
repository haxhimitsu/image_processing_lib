#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# author:"Haxhimitsu"
# date  :"2021/01/06"
# cite  :
# sample:python3 imgtrim_gui_ver.2.0.py  --input_dir ../assets/original_img/cbn_test_01/ --output_dir ../assets/sample_output/  --trim_width 32 --trim_height 64
#python3 imgtrim_gui_ver.2.0.py  --input_dir ~/Desktop/cbn_3dref_dataset/test/ --output_dir ~/Desktop/temppp/
#---------------------------------------------------------------------

import os
import numpy as np
import tkinter as tk #GUI関連の機能を使うために必要
import tkinter.filedialog as tkfd #ファイルダイアログボックスを使うために必要
import tkinter.messagebox as tkmb #メッセージボックスを使うために必要
import cv2 #OpenCVを使うために必要
#import cv2
import sys
import argparse#引数拡張mジュール
import time
import copy

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir",  required=True, help="path to folder containing images")
parser.add_argument("--img_scale", type=float,default=1.0, help="set image size e.g.'0.5,0.8...'")
parser.add_argument("--trim_width", type =int ,default=32,help="set trim width")
parser.add_argument("--trim_height", type =int ,default=32,help="set trim height")
parser.add_argument("--output_dir",  help="output path",required=True)
a = parser.parse_args()

class mouseParam:
    def __init__(self, input_img_name):
        #マウス入力用のパラメータ
        self.mouseEvent = {"x":None, "y":None, "event":None, "flags":None}
        #マウス入力の設定
        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)
    
    #コールバック関数
    def __CallBackFunc(self, eventType, x, y, flags, userdata):
        
        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = eventType    
        self.mouseEvent["flags"] = flags    

    #マウス入力用のパラメータを返すための関数
    def getData(self):
        return self.mouseEvent
    
    #マウスイベントを返す関数
    def getEvent(self):
        return self.mouseEvent["event"]                

    #マウスフラグを返す関数
    def getFlags(self):
        return self.mouseEvent["flags"]                

    #xの座標を返す関数
    def getX(self):
        return self.mouseEvent["x"]  

    #yの座標を返す関数
    def getY(self):
        return self.mouseEvent["y"]  

    #xとyの座標を返す関数
    def getPos(self):
        return (self.mouseEvent["x"], self.mouseEvent["y"])
    

"""
# function      :   make  item list sort by name 
# input arg     :   directy path
# output        :   list of each contents path (list)
# func detail   :   make list of path several contents in directry sorted by namae.
                    if None contents input directry path EOF error and 
"""
def find(d):
    result = []
    for filename in os.listdir(d):
        _, ext = os.path.splitext(filename.lower())
        if ext == ".jpg" or ext == ".png" or ext == ".tif":
            result.append(os.path.join(d, filename))
        else:
            print("can't find  such file or directry")
            break
    result.sort()
    return result

"""
# function      : careate  directry
# input arg     : directry path
# output        : none
# func detail   : if not already exsits arg directry path,this function create directry.
"""
def create_directry(directry_path):
    if not os.path.exists(directry_path):
        os.makedirs(directry_path)
    else:
        print("already exsists"+directry_path)

def main():

    count = 0
    flag = 0
    mouse_flag = 0

    input_dir=a.input_dir
    output_dir=a.output_dir
    trim_width=int(a.trim_width/2)
    trim_height=int(a.trim_height/2)
    print(trim_height)
    print(trim_width)
    
    input_img_list=find(input_dir)
    print(input_img_list)
    create_directry(output_dir)

    for i in range(len(input_img_list)):
        color = cv2.imread(input_img_list[i])
        tmp = color

        #リサイズ
        tmp1=color.copy()
        height = tmp1.shape[0]*a.img_scale
        width = tmp1.shape[1]*a.img_scale
        half_size = cv2.resize(tmp1,(round(width),round(height)))

        window_name = "input window"
        cv2.imshow(window_name, half_size)
        mouseData = mouseParam(window_name)
        
        while flag == 0:
            #cv2.imshow(window_name, tmp)
            cv2.waitKey(20)
            #mouse_flag=0
            
            if mouseData.getEvent() == cv2.EVENT_MOUSEMOVE:
                
                x = mouseData.getX()
                y = mouseData.getY()
                mouse_flag = 0
                
                if  (y-trim_height >= 0) and (x-trim_width >= 0) and (y+trim_height >= 0) and (x+trim_width >= 0):
                    trimshow = tmp[(y-trim_height):(y+trim_height), (x-trim_width):(x+trim_width)]
                    cv2.imshow("trim", trimshow)
            
            if (mouseData.getEvent() == cv2.EVENT_MBUTTONDOWN) and (mouse_flag == 0):
                #flag = 1
                mouse_flag = 1
                
                if  (y-trim_height >= 0) and (x-trim_width >= 0) and (y+trim_height >= 0) and (x+trim_width >= 0):
                    count = count + 1;
                    trim = tmp[(y-trim_height):(y+trim_height), (x-trim_width):(x+trim_width)]
                    print("save at",output_dir+ '%d'%count +'.jpg')
                    cv2.imwrite(output_dir+ '%d'%count +'.jpg', trim)
            
            if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                flag = 1
                
            if mouseData.getEvent() == cv2.EVENT_RBUTTONDOWN:
                cv2.destroyAllWindows()
                sys.exit()
        flag = 0
        #count = count + 1;
        

    
    print("Done")



if __name__ == '__main__':
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
