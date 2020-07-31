# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import setuptools


setuptools.setup(
    name="iim", 
    version="0.1",
    author="Stig Rune Sellevag",
    author_email="stig-rune.sellevag@ffi.no",
    license="MIT License",
    description="Inoperability Input-Output Model",
    url="git@github.com:stigrs/iim.git",
    packages=setuptools.find_packages(),
    install_requires= [
        "numpy",
        "matplotlib",
        "pandas"
    ],
    scripts=["scripts/iim_run.py", "scripts/iim_collect.py", 
             "scripts/iim_nth_order_dep.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
