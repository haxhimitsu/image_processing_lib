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
from utils.utils import my_img_proces

myutil=my_img_proces()
myutil.sayStr("Hello")


parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", required=True, help="path to folder containing images")
parser.add_argument("--output_dir", required=True, help="output path")
parser.add_argument('--resize_pixel',type=int, nargs='+', help='Set resize size height width')
# Use like: python arg.py -resize_pixel 320 640
parser.add_argument("--resize_scale",type=float,help="set resize scale")
parser.add_argument('--split_size',type=int, nargs='+', help='Set split size height width')
parser.add_argument("--trim", action='store_true')
parser.add_argument("--data_reduction",type=float,help="set reduction scale input value must be < 1.0")

parser.add_argument("--eq_hist_rgb", action='store_true')
parser.add_argument("--adjust_contrast",action='store_true')
parser.add_argument("--color_mask",action='store_true')
a = parser.parse_args()

def main():

    output_dir=a.output_dir
    myutil.create_directory(output_dir)

    img_list,ext=myutil.get_img_list(a.input_dir)
    print("sample_read_image_is->\n",img_list[0])
    src_height,src_width=myutil.get_img_specification(img_list[0])
    print("sample_img_height->",src_height)
    print("sample_img_width->",src_width)

    if a.resize_pixel is not None:
        print("process_resize_pixel\n")
        resize_val=a.resize_pixel
        #print("resize_list",resize_val)
        #print("resize_width",resize_val[1])
        #print("resize_height",resize_val[0])
        size=(resize_val[1],resize_val[0])
        #caution!! size=(width,height)
        for src_path in img_list:
            name, _ = os.path.splitext(os.path.basename(src_path))
            #print(name)
            orgimg = cv2.imread(a.input_dir+ '/'+name+ext)
            myutil.image_check(orgimg)
            image2=cv2.resize(orgimg,size)
            save_path=a.output_dir+ '/'+ name +'_'+str(resize_val[0])+"*"+str(resize_val[1])+'.jpg'
            #save_path=a.output_dir+ '/'+ name +'_'+resize_height+"*"+resize_width+'.jpg'
            cv2.imwrite(save_path,image2)

    if a.resize_scale is not None:
        print("process_resize_scale\n")
        scale=a.resize_scale
        width=int(src_width*scale)
        height=int(src_height*scale)
        print("resized_img_height->",height)
        print("resized_img_width->",width)
        for src_path in img_list:
            name, _ = os.path.splitext(os.path.basename(src_path))
            #print(name)
            orgimg = cv2.imread(a.input_dir+ '/'+name+ext)
            myutil.image_check(orgimg)
            image2=cv2.resize(orgimg,(width,height))
            save_path=a.output_dir+ '/'+ name +'_'+str(height)+"*"+str(width)+'.jpg'
            cv2.imwrite(save_path,image2)

    if a.trim is True:
        print("process_trim\n")
        for src_path in img_list:
            name, _ = os.path.splitext(os.path.basename(src_path))
            #print(name)
            orgimg = cv2.imread(a.input_dir+ '/'+name+ext)
            myutil.image_check(orgimg)
            trim = orgimg[(int(src_height*0.4)):(src_height), (0):(src_width)]
            #print("save at",output_dir+ name+'_'+"trimed" +'.jpg')
            cv2.imwrite(output_dir+ name+'_'+"trimed" +'.jpg', trim)

    if a.split_size is not None:
        print("process_split_size\n")
        target_trim=a.split_size
        resize_width, resize_height, rows, cols = myutil.get_split_specification(target_trim[1],target_trim[0])
        for src_path in img_list:
            name, _ = os.path.splitext(os.path.basename(src_path))
            #print(name)
            orgimg = cv2.imread(a.input_dir+ '/'+name+ext)
            orgimg = cv2.resize(orgimg, (resize_width, resize_height))
            chunks = []
            myutil.image_check(orgimg)
            for row_img in np.array_split(orgimg, cols, axis=0):
                for chunk in np.array_split(row_img, rows, axis=1):
                    chunks.append(chunk)
        #print(len(chunks))
        # 保存する。
            for i, chunk in enumerate(chunks):
                save_path=a.output_dir+ '/'+ name +'_'+"split"+f'_{i:02d}.jpg'
                #save_path = output_dir +str(input_image_name_list[k])+f'_{i:02d}.png'
                cv2.imwrite(save_path, chunk)

    if a.data_reduction is not None and a.data_reduction < 1.0:
        print("process_data_reduction\n")
        print("original_datasize->\n",len(img_list))
        exception_range=int(len(img_list)*a.data_reduction)
        print("reduction_datasize->\n",exception_range)
        reduction_img_list=img_list[:exception_range]
        for src_path in img_list:
            name, _ = os.path.splitext(os.path.basename(src_path))
            orgimg = cv2.imread(a.input_dir+ '/'+name+ext)
            myutil.image_check(orgimg)
            save_path=a.output_dir+ '/'+ name +'.jpg'
            cv2.imwrite(save_path,orgimg)




if __name__ == "__main__":
    main()