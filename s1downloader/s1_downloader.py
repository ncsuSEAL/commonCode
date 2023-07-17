#! /usr/bin/env python3
#################################################################################
# Title: S1_downloader.py
# Project: PNNL VIE Remote Sensing
# Script Purpose: Download and Process S1 Data from GEE
# Author: Jenna Abrahamson
# Last Updated: 07/17/2023
#################################################################################
#' Bulk download Sentinel-1 data from Google Earth Engine.
#'
#' This script downloads Sentinel-1 GRD SAR data from GEE. This script uses 
#' processing functions developed and described in Mullissa et al., 2021. 
#' Please see the associated paper at \href{https://www.mdpi.com/2072-4292/13/10/1954} or 
#' visit the GitHub repo at \href{https://github.com/adugnag/gee_s1_ard}.
#'
#' Running this script requires a GEE username and password. It will automatically 
#' open a browser window for the user to input this information. 

# Import necessary libraries
import argparse
from pathlib import Path
import ee
import eemont
import geemap  
import os
# From wrapper.py -> make sure in same workdir
from wrapper import s1_preproc

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
        description="CLI tool for downloading Sentinel-1 products from GEE. "
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


#' Generate params for GEE processing
#'
#' @description
#' Takes in user defined start and end dates, an input geojson AOI, and 
#' a specified output directory to download analysis ready Sentinel-1 
#' SAR data from GEE.
#' @param start Start date (str - "YYYY-MM-DD")
#' @param end End date (str - "YYYY-MM-DD")
#' @param aoi_path Path to geojson area of interest (str)
#' @param outdir Path to desired output dir to download to (str)
#'
#' @return A dictionary of params to use with s1_preproc()
#' @export

def create_params(start, end, aoi_path, outdir):
    
    # Check that dates are in correct format
    if len(start) != 10:
          print(f"{Colors.error} Incorrect start date format! {Colors.end}")
    if len(end) != 10:
          print(f"{Colors.error} Incorrect end date format! {Colors.end}")

    # Load geojson as ee object 
    roi_poly = geemap.geojson_to_ee(aoi_path)
    roi_geom = roi_poly.geometry()

    # Constuct dictionary of params
    params = {'APPLY_BORDER_NOISE_CORRECTION' : True, 
              'APPLY_TERRAIN_FLATTENING': True, 
              'APPLY_SPECKLE_FILTERING': True, 
              'POLARIZATION': 'VV', 
              'ORBIT' : 'ASCENDING', 
              'ORBIT_NUM' : None,
              'SPECKLE_FILTER_FRAMEWORK' : 'MULTI', 
              'SPECKLE_FILTER' : 'REFINED LEE', 
              'SPECKLE_FILTER_KERNEL_SIZE': 7, 
              'SPECKLE_FILTER_NR_OF_IMAGES': 10, 
              'TERRAIN_FLATTENING_MODEL': 'VOLUME', 
              'DEM' : ee.Image('USGS/SRTMGL1_003'), 
              'TERRAIN_FLATTENING_ADDITIONAL_LAYOVER_SHADOW_BUFFER' : 0,
              'FORMAT': 'DB', 
              'START_DATE' : start, 
              'STOP_DATE' : end, 
              'ROI' : roi_geom, 
              'CLIP_TO_ROI' : True, 
              'EXPORT_IMAGES' : True, 
              'OUT_DIR' : outdir}

    # Return params dict
    return params


# Run code
def main():

    # Parse command line arguments
    args = parser()
    outdir = args.outdir
    aoi_path = args.input_aoi
    start = args.start
    end = args.end

    # Initialize GEE
    ee.Authenticate()

    # Format params dict
    params = create_params(start, end, aoi_path, outdir)

    # Start Downloading
    print(f"{Colors.ok} Start Downloading S1... {Colors.end}")
    s1_preproc(params)

    print(f"{Colors.ok} Finished Downloading! {Colors.end}")


if __name__ == "__main__":
    main()
