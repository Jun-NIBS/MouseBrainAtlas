# Alex N's notes for running through the code

## File Formats
* The files from CSHL are sent to us as jp2000. 
* Files from UCSD **unknown for now**
* Files are stored on S3 and birdstore as uncompressed jp2000. 

## Preprocessing
### Neurotrace (CSHL)
Requires files from pre-preprocessing step including [name]_anchor.txt, [name]_sorted_filenames.txt, and a collection of other text, json files, and pkl files (< I will elaborate on this soon).

Neutrace data typically is stained with another indicator, data has multiple channels that are a part of the preprocessing stage.

Run **preprocess_cshl_data_v2_neurotrace.ipynb**, it will complete every step of the preprocessing stage for neurotrace brains as outlined below:
* Prepare data
  - set 'stack' equal to brain name, make sure raw files are on S3:///mousebrainatlas-rawdata/...
* Download raw scanner files from S3 and Specify raw file locations
  - Specify where to download all raw files, for me was `~/MD###/`
* Convert raw JPEG2000 to TIFF format **[JP2 -> TIF]**
  - CSHL uses NanoZoomer, gives CSHL format which apparently can onlly be converted to jp2
  - input:  `~/MD###/*.jp2`  (Location of ALL raw files, defined earlier)
  - output: `~/CSHL_data_processed/MD###/MD###_raw/*_raw.tif`
  - NOTE: may have discrepency with defined input/output directories
* Extract Neurotrace channel **[raw -> raw_Ntb]**
  - input:  `~/CSHL_data_processed/MD###/MD###_raw/*_raw.tif`
  - output: `~/CSHL_data_processed/MD###/MD###_raw_Ntb/*_raw_Ntb.tif`
* Generate thumbnails and linearly contrast stretch **[raw_Ntb -> thumbnail_Ntb -> thumbnail_NtbNormalized]**
  - Requires file `MD###_sorted_filenames.txt` in `~/CSHL_data_processed/MD###/` among others
    - List of necessary pre-preprocess files here [NEED TO ADD]
  - input:   ----`~/CSHL_data_processed/MD###/MD###_raw_Ntb/*_raw_Ntb.tif`
  - output1: `~/CSHL_data_processed/MD###/MD###_thumbnail_Ntb/*_thumbnail_Ntb.tif`
  - output2: `~/CSHL_data_processed/MD###/MD###_thumbnail_NtbNormalized/*_thumbnail_NtbNormalized.tif`
* Compute Transforms using thumbnail_NtbNormalized
  - Use Elastix to align, computing transforms between adjacent sections
    - Gives *pairwise* transforms
  - Next step is to Compose the pairwise transformations, requires anchor slide
    - Then for each section (=slide), multiply all the pairwise transforms between this section and the anchor section. This gives each section a X-to-anchor transform. The X-to-anchor transforms for all sections are stored in a pkl file.
      - Yuncong: "This is the basics, though partially innacurate"
    - REAL STEPS
* Generate Thumbnail mask
  - Requires GUI, using this program, you draw rough outlines, which are then shrinked by an algorithm called "active contour" to tightly fit the tissue content. [SKIP FOR NOW]


### Thionin (UCSD)
Not yet started.
### Detection/Classification
Not yet started.
### Registration/3D Construction
Not yet started.


## Setting up environment
metadata.py
distributed_utilities.py
