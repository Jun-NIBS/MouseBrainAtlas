# Documentation Files
 Following are all of the documentation files and user guides for the Atlas code. Having had multiple developers working on it, there are documentation files deemed "historical" that were made by earlier developers. Certain documents are also marked as incomplete and should be ignored by non-developers.

## User Guide
**[In Development]** [Alex User Guide](RunningFiles.md)
  - Running Guide made by AlexN to assist with running the code:
     1. Preprocessing
     2. Registration
     3. Visualization
     4. Atlas Building
     5. ...
     
**[Historical]** [Yuncong User Guide](User%20Manuals/UserGuide.md)
  - User Guide made by Yuncong to assist with running the code. Currently the most complete guide of the code, use this if in doubt.

### Historical
- **[Historical]** [Dev Guide](DeveloperGuide.md)
  - Incomplete to-be guide of entire running process
- **[Historical]** [Registration Steps](Analysis.md)
  - Guide for Registration with list of relevant scripts
- **[Historical]** [Old README](old_readme.md)
  - Yuncong's old README

## Server Information
Anything having to do with BirdStore and S3.
- [AWS Instructions](writeup/AWS_instruction.md)
  - Guide for transferring files to/from AWS S3 and Birdstore as well as running code on AWS with CfnCluster

## File Organization
- [Software Dependancies](dependancies.md)
  - List of all packages that need to be installed 
- [Data File Organization](writeup/S3_file_organization.md)
  - Naming conventions in S3 storage
- [Stack Directories](Brain_stack_directories.md)
  - Description of every stack, all relevant information

## Machine Learning Documents
- **[Historical]** [Bayesian Parameters](writeup/bayesian.md)
  - Parameters and associated uncertainty in Atlas building process
- **[Historical]** [Uncertainty](writeup/zscore_hessian.md)
  - Z-score and Hessians used to quantify uncertainty
