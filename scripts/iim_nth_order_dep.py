#!/usr/bin/env python
#
# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Program for analysing n-th order interdependencies from IIM 
interdependency matrix."""

import argparse
import csv
import numpy as np
import iim.iim as iim
from pathlib import Path


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyse n-th order IIM interdependencies")
    parser.add_argument("-f", "--file",
                        action="store",
                        dest="filename",
                        required=True,
                        help="input filename")
    parser.add_argument("-n", "--order",
                        action="store",
                        dest="order",
                        type=int,
                        required=False,
                        default=1,
                        help="n-th order interdependency")
    parser.add_argument("-t", "--table",
                        action="store",
                        dest="table",
                        choices=["IO", "A"],
                        default="IO",
                        required=False,
                        help="type of input-output table")
    parser.add_argument("-m", "--mode",
                        action="store",
                        dest="mode",
                        choices=["Demand", "Supply"],
                        default="Demand",
                        required=False,
                        help="calculation mode")
    return parser.parse_args()


def write_aij(inputfile, aij, order):
    """Write max n-th order interdependencies to CSV file."""
    filename = Path(inputfile).stem + "_" + str(order) + "-order_dep.csv"
    with open(filename, "w", newline="") as fout:
        writer = csv.writer(fout, dialect="excel")
        aij_str = "max(aj^" + str(order) + ")"
        tmp = ["i", "j", aij_str]
        writer.writerow(tmp)
        writer.writerows(aij)


def main():
    args = parse_arguments()
    psector = []
    cvalue = []
    model = iim.IIM(args.filename, psector, cvalue, args.table, args.mode)
    aij = model.max_nth_order_interdependency(args.order)
    write_aij(args.filename, aij, args.order)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print("Error: ", err)
