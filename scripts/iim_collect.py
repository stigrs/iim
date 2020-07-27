#!/usr/bin/env python
#
# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Program for collecting output from IIM runs.

Structure of input file:

PerturbedSector1 PerturbedSector 2 PerturbedSectorN
FilenameRun1
FilenameRun2
FilenameRunN
"""

import argparse
import csv
import re
import numpy as np
from pathlib import Path


class IIMCollect:
    """Class for collecting output from IIM runs. Output are written as
    comma separated values (CSV).
    """
    def __init__(self):
        self.sectors = []        # list of sectors
        self.inoperability = []  # inoperability for each sector
        self.delta = []          # dependency index
        self.delta_overall = []  # overall dependency index
        self.rho = []            # influence gain
        self.rho_overall = []    # overall influence gain
        self.runs = []           # list of IIM runs

    def _read_data_file(self, filename):
        # Read output file from IIM.
        self.sectors = []
        self.delta = []
        self.rho = []
        qstar = []
        with open(filename) as fin:
            for dummy in range(0, 3):  # ignore header
                line = fin.readline()
            line = fin.readline()
            for dummy in range(0, 3):  # ignore
                line = fin.readline()
            for line in fin:
                pattern = r"(\w+)(\s+)(\d+\.\d*)(\s+)(\d+\.\d*)(\s+)(\d+\.\d*)(\s+)(\d+\.\d*)(\s+)(\d+\.\d*)"
                match = re.search(pattern, line)
                self.sectors.append(match.group(1))
                qstar.append(float(match.group(3)))
                self.delta.append(float(match.group(5)))
                self.delta_overall.append(float(match.group(7)))
                self.rho.append(float(match.group(9)))
                self.rho_overall.append(float(match.group(11)))
        self.inoperability.append(qstar)

    def _print_data(self, inputfile):
        # Print collected IIM data.
        filename = Path(inputfile).stem + ".csv"
        with open(filename, "w", newline="") as fout:
            writer = csv.writer(fout, dialect="excel")
            tmp = ["Sector", "delta", "delta_overall", "rho", "rho_overall"]
            for i in range(len(self.runs)):
                tmp.append(self.runs[i])
            writer.writerow(tmp)
            for i in range(len(self.sectors)):
                tmp = []
                tmp.append(self.sectors[i])
                tmp.append(self.delta[i])
                tmp.append(self.delta_overall[i])
                tmp.append(self.rho[i])
                tmp.append(self.rho_overall[i])
                for j in range(len(self.runs)):
                    tmp.append(self.inoperability[j, i])
                writer.writerow(tmp)

    def collect(self, filename):
        """Collect data from each IIM output file."""
        with open(filename) as fin:
            line = fin.readline()
            for run in line.split():
                self.runs.append(run)
            for f in fin:
                if f and (not f.isspace()):
                    self._read_data_file(f.rstrip())
        self.inoperability = np.array(self.inoperability)
        self._print_data(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post-process output from IIM")
    parser.add_argument("-f", "--file",
                        action="store",
                        dest="filename",
                        required=True,
                        help="name of IIM output file")
    args = parser.parse_args()

    try:
        model = IIMCollect()
        model.collect(args.filename)
    except Exception as err:
        print("Error: ", err)
