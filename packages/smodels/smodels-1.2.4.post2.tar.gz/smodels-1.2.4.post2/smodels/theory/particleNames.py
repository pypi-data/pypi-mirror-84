#!/usr/bin/env python3

"""
.. module:: particleNames
   :synopsis: Provides functions for getting particle names from pdg ids, and
              other helpers.

.. moduleauthor:: Andre Lessa <lessa.a.p@gmail.com>

"""

from smodels.theory.exceptions import SModelSTheoryError as SModelSError
import itertools

from smodels.tools.smodelsLogging import logger

ptcDic = {"e"  : ["e+",  "e-"],                                                                                                               
          "mu" : ["mu+", "mu-"],                                                                                                              
          "ta" : ["ta+", "ta-"],                                                                                                              
          "l+" : ["e+",  "mu+"],                                                                                                              
          "l-" : ["e-",  "mu-"],                                                                                                              
          "l"  : ["e-",  "mu-", "e+", "mu+"],                                                                                                 
          "W"  : ["W+",  "W-"],                                                                                                               
          "t"  : ["t+",  "t-"],                                                                                                               
          "L+" : ["e+",  "mu+", "ta+"],                                                                                                       
          "L-" : ["e-",  "mu-", "ta-"],                                                                                                       
          "L"  : ["e+",  "mu+", "ta+", "e-", "mu-", "ta-"],                                                                                   
          "jet" : ["q", "g", "c", "pi"],                                                                                                      
          "all" : ["e+",  "mu+", "ta+", "e-", "mu-", "ta-", "W+", "W-","Z",                                                                   
                   "photon","higgs","t+","t-","b","c","q","g","c","pi"]}


#Final states. Define final state labels
#according to the qNumbers tuples.

finalStates = {
"HSCP" : [[1,3,1],[1,-3,1],[0,3,1],[0,-3,1],[2,3,1],[2,-3,1]],
"MET" : [[1,0,1],[0,0,1],[2,0,1]],
"RHadronG" : [[1,0,8]],  #Gluino-like RHadron
"RHadronQ" : [[0,2,3],[0,-1,3],[0,-2,3],[0,1,3]],  #Squark-like RHadron
"Displaced" : [None]
}


def getName(pdg):
    """
    Convert pdg number to particle name according to the dictionaries rOdd and
    rEven.

    :type pdg: int
    :returns: particle name (e.g. gluino, mu-, ...)
    
    """
    
    from smodels.particlesLoader import rEven, rOdd, qNumbers

    p = int(pdg)
    if p in rOdd:
        return rOdd[p]
    if p in rEven:
        return rEven[p]
    else:
        return False


def getPdg(name):
    """
    Convert a name to the pdg number according to the dictionaries rOdd and
    rEven.

    :type name: string
    :returns: particle pdg; None, if name could not be resolved
    
    """
    
    from smodels.particlesLoader import rEven, rOdd
    
    for (pdg, pname) in rOdd.items():
        if name == pname:
            return abs(pdg)
    for (pdg, pname) in rEven.items():
        if name == pname:
            return abs(pdg)
    return None


def elementsInStr(instring,removeQuotes=True):
    """
    Parse instring and return a list of elements appearing in instring.
    instring can also be a list of strings.
    
    :param instring: string containing elements (e.g. "[[['e+']],[['e-']]]+[[['mu+']],[['mu-']]]")
    :param removeQuotes: If True, it will remove the quotes from the particle labels.
                         Set to False, if one wants to run eval on the output.
    
    :returns: list of elements appearing in instring in string format
    
    """
    
    from smodels.particlesLoader import rEven
    
    outstr = ""
    if isinstance(instring,str):
        outstr = instring
    elif isinstance(instring,list):
        for st in instring:
            if not isinstance(st,str):
                logger.error("Input must be a string or a list of strings")
                raise SModelSError()
            # Combine list of strings in a single string
            outstr += st
    else:
        raise SModelSError ( "syntax error in constraint/condition: ``%s''." \
              "Check your constraints and conditions in your database." % str(instring) )

    elements = []
    outstr = outstr.replace(" ", "")
    if removeQuotes:
        outstr = outstr.replace("'", "")
    elStr = ""
    nc = 0
    # Parse the string and looks for matching ['s and ]'s, when the matching is
    # complete, store element
    for c in outstr:
        delta = 0
        if c == '[':
            delta = -1
        elif c == ']':
            delta = 1
        nc += delta
        if nc != 0:
            elStr += c
        if nc == 0 and delta != 0:
            elements.append(elStr + c)
            elStr = ""
            # Syntax checks
            ptclist = elements[-1].replace(']', ',').replace('[', ',').\
                    split(',')
            for ptc in ptclist:
                ptc = ptc.replace("'","")
                if not ptc:
                    continue
                if ptc == '*':
                    ptc = InclusiveStr()
                if not ptc in rEven.values() and not ptc in ptcDic:
                    raise SModelSError("Unknown particle. Add " + ptc + " to your particles.py")

    # Check if there are not unmatched ['s and/or ]'s in the string
    if nc != 0:
        raise SModelSError("Wrong input (incomplete elements?) " + instring)

    return elements


def vertInStr(instring):
    """
    Parses instring (or a list of strings) and returns the list of particle
    vertices appearing in instring.
    
    :param instring: string containing elements (e.g. "[[['e+']],[['e-']]]+[[['mu+']],[['mu-']]]")
    
    :returns: list of elements appearing in instring in string format
    
    """
    
    from smodels.particlesLoader import rEven
    
    if type(instring) == type('st'):
        outstr = instring
    elif type(instring) == type([]):
        outstr = ""
        for st in instring:
            if type(st) != type('st'):
                logger.error("Input must be a string or a list of strings")
                raise SModelSError()
            # Combine list of strings in a single string
            outstr += st

    vertices = []
    outstr = outstr.replace(" ", "").replace("'", "")
    vertStr = ""
    nc = 0
    # Parse the string and looks for matching ['s and ]'s, when the matching is
    # complete, store element
    for c in outstr:
        delta = 0
        if c == '[':
            delta = -1
        elif c == ']':
            delta = 1
        nc += delta
        if c == '[':
            vertStr = ""
        if nc != 0 and c != '[' and c != ']':
            vertStr += c
        if delta > 0 and vertStr:
            vertices.append(vertStr.split(','))
            # Syntax checks:
            for ptc in vertices[-1]:
                if not ptc:
                    continue
                if ptc == '*':
                    ptc = InclusiveStr()                
                if not ptc in rEven.values() and not ptc in ptcDic:
                    logger.error("Unknown particle. Add " + ptc + " to smodels/particle.py")
                    raise SModelSError()
            vertStr = ""

    # Check if there are not unmatched ['s and/or ]'s in the string
    if nc != 0:
        logger.error("Wrong input (incomplete elements?) " + instring)
        raise SModelSError()

    return vertices

def simParticles(plist1, plist2, useDict=True):
    """
    Compares two lists of particle names. Allows for dictionary
    labels (Ex: L = l, l+ = l, l = l-,...). Ignores particle ordering inside
    the list
 
    :param plist1: first list of particle names, e.g. ['l','jet']
    :param plist2: second list of particle names 
    :param useDict: use the translation dictionary, i.e. allow e to stand for
                    e+ or e-, l+ to stand for e+ or mu+, etc 
    :returns: True/False if the particles list match (ignoring order)    
    """
    
    from smodels.particlesLoader import rEven

    if not isinstance(plist1,list) or type(plist1) != type(plist2):
        logger.error("Input must be a list")
        raise SModelSError()
    if len(plist1) != len(plist2):
        return False
    for i,p in enumerate(plist1):
        if plist1[i] == '*':
            plist1[i] = InclusiveStr()
        if plist2[i] == '*':
            plist2[i] = InclusiveStr()
        if not isinstance(p,str) or not isinstance(plist2[i],str):
            logger.error("Input must be a list of particle strings")
            raise SModelSError()
        elif not p in list ( ptcDic.keys() ) + list ( rEven.values() ):
            logger.error("Unknow particle: %s" %p)
            raise SModelSError()
        elif not plist2[i] in list ( ptcDic.keys() ) + list ( rEven.values() ):
            logger.error("Unknow particle: %s" %plist2[i])
            raise SModelSError()
                        
        
    l1 = sorted(plist1)
    l2 = sorted(plist2)
    if not useDict:
        return l1 == l2
    
    #If dictionary is to be used, replace particles by their dictionay entries
    #e.g. [jet,mu+] -> [[q,g,c],[mu+]], [jet,mu] -> [[q,g,c],[mu+,mu-]] 
    extendedL1 = []    
    for i,p in enumerate(plist1):
        if not p in ptcDic:
            extendedL1.append([p])
        else:
            extendedL1.append(ptcDic[p])
    extendedL2 = []    
    for i,p in enumerate(plist2):
        if not p in ptcDic:
            extendedL2.append([p])
        else:
            extendedL2.append(ptcDic[p])
    
    #Generate all combinations of particle lists (already sorted to avoid ordering issues)
    #e.g. [[q,g,c],[mu+]] -> [[q,mu+],[g,mu+],[c,mu+]]
    extendedL1 = [sorted(list(i)) for i in itertools.product(*extendedL1)]
    extendedL2 = [sorted(list(i)) for i in itertools.product(*extendedL2)]

    #Now compare the two lists and see if there is a match:
    for plist in extendedL1:
        if plist in extendedL2: return True
        
    return False


def getFinalStateLabel(pid):
    """
    Given the particle PID, returns the label corresponding to its final state
    (e.g. 1000022 -> MET, 1000023 -> HSCP,...)
    :parameter pid: PDG code for particle (must appear in particles.py)
    :return: Final state string (e.g. MET, HSCP,...)
    """

    from smodels.particlesLoader import qNumbers

    if pid == 0:
        # If pid is zero, return displaced
        return "Displaced"
    if not abs(pid) in qNumbers:
        logger.error("qNumbers are not defined for %i. Please, add it to particles.py." %pid)
        raise SModelSError
    elif not pid in qNumbers:  #Use the anti-particle info:
        pidQnumber = qNumbers[abs(pid)]
        pidQnumber[1] = -pidQnumber[1] #Flip the charge sign
    else:    
        pidQnumber = qNumbers[pid]
    for key,qnumberList in finalStates.items():
        if pidQnumber in qnumberList:
            return key
    
    logger.error("Final state for %i not found. Please, add it to particles.py." %pid)
    raise SModelSError


class InclusiveStr(str):
    """
    A string wildcard class. It will return True when compared to any other string.
    """
    
    def __init__(self):
        str.__init__(self)
        
    def __str__(self):
        return '*'    

    def __repr__(self):
        return self.__str__()

    def __cmp__(self,other):
        if isinstance(other,str):
            return 0
        else:
            return -1

    def __eq__(self,other):
        return self.__cmp__(other) == 0  
    
    def __ne__(self,other):
        return self.__cmp__(other) != 0
     
