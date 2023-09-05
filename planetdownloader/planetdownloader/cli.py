#! /usr/bin/env python3
################################################################################
# Author: Izzi Hinks
# Title: cli.py
################################################################################

import argparse, order, download, list_ids, os, time, asyncio
from planet import Auth, OrdersClient, collect, Session, data_filter
from pathlib import Path
from datetime import datetime
import multiprocessing as mp

# Constant variables
AOI_POLY = ""
# ID_PATH = ""
ITEM_TYPE = ""
BUNDLE = ""
START_DATE = ""
END_DATE = ""
MAX_CLOUDS = 0.99
BANDMATH = ""
CLIP_BOOL = False
OUT_DIR = ""
PROCESSES = 0
API_KEY = ""


# Helper functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def valid_date(s):
    try:
        # return time.strptime(s, "%Y-%m-%d")
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


def proportion(n):
    num = float(n)
    try:
        if 0 <= num < 1:
            return num
    except ValueError:
        msg = "not a valid proportion: {%d}; needs to be 0.00-0.99".format(num)
        raise argparse.ArgumentTypeError(msg)


def prep_dir(d):
    try:
        dir_path = Path(d)
        if dir_path.is_file():
            # TODO: Make sure the file is a geojson
            # print("file path is: ", dir_path)
            return dir_path
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
            # print("directory: ", dir_path)
            return dir_path
    except ValueError:
        msg = "--geojson argument must either be a single .geojson file or a directory that holds multiple .geojson files (if you have multiple AOIs)"
        raise argparse.ArgumentTypeError(msg)


def login_to_planet(key_arg):
    if key_arg is not None:  # API Key as an argument
        API_KEY = key_arg
    elif os.environ.get("PL_API_KEY", ""):  # API Key stored in an environment variable
        API_KEY = os.environ.get("PL_API_KEY", "")
    else:
        api_key_file = os.path.join(os.path.dirname(__file__), "api_key.txt")
        if os.path.exists(api_key_file):  # API Key in the api_key.txt file
            with open(api_key_file) as f:
                API_KEY = f.readline().strip()

    try:
        assert (
            API_KEY.isalnum() and len(API_KEY) == 32
        )  # all 32 characters are either alphabetic or numeric
        return Auth.from_key(API_KEY)
    except AssertionError:
        raise ValueError(
            f"Invalid Planet API key: '{API_KEY}'. Please add your API key to the api_key.txt file, as the '$PL_API_KEY' environment variable, or as the --api_key argument"
        )


def parser() -> argparse.Namespace:
    """
    Command line argument parser
    """

    # Create a parser to enable multiple modules
    global_parser = argparse.ArgumentParser(
        prog="planetdownloader",
        description="CLI tool for ordering and downloading Planet products",
        epilog="NOTE: Thanks for using %(prog)s! This is a work in progress; \
            please email irhinks@ncsu.edu if you run into any issues.",
    )

    # Add subparser to enable subcommands
    subp = global_parser.add_subparsers(dest="subcommands")

    # Add a new parser for each subcommand
    # login.add_arguments(subp) # Subcommand to log in to the Planet API
    list_ids.add_arguments(subp)  # Subcommand to get Planet image IDs of interest
    order.add_arguments(subp)  # Subcommand to order imagery
    download.add_arguments(subp)  # Subcommand to download imagery

    return global_parser.parse_args()


# Main function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    # start = time.time()

    # Retrieve arguments from parser
    args = parser()

    # Log in to Planet's API
    pl_client = login_to_planet(args.apikey)

    if args.subcommands == "list_ids":
        AOI_POLY = prep_dir(args.geojson)
        # ID_PATH = prep_dir(args.ids)
        ITEM_TYPE = args.itemtype
        BUNDLE = args.bundle
        START_DATE = args.start
        END_DATE = args.end
        MAX_CLOUDS = args.maxclouds
        # BANDMATH = args.bandmath
        # CLIP_BOOL = args.clip
        print("Listing all Planet image IDs that match all constraints...")
        result = list_ids.list_ids(
            AOI_POLY, ITEM_TYPE, BUNDLE, START_DATE, END_DATE, MAX_CLOUDS, pl_client
        )

    # Order imagery
    elif args.subcommands == "order":
        # Assign arguments to be the values of the constant variables
        # print("It was order!")
        AOI_POLY = prep_dir(args.geojson)
        if args.ids is not None:
            ID_PATH = prep_dir(args.ids)
        ITEM_TYPE = args.itemtype
        BUNDLE = args.bundle
        START_DATE = args.start
        END_DATE = args.end
        MAX_CLOUDS = args.maxclouds
        BANDMATH = args.bandmath
        CLIP_BOOL = args.clip

        if AOI_POLY.is_file():
            # Order imagery using the user's arguments
            result = order.order_imagery(
                AOI_POLY,
                # ID_PATH,
                ITEM_TYPE,
                BUNDLE,
                START_DATE,
                END_DATE,
                MAX_CLOUDS,
                BANDMATH,
                CLIP_BOOL,
                pl_client,
            )
        elif AOI_POLY.is_dir():
            # For each geojson in this directory:
            for polygon_file in AOI_POLY.glob("*.geojson"):
                # Order the imagery for this geojson using the user's arguments
                result = order.order_imagery(
                    polygon_file,
                    # ID_PATH,
                    ITEM_TYPE,
                    BUNDLE,
                    START_DATE,
                    END_DATE,
                    MAX_CLOUDS,
                    BANDMATH,
                    CLIP_BOOL,
                    pl_client,
                )
    # Download imagery
    elif args.subcommands == "download":
        # print("It was download!")
        START_DATE = args.start
        END_DATE = args.end
        ORDER_STATE = args.orderstate
        OUT_DIR = prep_dir(args.outdir)
        PROCESSES = args.processes

        print(OUT_DIR)

        # Gather orders that were ordered between the start and end dates
        order_names, orders_of_interest = asyncio.run(
            order.list_orders(START_DATE, END_DATE, ORDER_STATE)
        )
        # print(orders_of_interest)

        outcome = asyncio.run(
            download.download_orders(
                order_names, orders_of_interest, OUT_DIR, PROCESSES
            )
        )


if __name__ == "__main__":
    main()
