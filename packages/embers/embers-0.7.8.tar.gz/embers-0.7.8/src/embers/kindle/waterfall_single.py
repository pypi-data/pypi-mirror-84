"""
Waterfall Single
----------------

Saves a single waterfall plot to ``./embers_out/rf_tools``

"""

import argparse
from pathlib import Path

from embers.rf_tools.rf_data import single_waterfall

_parser = argparse.ArgumentParser(
    description="""
    Saved a single waterfall plot
    """
)

_parser.add_argument(
    "--rf_file",
    metavar="\b",
    default="tiles_data/S06XX/2019-10-10/S06XX_2019-10-10-02:30.txt",
    help="Path to raw rf data file. Default=tiles_data/S06XX/2019-10-10/S06XX_2019-10-10-02:30.txt",
)
_parser.add_argument(
    "--out_dir",
    metavar="\b",
    default="embers_out/rf_tools",
    help="Dir where colormap sample plot is saved. Default=./embers_out/rf_tools",
)

_args = _parser.parse_args()
_rf_file = _args.rf_file
_out_dir = _args.out_dir


def main():
    """Executable: save singel waterfall plot"""

    print(f"Waterfall plot saved to ./{_out_dir}/{Path(_rf_file).stem}.png")
    single_waterfall(_rf_file, _out_dir)
