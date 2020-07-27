# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Module providing I/O methods for IIM."""

import numpy as np
import matplotlib.pyplot as plt


def print_header(mode):
    """Print header for IIM output file."""
    print(90 * "=")
    print("%s %s" %
          (mode, 
          "Inoperability Input-Output Model for Interdependent "
          "Infrastructure Sectors"))
    print(90 * "=")


def print_perturbed_sectors(psector, cvalue):
    """Print list of perturbed sectors."""
    for ps, cs in zip(psector, cvalue):
        print("Perturbed sector: %s (%.2f)" % (ps, cs))


def print_results(psector, iim_model, txt):
    """Helper function for printing results from IIM runs."""
    print("%s: " % txt)
    for i in range(len(psector)):
        print("q(%s) = %.3f" % (psector[i], iim_model.get(psector[i])[0]))
    print("q_tot = %.3f" % iim_model.inoperability().sum())


def plot(xdata, ydata, xlabel=None, ylabel=None, title=None):
    """Helper function for creating IIM plots."""
    _, ax = plt.subplots(figsize=(15,5))
    ax.bar(xdata, ydata)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    plt.xticks(rotation=90)


def plot_group(xtick_labels, y1, y2, 
               xlabel=None, ylabel=None, legend=None, title=None):
    """Helper function for creating grouped IIM plots."""
    _, ax = plt.subplots(figsize=(15,5))
    ax.yaxis.grid(color='gray', linestyle='dashed')

    ind = np.arange(len(xtick_labels))
    width = 0.4

    p1 = ax.bar(ind, y1, width)
    p2 = ax.bar(ind + width, y2, width)

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(xtick_labels)
    plt.xticks(rotation=90)

    ax.legend((p1[0], p2[0]), legend)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
