# image processing libraly

いろいろな画像処理を行うディレクトリ


# Gneral specification
* 読み込み可能な画像の拡張子はopencvに準拠．
* 保存時の拡張子は，`.jpg`
* 保存先のディレクトリが存在しない場合，自動的にディレクトリが作成される．
* すでに存在するディレクトリを指定した場合は，上書きされる．
* argments のhelpを見れば機能と指定を見れる↓
```
python3 src/img_aug_ver2.0.py --h
```

# Usage
* 画像の高さと幅のピクセル値を指定したリサイズ↓
```python:src
python3 src/img_aug_ver2.0.py --inpt_dir "{your input directory}" --output_dir "{your output directry}" --resize_pixel  128 256
```
input_dir で指定したディレクトリ内の画像を読み込み，
height 128 ，width 256にリサイズ．
output_dir で指定したディレクトリ画像を保存する．


* 元画像に対する比率を用いたリサイズ↓
```bash
python3 src/img_aug_ver2.0.py --inpt_dir "{your input directory}" --output_dir "{your output directry}" --resize_scale  0.5
```
`--resize_scale`は，1.0以下のfloatで指定すること．
リサイズ後の値が浮動小数点の場合，intでcastしているため，切り上げ．



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
 
