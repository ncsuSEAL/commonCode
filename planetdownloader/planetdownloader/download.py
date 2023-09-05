#! /usr/bin/env python3
################################################################################
# Author: Izzi Hinks
# Title: download.py
################################################################################

import argparse, cli, asyncio
from pathlib import Path
import multiprocessing as mp
from planet import Session

# Order states https://developers.planet.com/docs/orders/ordering/#order-states
# this is in order of state progression except for final states
ORDER_STATE_SEQUENCE = [
    "queued",
    "running",
    "failed",
    "success",
    "partial",
    "cancelled",
]


def add_arguments(parser):
    download_p = parser.add_parser("download", help="Download Planet orders")

    download_p.add_argument(
        "-s",
        "--start",
        help="Start date of image search. Format: YYYY-MM-DD",
        type=cli.valid_date,
        required=True,
    )
    download_p.add_argument(
        "-e",
        "--end",
        help="End date of image search. Format: YYYY-MM-DD",
        type=cli.valid_date,
        required=True,
    )
    download_p.add_argument(
        "-os",
        "--orderstate",
        help="Order state of interest",
        choices=ORDER_STATE_SEQUENCE,
        nargs="+",
        required=True,
    )
    download_p.add_argument(
        "-o",
        "--outdir",
        help="Output directory where ordered files will be exported",
        type=Path,
        required=True,
    )
    download_p.add_argument(
        "-p",
        "--processes",
        help="Number of threads between which to split the downloads",
        type=int,
        default=mp.cpu_count(),
        required=False,
    )
    download_p.add_argument(
        "-k",
        "--apikey",
        help="Your Planet API key, if it has not already been added in the api_key.txt file or as an environment variable  with key '$PL_API_KEY'",
        type=str,
        required=False,
    )

    return parser


# async def download_order(pl_client, order_id, OUT_DIR):
#     await pl_client.download_order(order_id, OUT_DIR, progress_bar=True)
#     print("done")


async def download_orders(order_names, orders_of_interest, OUT_DIR, PROCESSES):
    async with Session() as sess:
        cl = sess.client("orders")
        pool = mp.Pool(PROCESSES)
        # Split processes
        # order_args = [(order_id, OUT_DIR) for order_id in orders_of_interest]
        # print(order_args)
        # result = pool.starmap_async(
        #     cl.download_order, [(order_id, OUT_DIR) for order_id in orders_of_interest]
        # )
        # return result
        for order_num in range(len(order_names)):
            order_path = Path(OUT_DIR, order_names[order_num])
            order_path.mkdir(parents=True, exist_ok=True)
            await cl.download_order(orders_of_interest[order_num], order_path)


# outcome = asyncio.run(download_order(cl, orders_of_interest[0], OUT_DIR))
# await cl.download_order(orders_of_interest[0], OUT_DIR, progress_bar=True)
