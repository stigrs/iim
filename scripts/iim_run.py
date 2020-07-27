#!/usr/bin/env python
#
# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Program for running IIM."""

import iim.main as iim_main


if __name__ == "__main__":
    try:
        iim_main.main()
    except Exception as err:
        print("Error: ", err)
