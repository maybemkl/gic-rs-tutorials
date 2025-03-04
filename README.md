# gic-rs-tutorials

Remote sensing tutorials taught at the McGill GIC.

## 1. PySTAC tutorial

You can access this tutorial in two ways.

### 1A. Google Colab

Open a notebook in [Google Colab](https://colab.research.google.com/drive/17fXgT5mXfFI_7CKvEujDwYgx3w6gyC3U?usp=sharing). Next, make sure you have the relevant files on your instance. These should include:

- A folder called "data"
- A folder called "img"
- A .py file called "utiles.py"
- A .py file called spectral_indexes.py

If you do *not* have them:

1. Download them from [Mediafire](https://www.mediafire.com/file/656ulooyxizybxc/pystac_files.zip/file)
2. Upload them to the Google Colab

### 1B. Git Clone

You can also clone this repo directly. In that case:

```bash

git clone https://github.com/maybemkl/gic-rs-tutorials.git

```

You need Jupyter lab or Jupyter notebook to actually run the code. Once you have those installed and a virtuan environment setup, install all the prerequisite packages:

```bash

pip install -r requirements.txt

```

Now you can run the notebook:

```bash

jupyter lab 01_pystac.ipynb

```

## 2. YOLOv5 for RS tutorial

The Google Colab can be accessed [here](https://colab.research.google.com/drive/1g8VJ--8UkWCoVS78FkHdJDJCo-Aw79I-?usp=sharing). This time you only need the image files [here](https://www.mediafire.com/file/pst5sfdw0vj005q/img.zip/file). Otherwise you can follow the steps above, except to  do:


```bash

pip install -r 02_requirements.txt

```

```bash

jupyter lab 02_object_detection_yolov5.ipynb

```