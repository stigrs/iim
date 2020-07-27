# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Provides the Static Demand-Driven and Supply-Driven Inoperability 
Input-Output Models (IIM) for Interdependent Infrastructure Sectors as 
described in the papers:

 - Haimes, Y. Y & Jiang, P. (2001). Leontief-based model of risk in complex
   interconnected infrastructures. Journal of Infrastructure Systems, 7, 1-12.

 - Haimes, Y. Y., Horowitz, B. M., Lambert, J. H., Santos, J. R., Lian, C. &
   Crowther, K. G. (2005). Inoperability input-output model for interdependent
   infrastructure sectors. I: Theory and methodology. Journal of Infrastructure
   Systems, 11, 67-79.

 - Leung, M., Haimes, Y. Y. & Santos, J. R. (2007). Supply- and output-side 
   extensions to the inoperability input-output model for interdependent 
   infrastructures. Journal of Infrastructure Systems, 13, 299-310.

 - Santos, J. R. & Haimes, Y. Y. (2004). Modeling the demand reduction
   input-output (I-O) inoperability due to terrorism of interconnected
   infrastructures. Risk Analysis, 24, 1437-1451.

 - Setola, R., De Porcellinis, S. & Sforna, M. (2009). Critical infrastructure
   dependency assessment using the input-output inoperability model.
   International Journal of Critical Infrastructure Protection, 2, 170-178.
"""
import numpy as np
import pandas as pd


class IIM:
    """Class providing the Inoperability Input-Output Model."""
    def __init__(
            self, filename, psector_, cvalue_, table_="IO", mode_="Demand"):
        self.sectors = []      # list of sectors
        self.io_table = []     # industry*industry input-output table
        self.xoutput = []      # as-planned production per sector
        self.amat = []         # Leontief technical coefficients
        self.astar = []        # interdependency matrix
        self.smat = []         # S matrix
        self.cstar = []        # degradation in demand/supply
        self.psector = []      # list of perturbed sectors
        self.cvalue = []       # list of perturbations
        self.table = table_    # type of input table
        self.mode = mode_      # type of calculation mode

        self._read_io_table(filename)
        self._create_perturbation(psector_, cvalue_)
        self._tech_coeff_matrix()
        self._interdepenency_matrix()

    def __len__(self):
        """Return number of sectors."""
        return len(self.sectors)

    def _read_io_table(self, filename):
        # Read I/O table or A* matrix from CSV file.
        #
        # Note:
        #  If I/O table is provided, last row must provide total output.
        #
        df = pd.read_csv(filename)
        self.io_table = np.array(df.values, dtype=float)  # df.to_numpy()
        self.sectors = df.columns.str.strip()
        if self.table == "IO":
            self.xoutput = self.io_table[-1, :]
            self.io_table = self.io_table[:-1, :]

    def _create_perturbation(self, psector_, cvalue_):
        n = len(self.sectors)
        self.cstar = np.zeros(n)
        if psector_:
            for ps, cs in zip(psector_, cvalue_):
                indx = self.sectors.get_loc(ps)
                self.cstar[indx] = cs
        self.psector = psector_
        self.cvalue = cvalue_

    def _tech_coeff_matrix(self):
        # Calculate Leontief technical coefficients matrix (A) from I-O table.
        #
        # Algorithm:
        #   Santos & Haimes (2004), eq. 2.
        #
        n = len(self.sectors)
        self.amat = np.zeros(shape=(n, n))
        if self.table == "IO":  # industry*industry input-output table provided
            for i in range(n):
                for j in range(n):
                    if self.xoutput[j] != 0.0:
                        self.amat[i, j] = self.io_table[i, j] / self.xoutput[j]
                    else:
                        self.amat[i, j] = 0.0
    
    def _interdepenency_matrix(self):
        # Calculate demand-driven or supply-driven interdependency matrix 
        # and the S matrix from technical coefficients.
        #
        # Algorithm:
        #  Santos & Haimes (2004), eq. 28. (A* matrix)
        #  Leung et al. (2007), p. 301 (A^S matrix)
        #  Setola et al. (2009), eq. 7. (S matrix)
        #
        n = len(self.sectors)
        self.astar = np.zeros(shape=(n, n))
        if self.mode == "Supply":   
            if self.table == "IO":
                self.astar = np.transpose(self.amat)  # Leung (2007), p. 301
            else:  # interdependency matrix is provided as input
                self.astar = self.io_table 
            self.smat = np.linalg.inv(np.identity(n) - self.astar)
        else:  # demand-driven 
            if self.table == "IO":
                # The algorithm:
                #   pmat = np.identity(n) * self.xoutput
                #   pinv = np.linalg.inv(pmat)
                #   self.astar = np.matmul(self.amat, pmat)
                #   self.astar = np.matmul(pinv, self.astar)
                # may create singular matrix if x_i == 0. 
                for i in range(n):
                    for j in range(n):
                        if self.xoutput[i] != 0.0:
                            self.astar[i, j] = \
                                self.io_table[i, j] / self.xoutput[i]
            else:  # interdependency matrix provided
                self.astar = self.io_table
            self.smat = np.linalg.inv(np.identity(n) - self.astar)

    def get(self, isector):
        """Return data for the i'th sector."""
        indx = self.sectors.get_loc(isector)
        di = self.dependency()[indx]
        odi = self.overall_dependency()[indx]
        rj = self.influence()[indx]
        orj = self.overall_influence()[indx]
        qi = self.inoperability()[indx]
        return [qi, di, odi, rj, orj]

    def get_sectors(self):
        """Return list of sectors."""
        return self.sectors
    
    def get_tech_coeff(self):
        """Return Leontief technical coefficients."""
        return self.amat

    def get_interdependency_matrix(self):
        """Return interdependency matrix."""
        return self.astar

    def get_xoutput(self):
        """Return as-planned production per sector."""
        return self.xoutput

    def dependency(self):
        """Calculate dependency index."""
        #
        # Algorithm:
        #   Setola et al. (2009), eq. 3.
        #
        # Note:
        #   Only defined for demand-driven IIM.
        #
        n = len(self.sectors)
        delta = np.zeros(n)
        if self.mode == "Demand":  
            for i in range(n):
                di = 0.0
                for j in range(n):
                    if j != i:
                        di += self.astar[i, j]
                delta[i] = di
        return delta / (n - 1.0)

    def influence(self):
        """Calculate influence gain."""
        #
        # Algorithm:
        #   Setola et al. (2009), eq. 4.
        #
        # Note:
        #   Only defined for demand-driven IIM.
        #
        n = len(self.sectors)
        rho = np.zeros(n)
        if self.mode == "Demand":  
            for j in range(n):
                rj = 0.0
                for i in range(n):
                    if i != j:
                        rj += self.astar[i, j]
                rho[j] = rj
        return rho / (n - 1.0)

    def overall_dependency(self):
        """Calculate overall dependency index."""
        #
        # Algorithm:
        #   Setola et al. (2009), eq. 9.
        # 
        # Note:
        #   Only defined for demand-driven IIM.
        #
        n = len(self.sectors)
        delta = np.zeros(n)
        if self.mode == "Demand": 
            for i in range(n):
                di = 0.0
                for j in range(n):
                    if j != i:
                        di += self.smat[i, j]
                delta[i] = di
        return delta / (n - 1.0)

    def overall_influence(self):
        """Calculate influence gain."""
        #
        # Algorithm:
        #   Setola et al. (2009), eq. 10.
        # 
        # Note:
        #   Only defined for demand-driven IIM.
        #
        n = len(self.sectors)
        rho = np.zeros(n)
        if self.mode == "Demand":  
            for j in range(n):
                rj = 0.0
                for i in range(n):
                    if i != j:
                        rj += self.smat[i, j]
                rho[j] = rj
        return rho / (n - 1.0)

    def interdependency_index(self, isector, jsector, order=1):
        """Return n-th order interdependency index between two sectors."""
        i = self.sectors.get_loc(isector)
        j = self.sectors.get_loc(jsector)
        amat = np.linalg.matrix_power(self.astar, order)
        return amat[i, j]

    def max_nth_order_interdependency(self, n):
        """Return maximum nth-order interdependency index for each sector."""
        assert n >= 1
        amat = np.linalg.matrix_power(self.astar, n)
        res = []
        for i in range(len(self.sectors)):
            j = np.argmax(amat[i, :], axis=0)
            tmp = [self.sectors[i], self.sectors[j], amat[i, j]]
            res.append(tmp)
        return res

    def inoperability(self):
        """Calculate overall risk of inoperability of the infrastructures."""
        #
        # Algorithm:
        #   Haimes & Jiang (2001), eq. 14.
        #   Haimes et al. (2005), eq. 38.
        #
        q = np.matmul(self.smat, self.cstar)
        q[q > 1.0] = 1.0  # upper limit
        return q
