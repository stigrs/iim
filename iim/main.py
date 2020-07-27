# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""This is main for IIM."""

import argparse
import iim.io as iim_io
import iim.iim as iim


def _restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "%r not a floating-point literal" % (x,))

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]" % (x,))
    return x


def _check_input(psector, cvalue):
    if len(psector) != len(cvalue):
        raise RuntimeError("psector and cvalue have different sizes")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Demand-Driven Inoperability Input-Output Model")
    parser.add_argument("-f", "--file",
                        action="store",
                        dest="filename",
                        required=True,
                        help="name of CSV file")
    parser.add_argument("-s", "--sector",
                        action="append",
                        dest="psector",
                        required=True,
                        help="name of perturbed sector")
    parser.add_argument("-c", "--cvalue",
                        action="append",
                        dest="cvalue",
                        required=True,
                        type=_restricted_float,
                        help="fraction of perturbation [0-1]")
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
    args = parser.parse_args()
    _check_input(args.psector, args.cvalue)
    return args


def main():
    """Driver for IIM solver."""
    args = parse_arguments()
    if args.mode == "Supply":
        iim_io.print_header("Supply-Driven")
    else:
        iim_io.print_header("Demand-Driven")

    model = iim.IIM(
        args.filename, args.psector, args.cvalue, args.table, args.mode)

    sectors = model.get_sectors()
    delta = model.dependency()
    rho = model.influence()
    delta_overall = model.overall_dependency()
    rho_overall = model.overall_influence()
    qstar = model.inoperability()

    iim_io.print_perturbed_sectors(args.psector, args.cvalue)
    print("\nSector\t\tInoperability\tDependency\tD(overall)\t"
          "Influence\tI(overall)")
    print(90 * "-")

    for i in range(0, len(sectors)):
        print("%-8s\t%8.6f\t%8.6f\t%8.6f\t%8.6f\t%8.6f"
              % (sectors[i].strip(), qstar[i], delta[i], delta_overall[i],
                 rho[i], rho_overall[i]))


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print("Error: ", err)
