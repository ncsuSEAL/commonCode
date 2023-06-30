# Download Sentinel-2 L2A Data

`S2_downloader.py` is adapted from `DownloadS2.R` (which can be found [here](https://github.com/ncsuSEAL/sealR/blob/master/R/DownloadSentinel2.R)) to allow for multiple tile downloads based on an input geojson AOI.

**Note:** This script only allows you to download L2A data. L2A data is provided since October 2016 and global since January 2017.
If you need data before this time period then you should download L1C data and process using Sen2Cor.

### Command Line Arguments:
-o\
--outdir\
type=str\
Output directory where all images will be downloaded into

-i\
--input_aoi\
type=str\
Path to geojson aoi
        
-s\
--start\
type=str\
Start date in the form YYYY-MM-DD
        
-e\
--end\
type=str\
End date in the form YYYY-MM-DD
    
### Example:
```
python3 S2_downloader.py -i "./aoi.geojson" -s "2020-01-01" -e "2023-01-01" -o "./S2_data"
```
