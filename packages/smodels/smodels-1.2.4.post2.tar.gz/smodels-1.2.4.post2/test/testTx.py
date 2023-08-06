#!/usr/bin/env python3

"""
.. module:: testTx
   :synopsis: Tests with Tx slha input files.
    
.. moduleauthor:: Wolfgang Waltenberger <wolfgang.waltenberger@gmail.com>
    
"""
import sys
sys.path.insert(0,"../")
from smodels.theory import slhaDecomposer
from smodels.tools.physicsUnits import GeV, fb
import unittest

class TxTest(unittest.TestCase):
    

    def testT1(self):
        from smodels.tools.smodelsLogging import logger
        logger.info("T1")
        """ test with the T1 slha input file """
        slhafile="./testFiles/slha/simplyGluino.slha"
        topos = slhaDecomposer.decompose ( slhafile, .1*fb, False, False, 5.*GeV )
        for topo in topos:
            for element in topo.elementList:
                masses=element.getMasses()
                # print "e=",element,"masses=",masses
                mgluino=masses[0][0]
                mLSP=masses[0][1]
                self.assertEqual( str(element), "[[[q,q]],[[q,q]]]" )
                self.assertEqual( int ( mgluino / GeV ), 675 )
                self.assertEqual( int ( mLSP / GeV ), 200 )

if __name__ == "__main__":
    unittest.main()
