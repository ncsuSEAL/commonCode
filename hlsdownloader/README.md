HLS downloader for v1.4

Uses standard python3 libraries with support for parallelized downloads.

run `hlsdownloader -h` to see help

Example:

```bash
hlsdownloader -t "17SPC" "17RKLM" "17PAB" -o ~/tmp/HLSpy -y 2015 2016 -p 8
```

HPC usage:

- Run on login node as compute nodes do not have internet connection
- ~17 minutes to download 1776 files (888 x2 hdf & hdr) with 2 cores used.
