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

##### Bucket mousebrainatlas-data

`aws ls s3://mousebrainatlas-data/`
 
* CSHL_SPM/
* CSHL_annotation_viz/
* CSHL_cells_v2/
* CSHL_classifiers/
* CSHL_data_processed/
* CSHL_labelings_thalamus/
* CSHL_labelings_v3/
* CSHL_meshes/
* CSHL_patch_features/
* CSHL_patch_locations/
* CSHL_patch_scores/
* CSHL_registration_parameters/
* CSHL_registration_visualization/
* CSHL_registration_visualization_atlasV5/
* CSHL_registration_viz_juxtaposed/
* CSHL_scoremap_viz/
* CSHL_scoremap_viz_grid/
* CSHL_scoremaps/
* CSHL_simple_global_registration/
* **CSHL_volumes/** the location of the information about the shape of the structures.
   * The directory Yoav used to create a 3D visualization of the atlas: CSHL_volumes/atlasV7/atlasV7_10.0um_scoreVolume/score_volumes/
* Dropbox/
* HRNTS2017/
* LGN3Datlas/
* blob_matching_atlas/
* image_examples/
* image_examples_raw/
* lauren_data/
* mxnet_models/
* raw_image_histograms/
* raw_image_histograms_fullImage/
* raw_image_histograms_log/
* raw_image_histograms_log_fullImage/
* stacy_data/
* training_examples/

- CSHL_data  **Yoav:**  I don't see this subdirectory of mousebrainatlas-data. [Here is the output of a current ls (7/21)](ListingOf_mousebrainatlas-data)
  - MD###                 '###' is a 3 digit brain designation
    - *_lossless.jp2 
    - *.lossy.jp2    
    - *.tif     
    - *.png    
    
*_lossless.jp2 is the only file that is NOT a thumbnail. Everything else is downsized.

##### Bucket 2: mousebrainatlas-rawdata
A lot of stuff here, will take a while.

