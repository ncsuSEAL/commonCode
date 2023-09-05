# #! /usr/bin/env python3
# ##############################################################################
# # Author: Izzi Hinks
# # Title: planetdownloader.py
# ##############################################################################

# import asyncio
# import os
# import getpass
# # import planet
# from planet import Auth, Session
# import geojson
# import argparse
# from typing import Union
# from pathlib import Path
# from urllib.request import urlopen, urlretrieve
# import re
# import multiprocessing as mp
# import time

# ##############
# # Constants
# BUNDLES = ["analytic","analytic_udm2","analytic_3b_udm2",
#     "analytic_5b","analytic_5b_udm2","analytic_8b_udm2",
#     "visual","uncalibrated_dn","uncalibrated_dn_udm2",
#     "basic_analytic","basic_analytic_udm2","basic_analytic_8b_udm2",
#     "basic_uncalibrated_dn","basic_uncalibrated_dn_udm2","analytic_sr",
#     "analytic_sr_udm2","analytic_8b_sr_udm2","basic_analytic_nitf",
#     "basic_panchromatic","basic_panchromatic_dn","panchromatic",
#     "panchromatic_dn","panchromatic_dn_udm2","pansharpened",
#     "pansharpened_udm2","basic_l1a_dn"]
# ITEM_TYPES = ["REScene","SkySatScene","MOD09GA","SkySatCollect",
#     "PSOrthoTile","Sentinel2L1C","MYD09GA","MYD09GQ",
#     "REOrthoTile","MOD09GQ","Landsat8L1G","PSScene",
#     "Sentinel1"]
# api_key="../api_key.txt"

# ##############
# # Variables


# #############
# # Core

# def add(a, b): 
#     return a + b


# def sub(a, b): 
#     return a - b


# def mul(a, b): 
#     return a * b


# def div(a, b): 
#     return a / b

# def valid_date(s):
#     try:
#         return time.strptime(s, "%Y-%m-%d")
#     except ValueError:
#         msg = "not a valid date: {0!r}".format(s)
#         raise argparse.ArgumentTypeError(msg)

# def parser() -> argparse.Namespace:
#     """
#     Command line argument parser
#     """
#     # Args to make: 
#     global_parser = argparse.ArgumentParser(
#         prog="planetdownloader",
#         description="CLI tool for ordering and downloading Planet products",
#         epilog="NOTE: Thanks for using %(prog)s! This is a work in progress; \
#             please email irhinks@ncsu.edu if you run into any issues."
#     )

#     subp = global_parser.add_subparsers(dest = 'subparser_name')

#     arg_template = {
#         "dest": "operands",
#         "type": float,
#         "nargs": 2,
#         "metavar": "OPERAND",
#         "help": "a numeric value",
#     }

#     add_parser = subp.add_parser("add", help="add two numbers a and b")
#     add_parser.add_argument(**arg_template)
#     add_parser.set_defaults(func=add)

#     sub_parser = subp.add_parser("sub", help="subtract two numbers a and b")
#     sub_parser.add_argument(**arg_template)
#     sub_parser.set_defaults(func=sub)

#     mul_parser = subp.add_parser("mul", help="multiply two numbers a and b")
#     mul_parser.add_argument(**arg_template)
#     mul_parser.set_defaults(func=mul)

#     div_parser = subp.add_parser("div", help="divide two numbers a and b")
#     div_parser.add_argument(**arg_template)
#     div_parser.set_defaults(func=div)

#     create_p = subp.add_parser('create', help="Create a bla?")
#     create_p.add_argument('database', type = Path, help = "Database file")

#     scrape_p = subp.add_parser('scrape', help = 'Query something')
#     scrape_p.add_argument("--database", type = Path, help = "Database file")

#     # global_parser.add_argument(
#     #     "-g",
#     #     "--geojsons",
#     #     help="Path to directory of geojson files with which to crop imagery",
#     #     type=Path,
#     #     required=True,
#     # )
#     # global_parser.add_argument(
#     #     "-i",
#     #     "--ids",
#     #     help="Path to directory of files that include comma-separated lists of image IDs to download",
#     #     type=Path,
#     #     required=True,
#     # )
#     # global_parser.add_argument(
#     #     "-t",
#     #     "--itemtype",
#     #     help="Item type for requested item IDs. Default is PSScene",
#     #     choices=ITEM_TYPES,
#     #     default="PSScene",
#     #     nargs='+',
#     #     required=True,
#     # )   
#     # global_parser.add_argument(
#     #     "-b",
#     #     "--bundle",
#     #     choices=BUNDLES,
#     #     help="Type of asset type bundle desired. Default is analytic_udm2, which provides images, UDM layers, and metadata",
#     #     default="analytic_udm2",
#     #     nargs='+',
#     #     required=True,
#     # )
#     # global_parser.add_argument(
#     #     "-s",
#     #     "--start",
#     #     help="Start date of image search. Format: YYYY-MM-DD",
#     #     type=valid_date,
#     #     required=True,
#     # )
#     # global_parser.add_argument(
#     #     "-e",
#     #     "--end",
#     #     help="End date of image search. Format: YYYY-MM-DD",
#     #     type=valid_date,
#     #     required=True,
#     # )
#     # global_parser.add_argument(
#     #     "-c",
#     #     "--maxclouds",
#     #     help="Maximum cloud cover proportion allowed (0.00-0.99)",
#     #     type=float,
#     #     required=True,
#     # )
#     # global_parser.add_argument(
#     #     "-o",
#     #     "--outdir",
#     #     help="Output directory where ordered files will be exported",
#     #     type=Path,
#     #     required=True,
#     # )

#     # args = subp.parse_args()
#     args = global_parser.parse_args()

#     print(args.func(*args.operands))

#     return args


# def main():

#     # if os.path.exists(api_key):
#     #     with open(api_key) as f:
#     #         api_key = ([ln.split('#')[0].strip() for ln in f.readlines() if not ln.strip().startswith('#')] or [''])[0]
#     # else:
#     #     api_key = api_key
#     # try:
#     #     assert api_key.isalnum() and len(api_key) == 32
#     #     assert Auth.from_key(api_key)
#     # except AssertionError:
#     #     raise ValueError(f"Invalid Planet API key: '{api_key}'. Please pass API key or file path in --api_key argument")

#     start = time.time()

#     # Parse
#     args = parser()

#     # geojson_dir = Path(args.geojsons)
#     # id_dir = Path(args.ids)
#     # item_type = args.itemtype
#     # bundle_type = args.bundle
#     # start_date = args.start
#     # end_date = args.end
#     # max_cloud_prop = args.maxclouds
#     # outdir = Path(args.outdir)

#     # # Make individual directories
#     # id_dir.mkdir(parents=True, exist_ok=True)
#     # outdir.mkdir(parents=True, exist_ok=True)

#     # sent_dir = outdir / "S30"
#     # sent_dir.mkdir(parents=True, exist_ok=True)

#     # land_dir = outdir / "L30"
#     # land_dir.mkdir(parents=True, exist_ok=True)

#     # # Construct file url  lists
#     # dir_urls = construct_dir_urls(SENSORS, tiles, years)
#     # file_urls = construct_file_urls(dir_urls)

#     # # Create processing pool
#     # pool = mp.Pool(processes)
#     # print(f"Total files found: {len(file_urls)}")
#     # print(f"Using {mp.cpu_count()} threads")
#     # # Split processes
#     # pool.starmap(
#     #     downloader, [(file_urls[i], outdir, logfile) for i in range(len(file_urls))]
#     # )
#     print("Total time: ", time.time() - start)

# if __name__ == '__main__':
#     main()


#     # pargs.add_argument("-t", "--tiles", nargs="+", help="HLS tile names.")
#     # pargs.add_argument(
#     #     "-y",
#     #     "--years",
#     #     nargs="+",
#     #     default=[2015, 2016, 2017, 2018, 2019],
#     #     help="Years to download",
#     # )
#     # pargs.add_argument(
#     #     "-l", "--log", default="./failed.txt", help="File listing failed downloads"
#     # )
#     # pargs.add_argument(
#     #     "-p",
#     #     "--processes",
#     #     default=mp.cpu_count() // 2,
#     #     type=int,
#     #     help="Number of threads to split download between",
#     # )
#     # return pargs.parse_args()