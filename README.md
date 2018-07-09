## The Active Mouse Brain Atlas

This repository hold the code and documentation for the active mouse brain atlas project. 

The core function of the code is to register a stack of brain slices to a standarized brain atlas.

Other functions include tools for annotating brain images, learning the texture corresponding the different structures, and estimating brain-to-brain variability in the location of the structures.

The code is in Python either stand-alone or in Jupyter Notebooks. This code is currenly in development.

The code is available free of charge in accordance with the GNU General Public License (GPL)

### Directories:

* **old**: Orphaned code
* **doc**: Documentation
* **src**: Code  
  src is further divided into
  * **PreProcessing**: Tools for preparing raw images for analysis.
  * **Registration**: Tools for registrating an existing stack.
  * **Learning**: Tools for learning textures and organzation of structures and creating or refining an atlas.

