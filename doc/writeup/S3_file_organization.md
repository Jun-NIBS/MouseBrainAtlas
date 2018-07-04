### File Organization on S3

##### Bucket 1: mousebrainatlas-data
- CSHL_data
  - MD###                 '###' is a 3 digit brain designation
    - *_lossless.jp2 
    - *.lossy.jp2    
    - *.tif     
    - *.png    
    
*_lossless.jp2 is the only file that is NOT a thumbnail. Everything else is downsized.

##### Bucket 2: mousebrainatlas-rawdata
A lot of stuff here, will take a while.


### Leftover from Yuncong

Resolution string
resol:
- lossless
- thumbnail
- down8

Intensity-related string
int:
- linearNormalized500
- linearNormalized2000
- linearNormalized500_jpeg
- gray
- gray_jpeg
- mask
- [empty string]
- jpeg
- tif

