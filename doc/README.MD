# Documentation Files
 Following are all of the documentation files and user guides for the Atlas code. Having had multiple developers working on it, there are documentation files deemed "historical" that were made by earlier developers. Certain documents are also marked as incomplete and should be ignored by non-developers. Several "historical" files are unmarked as they are not outdated.

## User Guide
**[In Development]** [Alex User Guide](RunningFiles.md)
  - Running Guide made by AlexN to assist with running the code:
     1. Preprocessing
     2. Registration
     3. Visualization
     4. Atlas Building
     5. ...


## Server Information
Anything having to do with the BirdStore and S3 servers this project uses. S3 is the primary location of all data and interfacing with it may be necessary. BirdStore, as of right now, is synced with S3 but is not used directly for file retrieval.
- [AWS Instructions](writeup/AWS_instruction.md)
  - Guide for transferring files to/from AWS S3 and Birdstore as well as running code on AWS with CfnCluster

## File Organization
These files contain information on what software is needed to run the code, how all of the processed data is organized both locally and on relevant servers, and a catalog of every brain that has gone through the code.
- [Software Dependancies](dependancies.md)
  - List of all packages that need to be installed 
- [Data File Organization](writeup/S3_file_organization.md)
  - Naming conventions in S3 storage
- [Stack Directories](Brain_stack_directories.md)
  - Description of every stack, all relevant information

### Historical
- [List of historical documentation files](HistoricalFileList.md)
