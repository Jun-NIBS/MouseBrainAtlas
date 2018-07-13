## The Active Mouse Brain Atlas

This repository contains the code and documentation for the active mouse brain atlas project. 

The core functionality of the code is to register, or align, a stack of brain slices to a standardized brain atlas.

Other functions include tools for annotating brain images, learning the texture corresponding the different structures, and estimating brain-to-brain variability in the location of the structures.

The code is in Python either stand-alone or in Jupyter Notebooks. This code is currently in development.

The code is available free of charge in accordance with the GNU General Public License (GPL)

### System Requirements

This system has been tested on Linux Ubuntu 16.04

**Special Hardware**
Feature extraction (transforming raw image to feature maps) is accelerated using a machine with one or more GPUs  (*Nvidia Titan X*) Computation time per image (section) is 
* About 30 minutes without a GPU
* 80 sec using a single GPU
* 15 sec using 8 GPUs

### Installation Instructions
clone this repository
```
git clone https://github.com/ActiveBrainAtlas/MouseBrainAtlas.git
```
**Typical cloning time:**
This repository is 3.3GB in size. Cloning takes about 3 minutes using an internet connection of 20MB/sec.

After cloning this repository execute the following commands:
```
cd setup
pip install -r requirements.txt
```
**Typical install time** on a typical desktop computer: 5 Minutes.

### Demo

Please consult the README in the Demo Directory


Input and expected output will be downloaded from an open S3 bucket

#### Expected demo run time 

on a typical desktop computer

* Global registration: 1 sec
* Local registration: 1 hour

### Contact Info

If there are any techincal difficulties with the code please contact one of the developers:
* Alex Newberry: adnewber@ucsd.edu
* Yuncong Chen: yuncong@ucsd.edu 
