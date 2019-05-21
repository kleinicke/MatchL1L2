# Download and Match L1-L2 OCO-2 retrieval Data

This Code was used to Match L1 and L2 Data, provided by Nasa. It should be fully functional, when you create the required account and store the NASA password as described for the usage of wget: https://disc.gsfc.nasa.gov/data-access#windows_wget.
The download paths might be outdated by now. You can easily get new ones from the GES DISC page https://disc.gsfc.nasa.gov/datasets?project=OCO  
For my project I used the L2 Lite dataset: OCO2_L2_Lite_FP: OCO-2 Level 2 bias-corrected XCO2 and other select fields from the full-physics retrieval aggregated as daily files, Retrospective processing V9r  
And the L1b Dataset: OCO2_L1B_Science: OCO-2 Level 1B calibrated, geolocated science spectra, Retrospective Processing V8r  


To download the L2 dataset open the folder `L2_9000` and run 
```
load.sh subset_OCO2_L2_Lite_FP_V9r_20190308_141525.txt
```
For the L1 dataset open the folder `L1`, change the subfolders in `start_load` and run it.  
It will create a screen for each file to download. You might want to only have one file to download per month instead up to 5. 
NASA only allows a one digit number of concurrent downloads. The script waits when a download request is rejected.  
It filters the data and will only download Nadir Data. To download Glimp data the filter has to be changed in the L1 download file.

The file `process.py` is responsible for matching the two File Types. The L2 data is relatively small and less files exist than for the L1 data.  
At the end I run `postprocess.py` to further sort out some problematic data.  

The code was used to create a dataset to learn the retrieval process with an Invertible Neural Network.
