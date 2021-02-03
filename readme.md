# image processing libraly

いろいろな画像処理を行うディレクトリ

# Usage

* 画像の高さと幅のピクセル値を指定したリサイズ↓
```python:src/img_aug_ver2.0.py
python3 src/img_aug_ver2.0.py --inpt_dir "{your input directory}" --output_dir "{your output directry}" --resize_pixel  128 256
```
input_dir で指定したディレクトリ内の画像を読み込み，
height 128 ，width 256にリサイズ．
output_dir で指定したディレクトリ画像を保存する．


* 画像同士の差分を計算するプログラム
IPS(image pixel simiraly)↓
```bash
python3 prog/src/img_diff_02.py  --input_dir cbn_test_04/images/  --target_fname  outputs --comp_fname targets
```
argments

target_fname,comp_fname  は比較したい画像名の文字列をしていする．


* 各光源の回転角度に対する割合を計算し，棒グラフや円形ヒストグラムを作成する↓
```bash
python3 rot_hist03.py --input_dir sample/ --source_fname Bloc --caloc_type pixel_size_to_ratio
```
--caloc_typeは以下の２つの指定方法がある．

--pixel_size_to_ratio ->元画像サイズに対する各光源色の割合．
![Test Image 1](graph/pixel_size_to_ratio.png)

color_size_to_ratio ->４色の光源の合計サイズに対する各光源色の割合．
を計算する．

円形ヒストグラム↓
![Test Image 1](graph/rot_hist_original.png)


その他のプログラムは，古いばーじょん．
# Requirement
 
 
* python 3.6.9
* matplotlib 3.2.2
* opencv 4.4.0


# Author
* haxhimitu
* National institute of sasebo calleage
* it1915[@]st.sasebo.ac.jp
* haxhimitsu.lab[@]gmail.com
 
