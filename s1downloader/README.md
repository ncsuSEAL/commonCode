# Download Sentinel-1 Analysis Ready Data

This script downloads bulk Sentinel-1 SAR ARD from Google Earth Engine. This script uses 
processing functions developed and described in Mullissa et al., 2021. 
Please see the associated [paper](https://www.mdpi.com/2072-4292/13/10/1954) or 
visit the GitHub [repo](https://github.com/adugnag/gee_s1_ard) for more information.

Running this script requires a GEE username and password. It will automatically 
open a browser window for the user to input this information. 

**Note:** This script is currently set up to return only VV polarization, informetric wide (IW) swath mode, 
and ascending orbit filtered S1 data. You will have to modify the `params` dictionary in `s1_downloader.py` if you would like to change these parameters. 

### Command Line Arguments:
```
-o, --outdir
type=str
Output directory where all images will be downloaded into
```
```
-i, --input_aoi
type=str
Path to geojson AOI
```
```   
-s, --start
type=str
Start date in the form YYYY-MM-DD
```
```
-e, --end
type=str
End date in the form YYYY-MM-DD
```

    
### Example:
```
python3 s1_downloader.py -i "./aoi.geojson" -s "2020-01-01" -e "2023-01-01" -o "./S1_data"
```
