#!/usr/bin/env python3
#----------------------------------------------------------------------
# author:"Haxhimitsu"
# date  :"2020/07/01"
#----------------------------------------------------------------------

import os #OS関連機能を使うために必要
import tkinter as tk #GUI関連の機能を使うために必要
import tkinter.filedialog as tkfd #ファイルダイアログボックスを使うために必要
import tkinter.messagebox as tkmb #メッセージボックスを使うために必要
import cv2 #OpenCVを使うために必要
import numpy as np #行列演算用ライブラリ
import matplotlib.pyplot as plt#描画ライブラリ
from mpl_toolkits.mplot3d import Axes3D#ライブラリ（3次元用）
import sys##システムエラー処理用
from scipy import stats
import argparse##引数拡張mジュール
#import tfimage as im
import time
import multiprocessing

#my module
import sys
from utils.utils import my_img_proces

myutil=my_img_proces()
myutil.sayStr("Hello")


parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", required=True, help="path to folder containing images")
parser.add_argument("--output_dir", required=True, help="output path")
parser.add_argument("--rot_img_deg", choices=["90", "180", "270"])
parser.add_argument("--resize_width",type=int )
parser.add_argument("--resize_height",type=int )
parser.add_argument("--trim")
parser.add_argument("--eq_hist_rgb", action='store_true')
parser.add_argument("--adjust_contrast",action='store_true')
parser.add_argument("--color_mask",action='store_true')
a = parser.parse_args()

def main():

    output_dir=a.output_dir
    myutil.create_directory(output_dir)
    
    img_list=myutil.get_img_list(a.input_dir)
    print(img_list[0])

    for src_path in img_list:
        name, _ = os.path.splitext(os.path.basename(src_path))
        #print(name)
        #dst_path = os.path.join(a.output_dir, name + ".png")
        orgimg = cv2.imread(a.input_dir+ '/'+name+'.jpg')

        if orgimg is None:
            print("Can't_read_image")
            sys.exit()

        if a.resize_height is not None:
            size=(a.resize_height,a.resize_width)
            image2=cv2.resize(orgimg,size)
            save_path=a.output_dir+ '/'+ name +'_'+str(a.resize_height)+"*"+str(a.resize_width)+'.png'
            cv2.imwrite(save_path,image2)

        if a.trim is not None:
            height,width,c=orgimg.shape
            trim = orgimg[(int(height*0.4)):(height), (0):(width)]
            print("save at",output_dir+ name+'_'+"trimed" +'.jpg')
            cv2.imwrite(output_dir+ name+'_'+"trimed" +'.jpg', trim)






if __name__ == "__main__":
    main()