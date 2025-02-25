# gic-rs-tutorials

Remote sensing tutorials taught at the McGill GIC.

## 1. PySTAC tutorial

You can access this tutorial in two ways.

### 1A. Google Colab

Open a notebook in [Google Colab](https://colab.research.google.com/drive/15q2DjvF1WfUnJc6-iT78pC0nhlIgQjvk?usp=sharing). Next, make sure you have the relevant files on your instance. These should include:

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