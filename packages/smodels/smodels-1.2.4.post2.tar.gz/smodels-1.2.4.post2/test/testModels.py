#!/usr/bin/env python3
 
"""
.. module:: testRunSModelS
   :synopsis: Tests runSModelS
 
.. moduleauthor:: Ursula Laa <Ursula.Laa@assoc.oeaw.ac.at>
.. moduleauthor:: Andre Lessa <lessa.a.p@gmail.com>
 
"""
 
import sys,os,imp
sys.path.insert(0,"../")
import unittest
from os.path import join 
from smodels.installation import installDirectory as iDir
from unitTestHelpers import equalObjs, runMain
from smodels.tools.smodelsLogging import setLogLevel
from smodels.tools import runtime
from smodels import particlesLoader
from imp import reload

# setLogLevel('debug')
 
 
class ModelsTest(unittest.TestCase):
  
    def testRuntimeImport(self):
        filename = "./testFiles/slha/idm_example.slha"
        runtime.modelFile = 'idm'
        reload(particlesLoader)
        outputfile = runMain(filename,inifile='testParameters_noModel.ini',suppressStdout=True)
        with open( outputfile, 'rb') as fp: ## imports file with dots in name
            output_module = imp.load_module("output",fp,outputfile, ('.py', 'rb', imp.PY_SOURCE) )
            smodelsOutput = output_module.smodelsOutput
        from idm_example_default import smodelsOutputDefault
        ignoreFields = ['input file','smodels version', 'ncpus', 'database version']
        smodelsOutputDefault['ExptRes'] = sorted(smodelsOutputDefault['ExptRes'],
                    key=lambda res: res['r'], reverse=True)
        equals = equalObjs(smodelsOutput,smodelsOutputDefault,allowedDiff=0.02,
                           ignore=ignoreFields)
        self.assertTrue(equals)
        self.removeOutputs(outputfile)
         
    def testParameterFile(self):
        filename = "./testFiles/slha/idm_example.slha"
        outputfile = runMain(filename,inifile='testParameters_idm.ini',suppressStdout=True)        
        with open( outputfile, 'rb') as fp: ## imports file with dots in name
            output_module = imp.load_module("output",fp,outputfile, ('.py', 'rb', imp.PY_SOURCE) )
            smodelsOutput = output_module.smodelsOutput
        from idm_example_default import smodelsOutputDefault
        ignoreFields = ['input file','smodels version', 'ncpus', 'database version']
        smodelsOutputDefault['ExptRes'] = sorted(smodelsOutputDefault['ExptRes'],
                    key=lambda res: res['r'], reverse=True)
        equals = equalObjs(smodelsOutput,smodelsOutputDefault,allowedDiff=0.02,
                           ignore=ignoreFields)
        self.assertTrue(equals)
        self.removeOutputs(outputfile)
        
    def testWrongModel(self):
        runtime.modelFile = 'mssm'
        reload(particlesLoader)
        filename = "./testFiles/slha/idm_example.slha"
        outputfile = runMain(filename,suppressStdout=True)
        with open( outputfile, 'rb') as fp: ## imports file with dots in name
            output_module = imp.load_module("output",fp,outputfile, ('.py', 'rb', imp.PY_SOURCE) )
            smodelsOutput = output_module.smodelsOutput
        self.assertTrue(smodelsOutput['OutputStatus']['decomposition status'] < 0)  
        self.removeOutputs(outputfile)


    def removeOutputs(self, f):
        """ remove cruft outputfiles """
        for i in [ f, f.replace(".py",".pyc") ]:
            if os.path.exists ( i ): os.remove ( i )
  
      

if __name__ == "__main__":
    unittest.main()
