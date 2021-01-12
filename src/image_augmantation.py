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

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", required=True, help="path to folder containing images")
parser.add_argument("--output_dir", required=True, help="output path")
parser.add_argument("--rot_img_deg", choices=["90", "180", "270"])
parser.add_argument("--resize_width",type=int )
parser.add_argument("--resize_height",type=int )
parser.add_argument("--eq_hist_rgb", action='store_true')
parser.add_argument("--adjust_contrast",action='store_true')
parser.add_argument("--color_mask",action='store_true')
a = parser.parse_args()


def find(d):
    result = []
    for filename in os.listdir(d):
        _, ext = os.path.splitext(filename.lower())
        if ext == ".jpg" or ext == ".png" or ext == ".bmp" or ext=='.tif':
            result.append(os.path.join(d, filename))
    result.sort()
    return result


def equalizeHistRGB(src):

    RGB = cv2.split(src)
    Blue   = RGB[0]
    Green = RGB[1]
    Red    = RGB[2]
    for i in range(3):
        cv2.equalizeHist(RGB[i])

    img_hist = cv2.merge([RGB[0],RGB[1], RGB[2]])
    return img_hist


def img_rot(orgimg,angle_deg,scale):

    ###画像の回転中心を指定#########
    #高さを定義
    height = orgimg.shape[0]
    #幅を定義
    width = orgimg.shape[1]
    #回転の中心を指定
    center = (int(width/2), int(height/2))

    #回転角を指定 angle_deg
    #スケールを指定 scale = 1.0
    #getRotationMatrix2D関数を使用
    trans = cv2.getRotationMatrix2D(center, float(angle_deg) , scale)
    #アフィン変換
    dst = cv2.warpAffine(orgimg, trans, (width,height))

    return dst

def color_mask(orgimg):

    #HSV化
    hsvval=cv2.cvtColor(orgimg, cv2.COLOR_BGR2HSV_FULL)

    #HSV値の取得
    h = hsvval[:, :, 0]
    s = hsvval[:, :, 1]
    v = hsvval[:, :, 2]

    #マスク画像の生成(赤色)
    maskimg = np.zeros(h.shape, dtype=np.uint8)
    # maskimg[((h < 20) | (h > 200)) & (s > 170)] = 255  #RED
    # maskimg[((h > 40) & (h < 120)) & (s > 128)] = 255  #GREEN
    # maskimg[((h > 38-35) & (h < 38+35)) & (s > 249-35) & (s < 249+35) & (v > 226-35) & (v < 226+35)] = 255  #GREEN
    #maskimg[(v < 50)] = 255  #Black
    maskimg[((h > 90-35) & (h < 90+35)) & (v < 40)] = 255  #Black

    #マスク画像の表示
    #cv2.imshow('maskImage',maskimg)

    # #Closing Dilation -> erosion
    # kernel = np.ones((3,3),np.uint8)
    # closing = cv2.morphologyEx(maskimg, cv2.MORPH_OPEN, kernel)
    # #plot opening image
    # cv2.imshow('Opening',closing)


    #反転処理
    binimg=cv2.bitwise_not(maskimg)
    #二値化した画像の表示
    cv2.imshow('Binary',binimg)

    #Opening erosion -> Dilation
    # kernel = np.ones((2,2),np.uint8)
    # opening = cv2.morphologyEx(binimg, cv2.MORPH_OPEN, kernel)
    # #plot opening image
    # cv2.imshow('Opening',opening)


    #読み込んだ画像にマスク処理
    colorimg=cv2.bitwise_and(orgimg, orgimg, mask=binimg)

    #マスク画像の表示
    #cv2.imshow('ColorImage',colorimg)

    return colorimg

def main():
    src_paths = []
    dst_paths = []
    skipped = 0

    ##########################
    # ルックアップテーブルの生成
    min_table = 50
    max_table = 205
    diff_table = max_table - min_table
    gamma1 = 0.75
    gamma2 = 1.5

    LUT_HC = np.arange(256, dtype = 'uint8' )
    LUT_LC = np.arange(256, dtype = 'uint8' )
    LUT_G1 = np.arange(256, dtype = 'uint8' )
    LUT_G2 = np.arange(256, dtype = 'uint8' )

    LUTs = []

    # ハイコントラストLUT作成
    for i in range(0, min_table):
        LUT_HC[i] = 0

    for i in range(min_table, max_table):
        LUT_HC[i] = 255 * (i - min_table) / diff_table

    for i in range(max_table, 255):
        LUT_HC[i] = 255

    # その他LUT作成
    for i in range(256):
        LUT_LC[i] = min_table + i * (diff_table) / 255
        LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)
        LUT_G2[i] = 255 * pow(float(i) / 255, 1.0 / gamma2)

    #LUTs.append(LUT_HC)
    #LUTs.append(LUT_LC)
    #LUTs.append(LUT_G1)
    LUTs.append(LUT_G2)
    ###################################################

    #create save folder
    if not os.path.exists(a.output_dir):
        os.makedirs(a.output_dir)

    ##get image folder
    for src_path in find(a.input_dir):
        name, _ = os.path.splitext(os.path.basename(src_path))
        dst_path = os.path.join(a.output_dir, name + ".tif")
        if os.path.exists(dst_path):
            skipped += 1
        else:
            src_paths.append(src_path)
            dst_paths.append(dst_path)
    print("skipping %d files that already exist" % skipped)
    print("processing %d files" % len(src_paths))


    for src_path in find(a.input_dir):
        name, _ = os.path.splitext(os.path.basename(src_path))
        print(name)
        #dst_path = os.path.join(a.output_dir, name + ".png")
        orgimg = cv2.imread(a.input_dir+ '/'+name+'.tif')

        if orgimg is None:
            print("Can't_read_image")
            sys.exit()
        if a.resize_height is not None:
            size=(a.resize_height,a.resize_width)
            image2=cv2.resize(orgimg,size)
            save_path=a.output_dir+ '/'+ name +'_'+str(a.resize_height)+str(a.resize_width)+'.png'
            cv2.imwrite(save_path,image2)

        if a.rot_img_deg is not None:
            image2=img_rot(orgimg,angle_deg=a.rot_img_deg,scale=1.0)
            save_path=a.output_dir+ '/'+ name +'_'+str(a.rot_img_deg)+'deg'+'.png'
            cv2.imwrite(save_path,image2)
            #print(save_path)

        if a.eq_hist_rgb is True:
            image2=equalizeHistRGB(orgimg)
            save_path=a.output_dir+ name +'_'+'eqhistrgb'+'.png'
            cv2.imwrite(save_path,image2)

        if a.adjust_contrast is True:
            for i, LUT in enumerate(LUTs):
                image2=cv2.LUT(orgimg, LUT)
                save_path=a.output_dir+ name +'.png'
            cv2.imwrite(save_path,image2)

        if a.color_mask is True:
            image2=color_mask(orgimg)
            save_path=a.output_dir+ name +'.png'
            cv2.imwrite(save_path,image2)


    print("Done")


if __name__ == "__main__":
    main()