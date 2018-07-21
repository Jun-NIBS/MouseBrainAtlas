## File Organization on S3

### Buckets

 Generated using AWS CLI command: `aws s3 ls` :
* 2017-09-13 11:19:25 mousebrainatlas-data
* 2018-06-26 18:09:52 mousebrainatlas-data-alexn
* 2017-08-14 12:23:57 mousebrainatlas-rawdata
* 2018-06-26 18:34:38 mousebrainatlas-rawdata-alexn
* 2017-05-16 15:59:36 mousebrainatlas-scripts
* 2018-07-10 20:10:09 mousebraindata-open
* 2017-05-10 17:30:28 yoav-seed-backup



##### Bucket 1: mousebrainatlas-data
- CSHL_data  **Yoav:**  I don't see this subdirectory of mousebrainatlas-data. [Here is the output of a current ls (7/21)](ListingOf_mousebrainatlas-data)
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

