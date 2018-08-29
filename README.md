The Active Mouse Brain Atlas project provides a toolkit for automatic registration of histological series to a standardized brain atlas, based on detecting structures by high-resolution textures.

- [System requirements](#system-requirements)
- [Installation Instructions](#installation-instructions)
- [Demo](#demo)

----

# System Requirements

This system has been tested on Linux Ubuntu 16.04

**Special Hardware**
Feature extraction (transforming raw image to feature maps) is accelerated using a machine with one or more GPUs  (*Nvidia Titan X*) Computation time per image (section) is 
* About 30 minutes without a GPU
* 80 sec using a single GPU
* 15 sec using 8 GPUs

# Installation Instructions
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

# Demo

Please consult the README in the Demo Directory


Input and expected output will be downloaded from an open S3 bucket

#### Expected demo run time 

on a typical desktop computer

* Roughly half an hour start to finish
