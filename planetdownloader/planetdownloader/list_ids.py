#! /usr/bin/env python3
################################################################################
# Author: Izzi Hinks
# Title: list_ids.py
################################################################################

import argparse, cli, ntpath, os, geojson, json, asyncio
from pathlib import Path
from planet import data_filter, Session, order_request, reporting, collect

# Constant variables
BUNDLES = [
    "analytic",
    "analytic_udm2",
    "analytic_3b_udm2",
    "analytic_5b",
    "analytic_5b_udm2",
    "analytic_8b_udm2",
    "visual",
    "uncalibrated_dn",
    "uncalibrated_dn_udm2",
    "basic_analytic",
    "basic_analytic_udm2",
    "basic_analytic_8b_udm2",
    "basic_uncalibrated_dn",
    "basic_uncalibrated_dn_udm2",
    "analytic_sr",
    "analytic_sr_udm2",
    "analytic_8b_sr_udm2",
    "basic_analytic_nitf",
    "basic_panchromatic",
    "basic_panchromatic_dn",
    "panchromatic",
    "panchromatic_dn",
    "panchromatic_dn_udm2",
    "pansharpened",
    "pansharpened_udm2",
    "basic_l1a_dn",
]
ITEM_TYPES = [
    "REScene",
    "SkySatScene",
    "MOD09GA",
    "SkySatCollect",
    "PSOrthoTile",
    "Sentinel2L1C",
    "MYD09GA",
    "MYD09GQ",
    "REOrthoTile",
    "MOD09GQ",
    "Landsat8L1G",
    "PSScene",
    "Sentinel1",
]


# Helper functions
def path_base(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def add_arguments(parser):
    ids_p = parser.add_parser(
        "list_ids", help="List Planet image IDs that meet certain criteria"
    )

    ids_p.add_argument(
        "-g",
        "--geojson",
        help="Path to either a geojson file of the area of interest, or a directory of geojson files if you have multiple areas of interest",
        type=Path,
        required=True,
    )
    ids_p.add_argument(
        "-t",
        "--itemtype",
        help="Item type for requested images. Default is PSScene",
        choices=ITEM_TYPES,
        default="PSScene",
        nargs="+",
        required=True,
    )
    # TODO: add functionality for fallback bundles: . "To specify a fallback asset type bundle, place it after your preferred asset type with a space between the types (e.g., '--bundle analytic_sr_udm2 analytic_sr')"
    ids_p.add_argument(
        "-b",
        "--bundle",
        choices=BUNDLES,
        help="Type of product bundle desired. Default is analytic_sr_udm2, which provides 4-band surface reflectance images, UDM layers, and metadata",
        default="analytic_sr_udm2",
        # nargs="+",
        nargs=1,
        required=True,
    )
    ids_p.add_argument(
        "-s",
        "--start",
        help="Start date of image search. Format: YYYY-MM-DD",
        type=cli.valid_date,
        required=True,
    )
    ids_p.add_argument(
        "-e",
        "--end",
        help="End date of image search. Format: YYYY-MM-DD",
        type=cli.valid_date,
        required=True,
    )
    ids_p.add_argument(
        "-m",
        "--maxclouds",
        help="Maximum cloud cover proportion allowed (0.00-0.99)",
        type=cli.proportion,
        required=True,
    )
    ids_p.add_argument(
        "-k",
        "--apikey",
        help="Your Planet API key, if it has not already been added in the api_key.txt file or as an environment variable  with key '$PL_API_KEY'",
        type=str,
        required=False,
    )

    return parser


# Combines all of the user's image constraints into a group of filters
# TODO: add view angle, permission filter, standard quality filter, clear pct, and also max/limit of results to return (0 if no maximum)
def create_combined_filter(
    AOI_POLY, ITEM_TYPE, BUNDLE, START_DATE, END_DATE, MAX_CLOUDS
):
    asset_filter = data_filter.asset_filter(BUNDLE)
    geom_filter = data_filter.geometry_filter(AOI_POLY)
    clear_percent_filter = data_filter.range_filter("clear_percent", 90)
    date_range_filter = data_filter.date_range_filter(
        "acquired", gte=START_DATE, lte=END_DATE
    )
    cloud_cover_filter = data_filter.range_filter("cloud_cover", None, MAX_CLOUDS)

    combined_filter = data_filter.and_filter(
        [geom_filter, clear_percent_filter, date_range_filter, cloud_cover_filter]
    )
    return combined_filter


# Search Planet's Data API
async def search_planet_api(poly_id, combined_filter, ITEM_TYPE):
    async with Session() as sess:
        cl = sess.client("data")
        request = await cl.create_search(
            name=poly_id,
            search_filter=combined_filter,
            item_types=ITEM_TYPE,
        )

    # The limit paramter allows us to limit the number of results from our search that are returned.
    # The default limit is 100. Here, we're setting our result limit to 50.
    # TODO: Go back and adjust the limit to a better default value
    async with Session() as sess:
        cl = sess.client("data")
        items = cl.run_search(search_id=request["id"], limit=10000000)
        # item_list = [i async for i in items]
        item_list = [i["id"] async for i in items]
        return item_list


def list_ids(
    AOI_POLY,
    ITEM_TYPE,
    BUNDLE,
    START_DATE,
    END_DATE,
    MAX_CLOUDS,
    pl_client,
):
    # if AOI_POLY.is_file():
    #     print("AOI is one geojson")
    base_path = path_base(AOI_POLY)

    # ID_file = open(os.path.join(ID_PATH, "filtered_" + base_path), "r")
    poly_id = base_path[0:-8]
    print("Gathering Planet image IDs for AOI: ", base_path)

    with open(AOI_POLY, "r") as f:
        # Load the geojson and grab the geometry of interest
        gj = geojson.load(f)
        geom = gj["features"][0]["geometry"]

        # Create a single filter with all of the user's needs
        combined_filter = create_combined_filter(
            geom, ITEM_TYPE, BUNDLE, START_DATE, END_DATE, MAX_CLOUDS
        )
        # print(combined_filter)

        item_list = asyncio.run(search_planet_api(poly_id, combined_filter, ITEM_TYPE))
        print(item_list)

        # # Retrieve the optional tools the user has selected
        # # tool_list = add_order_tools(geom, CLIP_BOOL, BANDMATH)

        # if len(item_list) > 500:
        #     print(
        #         "There are over 500 bundles in this order; automatically splitting the order into multiple orders..."
        #     )
        #     for i in range(0, len(item_list), 500):
        #         item_subset = item_list[i : i + 500]
        #         # Create order request

        # else:
        #     # Create order request
        #     aoi_order = order_request.build_request(
        #         name=poly_id + " order",
        #         products=[
        #             order_request.product(
        #                 item_ids=item_list,
        #                 product_bundle=str(BUNDLE[0]),
        #                 item_type=str(ITEM_TYPE[0]),
        #             )
        #         ],
        #         tools=tool_list,
        #     )
        #     # print(aoi_order)

        #     response = asyncio.run(submit_order(pl_client, aoi_order))

        # with open(os.path.join(str(ID_PATH), str(base_path)), "w") as f:
        #     jsonStr = json.dumps(item_list)
        #     f.write(jsonStr)
        #     f.close()
