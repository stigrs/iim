# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import os
import iim.iim as iim
import numpy as np
import unittest


class TestIIM(unittest.TestCase):
    def test_case1(self):
        # Correct answer (Haimes & Jiang, 2001):
        # --------------------------------------
        # For c = [0.0, 0.6], q = [0.571, 0.714]
        qans = [0.571, 0.714]

        fname = os.path.join("tests", "test_case1.csv")
        psector = ["Sector2"]
        cvalue = [0.6]
        table = "A"
        mode = "Demand"

        model = iim.IIM(fname, psector, cvalue, table, mode)
        q = model.inoperability()

        self.assertTrue(np.allclose(q, qans, atol=0.001))

    def test_case2(self):
        # Correct answer (Haimes & Jiang, 2001):
        # --------------------------------------
        # For c = [0.0, 0.5, 0.0, 0.0], q = [0.70, 0.78, 1, 1]
        qans = [0.70, 0.78, 1.0, 1.0]
    
        fname = os.path.join("tests", "test_case2.csv")
        psector = ["Sector2"]
        cvalue = [0.5]
        table = "A"
        mode = "Demand"

        model = iim.IIM(fname, psector, cvalue, table, mode)
        q = model.inoperability()

        self.assertTrue(np.allclose(q, qans, atol=0.01))

    def test_case3(self):
        # Correct answer:
        # ---------------
        # For c = [0.0, 0.0, 0.12], q = [0.04, 0.02, 0.14]
        qans = [0.04, 0.02, 0.14]
    
        fname = os.path.join("tests", "test_case3.csv")
        psector = ["SectorC"]
        cvalue = [0.12]
        table = "A"
        mode = "Demand"

        model = iim.IIM(fname, psector, cvalue, table, mode)
        q = model.inoperability()

        self.assertTrue(np.allclose(q, qans, atol=0.01))

    def test_case4(self):
        # Correct answer:
        # ---------------
        # Xu et al. (2011), eq. 31.
        a_ans = [[0.14, 0.17, 0.26, 0.14],
                 [0.11, 0.20, 0.32, 0.28],
                 [0.20, 0.10, 0.26, 0.14],
                 [0.14, 0.17, 0.10, 0.28]]

        fname = os.path.join("tests", "test_case4.csv")
        psector = ["Electric"]
        cvalue = [0.0]
        table = "IO"
        mode = "Supply"

        model = iim.IIM(fname, psector, cvalue, table, mode)
        amat = model.get_tech_coeff()

        self.assertTrue(np.allclose(a_ans, amat, atol=0.015))

    def test_case5(self):
        # Correct answer:
        # ---------------
        # Xu et al. (2011), eq. 34.
        a_ans = [[0.14, 0.11, 0.20, 0.14],
                 [0.17, 0.20, 0.10, 0.17],
                 [0.26, 0.32, 0.26, 0.10],
                 [0.14, 0.28, 0.14, 0.28]]

        fname = os.path.join("tests", "test_case4.csv")
        psector = ["Electric"]
        cvalue = [0.0]
        table = "IO"
        mode = "Supply"

        model = iim.IIM(fname, psector, cvalue, table, mode)
        amat = model.get_interdependency_matrix()

        self.assertTrue(np.allclose(a_ans, amat, atol=0.015))


if __name__ == "__main__":
    unittest.main()
