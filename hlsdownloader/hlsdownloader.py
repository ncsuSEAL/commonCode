#! /usr/bin/env python3
##############################################################################
# Author: Owen Smith
# Title: hlsdownloader.py
##############################################################################

import argparse
from typing import Union
from pathlib import Path
from urllib.request import urlopen, urlretrieve
import re
import multiprocessing as mp
import time

URL = "https://hls.gsfc.nasa.gov/data/v1.4"
SENSORS = ["S30", "L30"]

regex = re.compile(r'\"HLS(.*?)\.hdf"')


class Colors:
    cyan = "\033[96m"
    ok = "\033[92m"
    warning = "\033[93m"
    error = "\033[91m"
    end = "\033[0m"


def parser() -> argparse.Namespace:
    pargs = argparse.ArgumentParser(
        description="CLI tool for downloading v1.4 Harmonized Landsat Sentinel products. "
        "Offers multiprocessing support"
    )
    pargs.add_argument(
        "-o",
        "--outdir",
        help="Output directory where all tiles will be downloaded into",
    )
    pargs.add_argument("-t", "--tiles", nargs="+", help="HLS tile names.")
    pargs.add_argument(
        "-y",
        "--years",
        nargs="+",
        default=[2015, 2016, 2017, 2018, 2019],
        help="Years to download",
    )
    pargs.add_argument(
        "-l", "--log", default="./failed.txt", help="File listing failed downloads"
    )
    pargs.add_argument(
        "--threads",
        default=mp.cpu_count() // 2,
        help="Number of threads to split download between",
    )
    return pargs.parse_args()


def construct_dir_urls(sensors: list, tiles: list, years: list) -> list:
    tile_urls = []
    for sensor in sensors:
        for tile in tiles:
            for year in years:
                tile_urls.append(
                    f"{URL}/{sensor}/{year}/{tile[0:2]}/{tile[2]}/{tile[3]}/{tile[4]}"
                )
    return tile_urls


def construct_file_urls(dir_urls: list) -> list:
    file_paths = []
    for url in dir_urls:
        req = urlopen(url)
        encoding = req.headers.get_content_charset()
        req_str = req.read().decode(encoding)

        file_list = regex.findall(req_str)

        file_paths.extend([f"{url}/HLS{i}.hdf" for i in file_list])
        file_paths.extend([f"{url}/HLS{i}.hdf.hdr" for i in file_list])

    return file_paths


def downloader(path: str, outdir: Union[str, Path], logfile: str) -> None:
    file_name = path.split("/")[-1]
    outpath = outdir / file_name[4:7] / file_name
    print(outpath)
    if outpath.exists():
        print(f"{Colors.warning}Skiping {file_name}. Already exists. {Colors.end}")
        return
    print(f"{Colors.cyan}Downloading: {Colors.end}{file_name}")
    try:
        start = time.time()
        urlretrieve(path, str(outpath))
        print(f"{Colors.ok}Complete: {Colors.end}{time.time() - start:.2f}s", file_name)
    except:
        print(f"{Colors.error}Failed to download: {Colors.end}{file_name}")
        with open(logfile, "a") as f:
            print(f"{path}\n", file=f)


def main():

    start = time.time()
    args = parser()

    outdir = Path(args.outdir)
    tiles = args.tiles
    years = args.years
    logfile = args.log

    outdir.mkdir(parents=True, exist_ok=True)

    sent_dir = outdir / "S30"
    sent_dir.mkdir(parents=True, exist_ok=True)

    land_dir = outdir / "L30"
    land_dir.mkdir(parents=True, exist_ok=True)

    dir_urls = construct_dir_urls(SENSORS, tiles, years)
    file_urls = construct_file_urls(dir_urls)

    pool = mp.Pool(mp.cpu_count())
    print(f"Total files found: {len(file_urls)}")
    print(f"Using {mp.cpu_count()} threads")
    pool.starmap(
        downloader, [(file_urls[i], outdir, logfile) for i in range(len(file_urls))]
    )
    print("Total time: ", time.time() - start)


if __name__ == "__main__":
    main()
