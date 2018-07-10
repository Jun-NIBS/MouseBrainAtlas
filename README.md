## The Active Mouse Brain Atlas

This repository hold the code and documentation for the active mouse brain atlas project. 

The core function of the code is to register a stack of brain slices to a standarized brain atlas.

Other functions include tools for annotating brain images, learning the texture corresponding the different structures, and estimating brain-to-brain variability in the location of the structures.

The code is in Python either stand-alone or in Jupyter Notebooks. This code is currenly in development.

The code is available free of charge in accordance with the GNU General Public License (GPL)

### Directories:

* **old**: Orphaned code
* **doc**: Documentation
  * **User Guide**: [Reference manual for running the code](https://github.com/ActiveBrainAtlas/MouseBrainAtlas/blob/master/doc/User%20Manuals/UserGuide.md)
* **src**: Code  
  src is further divided into
  * **PreProcessing**: Tools for preparing raw images for analysis.
  * **Registration**: Tools for registrating an existing stack.
  * **Learning**: Tools for learning textures and organzation of structures and creating or refining an atlas.

#### PreProcessing
Takes in raw image stacks of sagittal brain sections. Images are first converted to Tiff files for easier manipulations. Each flourescant image is run through intensity normalization and are rigidly aligned to each other to allow for direct comparisson. Alginment can then be reviewed by a user to confirm accuracy. Each file is cropped down to the start of the brain to only display the regions of interest, this reduces future computation time. This cropping also has user-assisted features. Finally masks and 3D intensity volumes are generated.

#### Registration

#### Learning
