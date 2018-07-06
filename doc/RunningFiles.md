# Alex N's notes for running through the code

## Pre-Preprocessing
Files will come in raw as .CZI files or Nanozoomer files (.NDPI). NDPI files are from CSHL and can only be converted into JP2000 directly which is why that is how the raw, lossless data is stored. Yuncong converts these into TIFF files so they are useable but it requires conversion of 16bit to 8bit and Hannah said nobody understands how that works nor has Yuncong told anyone.

These files need to be converted to .TIFF files and have all of the surrounding, non-brain, area cut out of the image so that it does not slow down the rest of the code or interfere with anything.

## Preprocessing
### Neurotrace (CSHL)
Requires files from pre-preprocessing step including [name]_anchor.txt, [name]_sorted_filenames.txt, and a collection of other text, json files, and pkl files (< I will elaborate on this soon).

Run **preprocess_cshl_data_v2_neurotrace.ipynb**, it will complete every step of the preprocessing stage for neurotrace brains as outlined below:
1) Prepare data
  - set 'stack' equal to brain name, make sure raw files are on S3:///mousebrainatlas-rawdata/...
2) Download raw scanner files from S3 and Specify raw file locations
  - Specify raw file locations
3) Convert JPEG2000 to TIFF
4) Extract Neurotrace channel
5) Generate thumbnails and linearly contrast stretch
  i) Requires file 'CSHL_data_processed/MD662/MD662_sorted_filenames.txt' in 



### Thionin (UCSD)
Not yet started.
### Detection/Classification
Not yet started.
### Registration/3D Construction
Not yet started.


## Setting up environment
metadata.py
distributed_utilities.py
