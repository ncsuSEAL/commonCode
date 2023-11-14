# Walkthrough of downloading Planet imagery

#### Last edited June 16, 2023

#### Editors: Izzi

## Prerequisites: A virtual environment and the Planet SDK for Python

NOTE: You need to be using Python3 for this.

If you don't have the Planet SDK:

1. In your terminal, type: `python3 -m venv ~/.venv/planet-v2`
2. Then, type `source ~/.venv/planet-v2/bin/activate` to activate the virtual environment
3. Type `pip install planet --pre` to install the Planet SDK in the virtual environment
4. Type `planet --version` to ensure that you have installed version 2 of the SDK
5. Type `planet auth init` to sign on to your Planet account, entering the email and password of your Planet account when prompted. It should say "Initialized" once you have logged in.
6. Find your authentication key with: `planet auth value`. Either place the key in the `api_key.txt` file, or save the key as an environment variable with `export PL_API_KEY=<your api key>`. Check that it worked with `echo $PL_API_KEY` in your terminal.

This is the tl;dr version; find Planet's more thorough walkthrough [here](https://planet-sdk-for-python-v2.readthedocs.io/en/latest/get-started/quick-start-guide/#step-1-install-python-37-and-a-virtual-environment).

Then, make sure you have all of the required packages installed by adding all packages in `requirements.txt` in your environment. Visit [this site](https://frankcorso.dev/setting-up-python-environment-venv-requirements.html) to learn how to install packages from a `.txt` file into your virtual environment.

## Using the CLI

If you type `python planetdownloader --help` in your terminal, you should see:

```
usage: planetdownloader [-h] {list_ids,order,download} ...

CLI tool for ordering and downloading Planet products

positional arguments:
  {list_ids,order,download}
    list_ids            List Planet image IDs that meet certain criteria
    order               Order Planet data
    download            Download Planet orders

options:
  -h, --help            show this help message and exit

NOTE: Thanks for using planetdownloader! This is a work in progress; please email irhinks@ncsu.edu if you run into any issues.
```

## Getting IDlists (without ordering them)

**Skip this step if you want to order the imagery and not just receive the IDs of images of interest**

Type `python planetdownloader list_ids --help` in your terminal to see the arguments required to retrieve the image IDs of interest. There results will be:

```
usage: planetdownloader list_ids [-h] -g GEOJSON -t
                                 {REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1}
                                 [{REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} ...]
                                 -b
                                 {analytic,analytic_udm2,analytic_3b_udm2,analytic_5b,analytic_5b_udm2,analytic_8b_udm2,visual,uncalibrated_dn,uncalibrated_dn_udm2,basic_analytic,basic_analytic_udm2,basic_analytic_8b_udm2,basic_uncalibrated_dn,basic_uncalibrated_dn_udm2,analytic_sr,analytic_sr_udm2,analytic_8b_sr_udm2,basic_analytic_nitf,basic_panchromatic,basic_panchromatic_dn,panchromatic,panchromatic_dn,panchromatic_dn_udm2,pansharpened,pansharpened_udm2,basic_l1a_dn}
                                 -s START -e END -m MAXCLOUDS [-k APIKEY]

options:
  -h, --help            show this help message and exit
  -g GEOJSON, --geojson GEOJSON
                        Path to either a geojson file of the area of interest, or a directory of geojson files if you have multiple areas of interest
  -t {REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} [{REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} ...], --itemtype {REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} [{REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} ...]
                        Item type for requested images. Default is PSScene
  -b {analytic,analytic_udm2,analytic_3b_udm2,analytic_5b,analytic_5b_udm2,analytic_8b_udm2,visual,uncalibrated_dn,uncalibrated_dn_udm2,basic_analytic,basic_analytic_udm2,basic_analytic_8b_udm2,basic_uncalibrated_dn,basic_uncalibrated_dn_udm2,analytic_sr,analytic_sr_udm2,analytic_8b_sr_udm2,basic_analytic_nitf,basic_panchromatic,basic_panchromatic_dn,panchromatic,panchromatic_dn,panchromatic_dn_udm2,pansharpened,pansharpened_udm2,basic_l1a_dn}, --bundle {analytic,analytic_udm2,analytic_3b_udm2,analytic_5b,analytic_5b_udm2,analytic_8b_udm2,visual,uncalibrated_dn,uncalibrated_dn_udm2,basic_analytic,basic_analytic_udm2,basic_analytic_8b_udm2,basic_uncalibrated_dn,basic_uncalibrated_dn_udm2,analytic_sr,analytic_sr_udm2,analytic_8b_sr_udm2,basic_analytic_nitf,basic_panchromatic,basic_panchromatic_dn,panchromatic,panchromatic_dn,panchromatic_dn_udm2,pansharpened,pansharpened_udm2,basic_l1a_dn}
                        Type of product bundle desired. Default is analytic_sr_udm2, which provides 4-band surface reflectance images, UDM layers, and
                        metadata
  -s START, --start START
                        Start date of image search. Format: YYYY-MM-DD
  -e END, --end END     End date of image search. Format: YYYY-MM-DD
  -m MAXCLOUDS, --maxclouds MAXCLOUDS
                        Maximum cloud cover proportion allowed (0.00-0.99)
  -k APIKEY, --apikey APIKEY
                        Your Planet API key, if it has not already been added in the api_key.txt file or as an environment variable with key '$PL_API_KEY'
```

### Example: Retrieving image IDs with specific requirements

Here's an example of retrieving image IDs for 4-band surface reflectance PSScene images, UDM2 layers, and metadata with acquisition dates between 2022-01-01 (Jan 1, 2022) and 2022-03-01 (March 1, 2022) with a maximum allowed cloud proportion per tile of 0.99 (99% of the tile):

```
python planetdownloader list_ids --geojson <insert_path_to_geojson_here> --itemtype PSScene --bundle analytic_sr_udm2 --start 2022-01-01 --end 2022-03-01 --maxclouds 0.99
```

## Ordering Planet data

Typing `python planetdownloader order --help` in your terminal will show you the arguments required to order images:

```
usage: planetdownloader order [-h] -g GEOJSON -i IDS -t
                              {REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1}
                              [{REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} ...]
                              -b
                              {analytic,analytic_udm2,analytic_3b_udm2,analytic_5b,analytic_5b_udm2,analytic_8b_udm2,visual,uncalibrated_dn,uncalibrated_dn_udm2,basic_analytic,basic_analytic_udm2,basic_analytic_8b_udm2,basic_uncalibrated_dn,basic_uncalibrated_dn_udm2,analytic_sr,analytic_sr_udm2,analytic_8b_sr_udm2,basic_analytic_nitf,basic_panchromatic,basic_panchromatic_dn,panchromatic,panchromatic_dn,panchromatic_dn_udm2,pansharpened,pansharpened_udm2,basic_l1a_dn}
                              -s START -e END -m MAXCLOUDS [-bm {ndvi,evi2,ndwi} [{ndvi,evi2,ndwi} ...]] [-c] [-k APIKEY]

options:
  -h, --help            show this help message and exit
  -g GEOJSON, --geojson GEOJSON
                        Path to either a geojson file of the area of interest, or a directory of geojson files if you have multiple areas of interest
  -i IDS, --ids IDS     Path to directory of files that include comma-separated lists of image IDs to download
  -t {REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} [{REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} ...], --itemtype {REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} [{REScene,SkySatScene,MOD09GA,SkySatCollect,PSOrthoTile,Sentinel2L1C,MYD09GA,MYD09GQ,REOrthoTile,MOD09GQ,Landsat8L1G,PSScene,Sentinel1} ...]
                        Item type for requested item IDs. Default is PSScene
  -b {analytic,analytic_udm2,analytic_3b_udm2,analytic_5b,analytic_5b_udm2,analytic_8b_udm2,visual,uncalibrated_dn,uncalibrated_dn_udm2,basic_analytic,basic_analytic_udm2,basic_analytic_8b_udm2,basic_uncalibrated_dn,basic_uncalibrated_dn_udm2,analytic_sr,analytic_sr_udm2,analytic_8b_sr_udm2,basic_analytic_nitf,basic_panchromatic,basic_panchromatic_dn,panchromatic,panchromatic_dn,panchromatic_dn_udm2,pansharpened,pansharpened_udm2,basic_l1a_dn}, --bundle {analytic,analytic_udm2,analytic_3b_udm2,analytic_5b,analytic_5b_udm2,analytic_8b_udm2,visual,uncalibrated_dn,uncalibrated_dn_udm2,basic_analytic,basic_analytic_udm2,basic_analytic_8b_udm2,basic_uncalibrated_dn,basic_uncalibrated_dn_udm2,analytic_sr,analytic_sr_udm2,analytic_8b_sr_udm2,basic_analytic_nitf,basic_panchromatic,basic_panchromatic_dn,panchromatic,panchromatic_dn,panchromatic_dn_udm2,pansharpened,pansharpened_udm2,basic_l1a_dn}
                        Type of product bundle desired. Default is analytic_sr_udm2, which provides 4-band surface reflectance images, UDM layers, and
                        metadata
  -s START, --start START
                        Start date of image search. Format: YYYY-MM-DD
  -e END, --end END     End date of image search. Format: YYYY-MM-DD
  -m MAXCLOUDS, --maxclouds MAXCLOUDS
                        Maximum cloud cover proportion allowed (0.00-0.99)
  -bm {ndvi,evi2,ndwi} [{ndvi,evi2,ndwi} ...], --bandmath {ndvi,evi2,ndwi} [{ndvi,evi2,ndwi} ...]
                        You can optionally select one bandmath calculation to receive in your order
  -c, --clip            Add this argument to clip your images to your area of interest (your --geojson input)
  -k APIKEY, --apikey APIKEY
                        Your Planet API key, if it has not already been added in the api_key.txt file or as an environment variable with key '$PL_API_KEY'
```

Note that the `--geojson` parameter will allow for either the path to one single geojson file, or the path to a folder that entails many geojsons. The order functionality will automatically order the images for the single geojson or generate orders for each geojson in the folder.

### Example: Order imagery within a geojson

Ordering 4-band PSScene imagery (surface reflectance, UDM2, and metadata) within a specific geojson between 2022-01-01 and 2022-03-01. It will give you imagery with a max cloud proportion of 0.5 (50%) per tile, provide you with NDVI and EVI2 bands, and clip the images to the bounds of the geojson.

NOTE: The only bandmath options available currently are NDVI, EVI2, and NDWI. I will add more later!

```
planetdownloader order --geojson <insert_path_to_geojson_here> --itemtype PSScene --bundle analytic_sr_udm2 --start 2022-01-01 --end 2022-03-01 --maxclouds 0.5 --bandmath ndvi evi2 --clip
```

### Example: Order imagery for all geojson files in a directory

Create an order of 4-band PSScene imagery (surface reflectance, UDM2, and metadata) between 2022-01-01 and 2022-03-01 for each geojson in the folder. It will give you imagery with a max cloud proportion of 0.5 (50%) per tile, provide you with NDVI and EVI2 bands, and clip the images to the bounds of the geojson.

NOTE: The only bandmath options available currently are NDVI, EVI2, and NDWI. I will add more later!

```
planetdownloader order --geojson <insert_path_to_directory_here> --itemtype PSScene --bundle analytic_sr_udm2 --start 2022-01-01 --end 2022-03-01 --maxclouds 0.5 --bandmath ndvi evi2 --clip
```

## Downloading Planet orders

Typing `python planetdownloader download --help` in your terminal will show you the arguments required to order images to your desired folder:

```
usage: planetdownloader download [-h] -s START -e END -os {queued,running,failed,success,partial,cancelled}
                                 [{queued,running,failed,success,partial,cancelled} ...] -o OUTDIR [-p PROCESSES] [-k APIKEY]

options:
  -h, --help            show this help message and exit
  -s START, --start START
                        Start date of image search. Format: YYYY-MM-DD
  -e END, --end END     End date of image search. Format: YYYY-MM-DD
  -os {queued,running,failed,success,partial,cancelled} [{queued,running,failed,success,partial,cancelled} ...], --orderstate {queued,running,failed,success,partial,cancelled} [{queued,running,failed,success,partial,cancelled} ...]
                        Order state of interest
  -o OUTDIR, --outdir OUTDIR
                        Output directory where ordered files will be exported
  -p PROCESSES, --processes PROCESSES
                        Number of threads between which to split the downloads
  -k APIKEY, --apikey APIKEY
                        Your Planet API key, if it has not already been added in the api_key.txt file or as an environment variable with key '$PL_API_KEY'
(planet-v2) (base) irhinks@Hinks-MBA planetdownloader %
```

### Example: Download successful orders created between two dates

To download all successful orders created between 2023-08-20 and 2023-09-04 and place them into a specific directory:

Note that the CLI will automatically create a subdirectory in which it will place data for each order.

```
python planetdownloader download --start 2023-08-20 --end 2023-09-04 --orderstate success --outdir <dir_in_which_to_download_orders>
```

## Common Planet errors
* If you get a `HTTPStatusError: Client error '400 Bad Request'` error first triple check that your syntax for the order is correct. If that looks correct, the error may be due to your request containing satellites that cannot product `analytic_sr` assets because they have either a different hardware configuration, are an old-generation satellite, or an experimental satellite. Known satellite IDs that fall into this category are `0c81`, `0c1b`, `0c76`, `0c65`, `0c43`, `0f06`, `0c37`, `1105`, `0f02`, `0c54` and `0f1c`. If you have any of these satellite products found in your order (for example, `20161102_173224_0c76`), remove their item IDs and this should allow the order to be placed successfully.
* If you get a `HTTPStatusError: Server error: '500 Internal Server Error'` error check that your orders are being split into a maximum of 100 items at a time. This error tends to occur if you get close to Planet's maximum 500 items per order and will cause the order to not be able to download properly. It is recommended by Planet that orders be submitted in batches of 100 items at a time.

