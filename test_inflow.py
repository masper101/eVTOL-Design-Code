import unittest
from compute_inflow import compute_inflow
import numpy as np

class TestInflow(unittest.TestCase):

    def test_computeInflow(self):
        
        CT = .008
        lam_h = (CT/2)**0.5
        
        # test hover case (mu=0)

        #TODO: FINISH
        # lam = compute_inflow(0, lam_z, CT, (CT/2)**0.5)
        # if alpha == 0:
        #     # self.assertEqual(lam, lam_h)
        # elif alpha > 0:
        #     self.assertEqual(lam, (lam_z))



if __name__ == "__main__":

    unittest.main()