The Active Mouse Brain Atlas project provides a toolkit for automatic registration of histological series to a standardized brain atlas, based on detecting structures by high-resolution textures.

- [Installation](#installation)
- [Demo](#demo)
- [Reference](#reference)

----

# Installation

This system has been tested on Ubuntu 16.04. The feature extraction step can be significantly accelerated using GPU (80 seconds per image using a single Nvidia Titan X, 15 seconds using 8 GPUs, compared to 30 minutes using CPU).

```
git clone https://github.com/ActiveBrainAtlas/MouseBrainAtlas.git
cd setup
pip install -r requirements.txt
```

Cloning the repository takes about 3 minutes using a 20MB/s connection. Installing requirements takes around 5 minutes.

# Demo

We provide demo scripts that demonstrate the process of registering an example brain with the atlas, and visualizing the result. See the [demo] directory for details. The demo takes roughly half an hour from start to finish.

# Reference

The Active Atlas: Combining 3D Anatomical Models with Texture Detectors, Yuncong Chen et al., MICCAI 2017 [[pdf]](https://arxiv.org/pdf/1702.08606.pdf)

