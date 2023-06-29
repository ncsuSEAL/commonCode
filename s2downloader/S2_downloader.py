#! /usr/bin/env python3
#################################################################################
# Title: S2_downloader.py
# Script Purpose: Download S2 L2A data from Copernicus
# Author: Jenna Abrahamson, adapted from Xiaojie Gao/Ian McGregor's DownloadS2.R
#################################################################################

#' Download Sentinel 2 dataset from Google Cloud.
#'
#' This script downloads all Sentinel 2 images (L2A) from
#' \href{https://console.cloud.google.com/storage/browser/gcp-public-data-sentinel-2?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&prefix=&forceOnObjectsSortingFiltering=false}{Google's repository}(.
#' These images are the same as if you downloaded these from ESA Copernicus, but faster (i.e. you don't have to
#' request images and wait for them). Note that Google does not do their own L2A conversion - all L2A images
#' are supplied directly from Copernicus (true as of November 2022).
#'
#' Running this function requires Google Cloud Storage SDK, which you can download and install
#' from \href{https://cloud.google.com/sdk/docs/install}{here}. For your first time attempting to run the function
#' you will need to open a python or terminal script and run `gcloud auth login`, which will take you to log in to your
#' google account.
#'
#' Note: L2A data is provided since October 2016 and global since January 2017;
#' if you need to go further back then that then you will have to process L1 data
#' using Sen2Cor which IS NOT done in this script.

##############
# Import packages
import argparse
from pathlib import Path
import os
import subprocess
from datetime import date, timedelta
import pandas as pd
import geopandas as gpd

##############
# Constants
URL = "gs://gcp-public-data-sentinel-2/L2/tiles"

#############
# Misc
class Colors:
    cyan = "\033[96m"
    ok = "\033[92m"
    warning = "\033[93m"
    error = "\033[91m"
    end = "\033[0m"


#############
# Core
def parser():
    """
    Command line argument parser
    """
    pargs = argparse.ArgumentParser(
        description="CLI tool for downloading L2A Sentinel products. "
    )
    pargs.add_argument(
        "-o",
        "--outdir",
        type=str,
        help="Output directory where all images will be downloaded into",
    )
    pargs.add_argument(
        "-i", 
        "--input_aoi", 
        type=str, 
        help="Path to geojson aoi"
    )
    pargs.add_argument(
        "-s", 
        "--start", 
        type=str, 
        help="Start date in the form YYYY-MM-DD",
    )
    pargs.add_argument(
        "-e", 
        "--end", 
        type=str, 
        help="End date in the form YYYY-MM-DD",
    )
    return pargs.parse_args()

def identify_tiles(aoi_path: str, mgrs_path: str) -> list:
    """
    Identify tiles to download

    Args:
        aoi_path
        mgrs_path

    Returns:
        list
    """

    # Load mgrs geojson
    mgrs_geo = gpd.read_file(mgrs_path)
    # Load aoi geojson
    aoi_geo = gpd.read_file(aoi_path)

    # Find tiles where they intersect
    tiles = list(gpd.overlay(mgrs_geo, aoi_geo, how = "intersection")['Name'].unique())

    return(tiles)
  
def construct_file_urls(tiles: list) -> list:
    """
    Construct the urls for S2 file directories

    Args:
        tiles

    Returns:
        list
    """
    # Initiate list of file urls
    file_urls = []

    # Check for multiple tiles, run w/ 1 tile
    if len(tiles) == 1:
        tile = tiles[0]
        # Dir structure
        file_list = f"{URL}/{tile[0:2]}/{tile[2]}/{tile[3:5]}"
        # Create gsutil command
        com = f"gsutil ls {file_list}"
        # Get file urls
        proc = os.popen(com).read().strip()
        result_items = proc.split("\n")

        # Append to list
        file_urls.append(result_items)

    # Run with multiple tiles
    elif len(tiles) > 1:
        for tile in tiles:
            # Dir structure
            file_list = f"{URL}/{tile[0:2]}/{tile[2]}/{tile[3:5]}"
            # Create gsutil command
            com = f"gsutil ls {file_list}"
            # Get file urls
            proc = os.popen(com).read().strip()
            result_items = proc.split("\n")

            # Append to list
            file_urls.append(result_items)

    else:
        print(f"{Colors.error}Error parsing tiles, check tiles input!")

    return file_urls


def query_by_date(start_date: str, end_date: str, file_urls: list) -> str:
    """
    Query dates to keep only images within specified date range

    Args:
        start_date 
        end_date
        file_urls

    Returns:
        list
    """

    # Turn to date objects
    sdate = date(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
    edate = date(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))

    # Generate list of all possible dates
    dates = pd.date_range(sdate, edate - timedelta(days=1), freq="d")
    date_char = [date_obj.strftime("%Y%m%d") for date_obj in dates]

    # Keep any images that match date range

    # For one tile
    if len(file_urls) == 1:
        s2_links = file_urls[0]
        keep_dates = [j for j in date_char if all(j not in k for k in s2_links)]

        keep_links = []
        for i in date_char:
            for j in s2_links:
                if i in j:
                    keep_links.append(j)
        return keep_links

    # For multiple tiles
    elif len(file_urls) > 1:
        tile_links = []
        for x, tile_urls in enumerate(file_urls):
            s2_links = file_urls[x]
            keep_dates = [j for j in date_char if all(j not in k for k in s2_links)]

            keep_links = []
            for i in date_char:
                for j in s2_links:
                    if i in j:
                        keep_links.append(j)
            tile_links.append(keep_links)

        return tile_links

    # If zero links found, return error
    else:
        print(f"{Colors.error}Error in query_by_date: no file urls found!")


def downloader(subset_list: list, tiles: list, outdir: str) -> list:
    """
    Download files

    Args:
        subset_list
        tiles

    Returns:
        Downloads S2 data to tile directories
    """

    file_urls = subset_list

    # Download for multiple tiles
    if len(tiles) > 1:
        for img_dir in file_urls:
            for i, image in enumerate(img_dir):

                # Match tile
                for tile in tiles:
                    if tile in img_dir[i]:
                        tile_id = tile
                    else:
                        continue

                # Create output folder if doesn't exist
                outpath = outdir / tile_id
                check = os.path.isdir(outpath)
                if not check:
                    os.makedirs(outpath)
                    print(f"{Colors.cyan}Created folder: {outpath}{Colors.end}")


                # Get clean link
                file = img_dir[i][0:114]
                dir_outpath = outdir / tile_id
                file_outpath = dir_outpath / file[49:114]

                # Check if file has already been downloaded
                if os.path.exists(file_outpath):
                    continue

                # If not, start downloading
                print(f"{Colors.ok}Downloading...: {image[49:114]}{Colors.end}")

                # note '-m' flag issue can happen depending on 
                # python installation, see https://bugs.python.org/issue33725
                os.system(f"gsutil -m cp -r {file}/ {dir_outpath}/.")

    # Download for one tile
    if len(tiles) == 1:
        img_dir = file_urls
        for i, image in enumerate(img_dir):

            # Match tile
            tile_id = tiles[0]

            # Create output folder if doesn't exist
            outpath = outdir / tile_id
            check = os.path.isdir(outpath)
            if not check:
                os.makedirs(outpath)
                print(f"{Colors.cyan}Created folder: {outpath}{Colors.end}")

            # Get clean link
            file = img_dir[i][0:114]
            dir_outpath = outdir / tile_id
            file_outpath = dir_outpath / file[49:114]

            # Check if file has already been downloaded
            if os.path.exists(file_outpath):
                continue

            # If not, start downloading
            print(f"{Colors.ok}Downloading...: {image[49:114]}{Colors.end}")

            # note '-m' flag issue can happen depending on 
            # python installation, see https://bugs.python.org/issue33725
            os.system(f"gsutil -m cp -r {file}/ {dir_outpath}/.")


def main():

    # Parse command line arguments
    args = parser()
    outdir = Path(args.outdir)
    aoi_path = args.input_aoi
    start = args.start
    end = args.end

    # Load mgrs grid
    mgrs_path = "./S2_mgrs_tiles.geojson"

    # Find intersecting tiles
    tiles = identify_tiles(mgrs_path, aoi_path)
    # Construct file url lists
    file_list = construct_file_urls(tiles)
    # Query images by date range
    subset_list = query_by_date(start, end, file_list)
    # Download images
    download = downloader(subset_list, tiles, outdir)

    print(f"{Colors.cyan}Finished Downloading!{Colors.end}")


if __name__ == "__main__":
    main()
