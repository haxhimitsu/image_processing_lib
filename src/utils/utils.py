#!/usr/bin/env python3
# coding: UTF-8

#---------------------------------------------------------------
# author:"Haxhimitsu"
# date  :"2021/01/06"
# cite  :
# sample:python3 imgtrim_gui_ver.2.0.py  --input_dir ../assets/original_img/cbn_test_01/ --output_dir ../assets/sample_output/  --trim_width 32 --trim_height 64
#---------------------------------------------------------------
import numpy as np

import os
import cv2 #OpenCVを使うために必要
class my_img_proces:

    def image_check(self,image):
        if image is None:
            print("Can't_read_image")
            sys.exit()

    def get_img_specification(self,image_path):
        image=cv2.imread(image_path)
        self.image_check(image)
        self.img_width=image.shape[1]
        self.img_height=image.shape[0]

        return self.img_height, self.img_width

    """
    # function      : careate  directry
    # input arg     : directry path
    # output        : none
    # func detail   : if not already exsits arg directry path,this function create directry.
    """
    def create_directory(self,directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        else:
            print("already exsists"+directory_path)

    def get_img_list(self,img_directory):
        result = []

        for filename in os.listdir(img_directory):
            _, ext = os.path.splitext(filename.lower())
            if ext == ".jpg" or ext == ".png" or ext == ".bmp" or ext=='.tif':
                result.append(os.path.join(img_directory, filename))
        result.sort()

        return result,ext
    
    def get_split_specification(self,target_width,target_height):
        rows=int(self.img_width/target_width)
        cols=int(self.img_height/target_height)
        resize_width=target_width*rows
        resize_height=target_height*cols
        print("split_resize_width->",resize_width,"split_resize_height->",resize_height)
        print("rows->",rows,"cols->",cols)
        return resize_width,resize_height,rows,cols



    def sayStr(self, str):
        print (str)

if __name__ == '__main__':
    test = my_img_proces()
    test.sayStr("Hello")   # Hello