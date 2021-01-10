#!/usr/bin/env python3
#----------------------------------------------------------------------
# author:"Haxhimitsu"
# date  :"2021/01/06"
# cite  :
# 
#---------------------------------------------------------------------

import os
import numpy as np
import tkinter as tk #GUI関連の機能を使うために必要
import tkinter.filedialog as tkfd #ファイルダイアログボックスを使うために必要
import tkinter.messagebox as tkmb #メッセージボックスを使うために必要
import cv2 #OpenCVを使うために必要
#import cv2
import sys
import argparse##引数拡張mジュール
import time
import copy

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir",  required=True, help="path to folder containing images")
#parser.add_argument("--source_fname", required=True ,help="set source img name")
#parser.add_argument("--caloc_type",type =str,choices=["pixel_size_to_ratio","color_size_to_ratio" ],required=True,help="caloc_type")
parser.add_argument("--output_dir",  help="output path")
#parser.add_argument("--comp_fname", required=True ,help="set compare img name")
#parser.add_argument("--rot_img_deg",choices=["90", "180", "270"])
#parser.add_argument("--b_dir", type=str, help="path to folder containing B images for combine operation")
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
    

def main():
    train_img_dirs = ['original_img/cbn_test_01']######################このプログラム使う時はここを書き換えよう############################

    count = 43
    
    flag = 0
    mouse_flag = 0
    input_dir=a.input_dir
    
    for i, d in enumerate(train_img_dirs):
        files = os.listdir(input_dir+"/"+ d)
        print(files)
        for f in files:
            # 画像読み込み
            print(input_dir +"/"+ d + '/' + f)
            color = cv2.imread(input_dir +"/"+ d + '/' + f,1)
            tmp = color

            #リサイズ
            tmp1=color.copy()
            height = tmp1.shape[0]
            width = tmp1.shape[1]
            half_size = cv2.resize(tmp1,(round(width/2),round(height/2)))

            window_name = "input window"
            cv2.imshow(window_name, half_size)
            mouseData = mouseParam(window_name)
            
            while flag == 0:
                #cv2.imshow(window_name, tmp)
                cv2.waitKey(20)
                #mouse_flag=0
                
                if mouseData.getEvent() == cv2.EVENT_MOUSEMOVE:
                    
                    x = mouseData.getX()*2
                    y = mouseData.getY()*2
                    mouse_flag = 0
                    
                    if (y-20 >= 0) and (x-20 >= 0) and (y+20 >= 0) and (x+30 >= 0):
                        trimshow = tmp[y-200:y+200, x-320:x+320]
                        cv2.imshow("trim", trimshow)
                
                if (mouseData.getEvent() == cv2.EVENT_RBUTTONDOWN) and (mouse_flag == 0):
                    #flag = 1
                    print("Rhoge")
                    mouse_flag = 1
                    
                    if (y-20 >= 0) and (x-20 >= 0) and (y+20 >= 0) and (x+20 >= 0):
                        count = count + 1;
                        trim = tmp[y-20:y+20, x-32:x+32]#トリミング
                        print(a.output_dir+ '%d'%count +'.jpg')
                        cv2.imwrite(a.output_dir+ '%d'%count +'.jpg', trim)
                
                if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                    flag = 1
                    
                if mouseData.getEvent() == cv2.EVENT_MBUTTONDOWN:
                    cv2.destroyAllWindows()
                    sys.exit()
            
            flag = 0
            #count = count + 1;
            
            if count % 100 == 0:
                print("test"+ '%d'%count +'.jpg')
            
    print('finish')
    
    #cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")