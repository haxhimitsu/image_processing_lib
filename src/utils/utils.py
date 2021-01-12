#!/usr/bin/env python3
# coding: UTF-8

#---------------------------------------------------------------
# author:"Haxhimitsu"
# date  :"2021/01/06"
# cite  :
# sample:python3 imgtrim_gui_ver.2.0.py  --input_dir ../assets/original_img/cbn_test_01/ --output_dir ../assets/sample_output/  --trim_width 32 --trim_height 64
#---------------------------------------------------------------
import numpy as np
#import pandas as pd
#from sklearn.model_selection import train_test_split
#import matplotlib.pyplot as plt
import os

class my_img_proces:

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

        return result



    def sayStr(self, str):
        print (str)
 
if __name__ == '__main__':
    test = my_img_proces()
    test.sayStr("Hello")   # Hello