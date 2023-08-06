#!/usr/bin/env python3
 
"""
.. module:: testCombined
   :synopsis: Tests the combination code
 
.. moduleauthor:: Ursula Laa <Ursula.Laa@assoc.oeaw.ac.at>
.. moduleauthor:: Andre Lessa <lessa.a.p@gmail.com>
 
"""
 
import sys,os,imp
sys.path.insert(0,"../")
import unittest
from unitTestHelpers import equalObjs, runMain
from smodels.tools.smodelsLogging import logger, setLogLevel
 
class CombinedTest(unittest.TestCase):
    def defineTest(self):
        """ define the current output as the default output.
        Use with care! """
        filename = "./testFiles/slha/gluino_squarks.slha"
        outputfile = runMain(filename,inifile="testParameters_agg.ini", suppressStdout=True )
        with open( outputfile, 'rb') as fp: ## imports file with dots in name
            output_module = imp.load_module("output",fp,outputfile, 
                                            ('.py', 'rb', imp.PY_SOURCE) )
        smodelsOutput = output_module.smodelsOutput
        f=open("gluino_squarks_default_agg.py","w")
        f.write ( "smodelsOutputDefault = %s\n" % smodelsOutput )
        f.close()

    def testCombinedResult(self):
        filename = "./testFiles/slha/gluino_squarks.slha"
        outputfile = runMain(filename,inifile="testParameters_agg.ini", suppressStdout=True )
        with open( outputfile, 'rb') as fp: ## imports file with dots in name
            output_module = imp.load_module("output",fp,outputfile, 
                                            ('.py', 'rb', imp.PY_SOURCE) )
            smodelsOutput = output_module.smodelsOutput
            from gluino_squarks_default_agg import smodelsOutputDefault
            ignoreFields = ['input file','smodels version', 'ncpus', 'database version']
            smodelsOutputDefault['ExptRes'] = sorted(smodelsOutputDefault['ExptRes'],
                        key=lambda res: res['r'], reverse=True)
            equals = equalObjs(smodelsOutput,smodelsOutputDefault,allowedDiff=0.02,
                               ignore=ignoreFields)
            if equals != True:
                logger.error ( "%s differs from %s!" % ( "gluino_squarks_default_agg.py", outputfile) ) 
            self.assertTrue(equals)
        for i in [ outputfile, outputfile.replace(".py",".pyc") ]:
            if os.path.exists ( i ):
                os.remove ( i )
 
if __name__ == "__main__":
    setLogLevel ( "debug" )
    unittest.main()
