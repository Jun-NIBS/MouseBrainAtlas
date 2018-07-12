This demo assumes a subject brain (DEMO999) is roughly globally aligned with the atlas (atlasV7).
It shows how one can:
- register 12N (hypoglossal nucleus) individually.
- register 3N_R (occulomotor, right) and 4N_R (trochlear, right) as a group.
- visualize the aligned atlas overlaid on original images

---------------------------

## Install packages, setup environment variables and download input data
```
sudo apt-get install wget python-pip
cd setup
sudo pip install -r requirements.txt
source set_env_variables.sh
cd ../demo
./download_demo_data.py
```

The input data are downloaded under `demo/demo_data`.

## Register 12N individually
- `$ ./register_brains_demo_12N.py`

## Register 3N_R and 4N_R as a group
- `$ ./register_brains_demo_3N_R_4N_R.py`

The program should finish in 2 minutes.

The outputs are also generated in _demo_data_ folder under the following paths. You can download the expected output from our S3 bucket using URLs formed by prepending https://s3-us-west-1.amazonaws.com/mousebrainatlas-data/ to the paths.

**Best set of transform parameters**
- `CSHL_registration_parameters/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_parameters.json`

**Optimization trajectory of transform parameters**
- `CSHL_registration_parameters/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_trajectory.bp`

**Score history**
- `CSHL_registration_parameters/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_scoreHistory.bp`

**Score evolution plot**
- `CSHL_registration_parameters/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_scoreEvolution.png`

**Simple globally aligned moving brain volumes**
- `CSHL_volumes/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp0_DEMO999_detector799_10.0um_scoreVolume_3N_4N_10.0um/score_volumes/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp0_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_3N_R.bp`

**Locally aligned moving brain volume**
- `CSHL_volumes/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N_10.0um/score_volumes/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_3N_R.bp`

------------------------

## Visualize registration results

To visualize the multi-probability level structures of the aligned atlas overlaid on original images:
- `$ ./visualize_registration_demo_3_structures.py`

An [example output image](example_atlas_overlay.jpg) is included in this repo.
White contours are the atlas after simple global registration.
Colored contours are the atlas after local registration. Different colors correspond to different probability levels. The  levels from outside in are 0.99, 0.75, 0.5, 0.25, 0.01.

The complete set of overlay images are under `CSHL_registration_visualization/DEMO999_atlas_aligned_multilevel_down16_all_structures/NtbNormalizedAdaptiveInvertedGammaJpeg/`
