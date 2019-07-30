# Download and Match L1-L2 OCO-2 retrieval Data

This Code was used to Match L1 and L2 Data, provided by Nasa. It should be fully functional, when you create the required account and store the NASA password as described for the usage of curl: https://disc.gsfc.nasa.gov/data-access#mac_linux_curl.

The download paths, stored in the L1 and L2 folders seem still to work. If they are outdated by now, you can easily replace them with new ones from the GES DISC page https://disc.gsfc.nasa.gov/datasets?project=OCO  
For my project I used the **L2 Lite dataset:** `OCO2_L2_Lite_FP: OCO-2 Level 2 bias-corrected XCO2 and other select fields from the full-physics retrieval aggregated as daily files, Retrospective processing V9r`  
And **the L1b Dataset:** `OCO2_L1B_Science: OCO-2 Level 1B calibrated, geolocated science spectra, Retrospective Processing V8r`  

## Download scripts

**To download the L2 dataset** open the folder `L2_9000` and run `bash load.sh`.

**For the L1 dataset** open the folder `L1`, and run `bash start_load.sh`. In that file you can select for which month to download the L1 data, and for what kind of files to filter (Nadir: ND, Glint: GL, Target: TG, or XS).  
It will create a screen for each month so multiple downloads in parallel and continues to run while you are logged out.
NASA only allows a small number of concurrent downloads by a single user. The script waits when a download request is rejected.  


## After downloading 
the L1b and L2 files, they have to be read and matched.
The file `process.py` is responsible for matching the two File Types. The L2 data is relatively small and less files exist than for the L1 data. You might need to create a few folders to store the extracted data as done by the script.

At the end run `postprocess.py` to further sort out some problematic data.  

The code was used to create a dataset to learn the retrieval process with an Invertible Neural Network.

For questions and remarks, feel free to contact me at kleinicke@stud.uni-heidelberg.de
