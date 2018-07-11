## Directories:

* **doc**: Documentation
  * **User Guide**: [Reference manual for running the code](https://github.com/ActiveBrainAtlas/MouseBrainAtlas/blob/master/doc/User%20Manuals/UserGuide.md)
* **src**: Code  
  src is further divided into
  * **PreProcessing**: Tools for preparing raw images for analysis.
  * **Registration**: Tools for registering an existing stack.
  * **Learning**: Tools for learning textures and organization of structures and creating or refining an atlas.
* **old**: Orphaned code


## Processing stages
#### PreProcessing
Takes in raw image stacks of sagittal brain sections. Images are first converted to Tiff files for easier manipulations. Each fluorescent image is run through intensity normalization and are rigidly aligned to each other to allow for direct comparison. Alignment can then be reviewed by a user to confirm accuracy. Each file is cropped down to the start of the brain to only display the regions of interest, this reduces future computation time. This cropping also has user-assisted features. Finally masks and 3D intensity volumes are generated.

#### Registration

#### Learning

#### 3D

#### Annotation and GUI


