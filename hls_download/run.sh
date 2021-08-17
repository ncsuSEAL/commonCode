#! /bin/sh

#
# Bash wrapper to run HLS SuPER script on HPC.
#

usage() {
    echo "Bash wrapper to run HSL SuPER script on NCSU HPC with consistent params.\n
Usage: [Annotation json] [Output directory] [-of output format default=NC4]
       [-s start date] [-e end date]";
}

if [ $# -lt 2 ]; then
  usage &&
  echo "\nSet ROI and output directory";
  exit 1
fi

# Defaults
r=$1
d=$2
f="NC4"
s="04/03/2014"
e=$(date "+%m/%d/%Y")


while getopts "s:e:h:f" o; do
    case "${o}" in
        s)
            s=${OPTARG}
            ;;
        e)
            e=${OPTARG}
            ;;
        f)
            f=${OPTARG}
            ;;
        h) usage;
           exit 1
            ;;
    esac
done

echo $r

python ./hls-super-script/HLS_SuPER.py -roi $r -dir $d -start $s -end $e -of $f
