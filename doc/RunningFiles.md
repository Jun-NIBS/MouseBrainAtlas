# Alex N's notes for running through the code




## Preprocessing
### Neurotrace (CSHL)
Requires files from pre-preprocessing step including [name]_anchor.txt, [name]_sorted_filenames.txt, and a collection of other text, json files, and pkl files.

Run **preprocess_cshl_data_v2_neurotrace.ipynb**, it will complete every step of the preprocessing stage as outlined below:
1) Download raw scanner files from S3
2) Specify raw file locations
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
