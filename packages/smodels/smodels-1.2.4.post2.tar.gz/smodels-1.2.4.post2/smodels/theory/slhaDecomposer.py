#!/usr/bin/env python3

"""
.. module:: slhaDecomposer
   :synopsis: Decomposition of SLHA events and creation of TopologyLists.

.. moduleauthor:: Andre Lessa <lessa.a.p@gmail.com>
.. moduleauthor:: Wolfgang Waltenberger <wolfgang.waltenberger@gmail.com>

"""

import copy
import time
import pyslha
from smodels.theory import element, topology, crossSection
from smodels.theory.branch import Branch, decayBranches
from smodels.tools.physicsUnits import fb, GeV, mm, m, MeV,fm
import math
from smodels.theory.exceptions import SModelSTheoryError as SModelSError
from smodels.tools.smodelsLogging import logger

def decompose(slhafile, sigcut=.1 * fb, doCompress=False, doInvisible=False,
              minmassgap=-1.*GeV, useXSecs=None):
    """
    Perform SLHA-based decomposition.

    :param slhafile: the slha input file. May be an URL (though http, ftp only).
    :param sigcut: minimum sigma*BR to be generated, by default sigcut = 0.1 fb
    :param doCompress: turn mass compression on/off
    :param doInvisible: turn invisible compression on/off
    :param minmassgap: maximum value (in GeV) for considering two R-odd particles
                       degenerate (only revelant for doCompress=True )
    :param useXSecs: optionally a dictionary with cross sections for pair
                 production, by default reading the cross sections
                 from the SLHA file.
    :returns: list of topologies (TopologyList object)

    """
    if slhafile.startswith("http") or slhafile.startswith("ftp"):
        logger.info ( "asked for remote slhafile %s. will fetch it." % slhafile )
        import requests
        import os.path
        r=requests.get(slhafile)
        if r.status_code != 200:
            logger.error ( "could not retrieve remote file %d: %s" % ( r.status_code, r.reason ) )
            raise SModelSError()
        basename = os.path.basename ( slhafile )
        f=open ( basename, "w" )
        f.write ( r.text )
        f.close()
        slhafile = basename
    t1 = time.time()

    if doCompress and minmassgap / GeV < 0.:
        logger.error("Asked for compression without specifying minmassgap. Please set minmassgap.")        
        raise SModelSError()

    if type(sigcut) == type(1.):
        sigcut = sigcut * fb

    try:
        f=pyslha.readSLHAFile ( slhafile )
    except pyslha.ParseError as e:
        logger.error ( "The file %s cannot be parsed as an SLHA file: %s" % (slhafile, e) )
        raise SModelSError()

    # Get cross section from file
    xSectionList = crossSection.getXsecFromSLHAFile(slhafile, useXSecs)
    # Get BRs and masses from file
    brDic, massDic = _getDictionariesFromSLHA(slhafile)
    # Only use the highest order cross sections for each process
    xSectionList.removeLowerOrder()
    # Order xsections by PDGs to improve performance
    xSectionList.order()
    #Reweight decays by fraction of prompt decays and add fraction of long-lived
    brDic = _getPromptDecays(slhafile,brDic)

    # Get maximum cross sections (weights) for single particles (irrespective
    # of sqrtS)
    maxWeight = {}
    for pid in xSectionList.getPIDs():
        maxWeight[pid] = xSectionList.getXsecsFor(pid).getMaxXsec()    

    # Generate dictionary, where keys are the PIDs and values 
    # are the list of cross sections for the PID pair (for performance)
    xSectionListDict = {}    
    for pids in xSectionList.getPIDpairs():
        xSectionListDict[pids] = xSectionList.getXsecsFor(pids)

    # Create 1-particle branches with all possible mothers
    branchList = []
    for pid in maxWeight:
        branchList.append(Branch())
        branchList[-1].PIDs = [[pid]]
        if not pid in massDic:
            logger.error ( "pid %d does not appear in masses dictionary %s in slhafile %s" % 
                    ( pid, massDic, slhafile ) )
        branchList[-1].masses = [massDic[pid]]
        branchList[-1].maxWeight = maxWeight[pid]

    # Generate final branches (after all R-odd particles have decayed)
    finalBranchList = decayBranches(branchList, brDic, massDic, sigcut)
    # Generate dictionary, where keys are the PIDs and values are the list of branches for the PID (for performance)
    branchListDict = {}
    for branch in finalBranchList:
        if len(branch.PIDs) != 1:
            logger.error("During decomposition the branches should \
                            not have multiple PID lists!")
            return False   
        if branch.PIDs[0][0] in branchListDict:
            branchListDict[branch.PIDs[0][0]].append(branch)
        else:
            branchListDict[branch.PIDs[0][0]] = [branch]
    for pid in xSectionList.getPIDs():
        if not pid in branchListDict: branchListDict[pid] = []

    #Sort the branch lists by max weight to improve performance:
    for pid in branchListDict:
        branchListDict[pid] = sorted(branchListDict[pid], 
                                     key=lambda br: br.maxWeight, reverse=True)
    
    smsTopList = topology.TopologyList()
    # Combine pairs of branches into elements according to production
    # cross section list
    for pids in xSectionList.getPIDpairs():
        weightList = xSectionListDict[pids]
        minBR = (sigcut/weightList.getMaxXsec()).asNumber()
        if minBR > 1.: continue
        for branch1 in branchListDict[pids[0]]:
            BR1 = branch1.maxWeight/maxWeight[pids[0]]  #Branching ratio for first branch            
            if BR1 < minBR: break  #Stop loop if BR1 is already too low            
            for branch2 in branchListDict[pids[1]]:
                BR2 = branch2.maxWeight/maxWeight[pids[1]]  #Branching ratio for second branch
                if BR2 < minBR: break  #Stop loop if BR2 is already too low
                
                finalBR = BR1*BR2                
                if type(finalBR) == type(1.*fb):
                    finalBR = finalBR.asNumber()
                if finalBR < minBR: continue # Skip elements with xsec below sigcut

                if len(branch1.PIDs) != 1 or len(branch2.PIDs) != 1:
                    logger.error("During decomposition the branches should \
                            not have multiple PID lists!")
                    return False    

                newElement = element.Element([branch1, branch2])
                newElement.weight = weightList*finalBR
                newElement.sortBranches()  #Make sure elements are sorted BEFORE adding them
                smsTopList.addElement(newElement)
    
    smsTopList.compressElements(doCompress, doInvisible, minmassgap)
    smsTopList._setElementIds()

    logger.debug("slhaDecomposer done in %.2f s." % (time.time() -t1 ) )
    return smsTopList

def writeIgnoreMessage(keys, rEven, rOdd):
    msg = ""
    for pid in keys:
        if not pid in list(rEven) + list(rOdd):
            logger.warning("Particle %i not defined in particles.py, its decays will be ignored" %(pid))
            continue
        if pid in rEven:
            msg += "%s, " % rEven[pid]
            continue
    if len(msg)>0:
            logger.debug ( "Ignoring %s decays" % msg[:-2] )

def _getDictionariesFromSLHA(slhafile):
    """
    Create mass and BR dictionaries from an SLHA file.
    Ignore decay blocks with R-parity violating or unknown decays

    """

    from smodels.particlesLoader import rEven, rOdd

    res = pyslha.readSLHAFile(slhafile)

   
    # Get mass and branching ratios for all particles
    brDic = {}
    writeIgnoreMessage(res.decays.keys(), rEven, rOdd)

    for pid in res.decays.keys():
        if not pid in rOdd:
            continue
        brs = []
        for decay in res.decays[pid].decays:
            nEven = nOdd = 0.
            for pidd in decay.ids:
                if pidd in rOdd: nOdd += 1
                elif pidd in rEven: nEven += 1
                else:
                    logger.warning("Particle %i not defined in particles.py,decay %i -> [%s] will be ignored" %(pidd,pid,decay.ids))
                    break
            if nOdd + nEven == len(decay.ids) and nOdd == 1:
                brs.append(decay)
            else:
                logger.info("Ignoring decay: %i -> [%s]",pid,decay.ids)

        brsConj = copy.deepcopy(brs)
        for br in brsConj:
            br.ids = [-x for x in br.ids]
        brDic[pid] = brs
        brDic[-pid] = brsConj
    # Get mass list for all particles
    massDic = dict(res.blocks['MASS'].items())
    for pid in list ( massDic.keys() )[:]:
        massDic[pid] = round(abs(massDic[pid]),1)*GeV
        if not -pid in massDic: massDic[-pid] = massDic[pid] 

    #Include proxy for displaced decays
    if 0 in massDic or 0 in brDic:
        logger.error("PDG = 0 is reserved for displaced decays and it can not be used for other particles. Please redefine the input model PDG assignments.")
        raise SModelSError()
    else:
        dispPid = 0
        massDic[dispPid] = 0. * GeV
        dispDec = pyslha.Decay(br=1., ids=[], nda=0)
        brDic[dispPid] = [dispDec]
   
 
    return brDic, massDic



def _getPromptDecays(slhafile,brDic,l_inner=1.*mm,gb_inner=1.3,l_outer=10.*m,gb_outer=1.43):
    """
    Using the widths in the slhafile, reweights the BR dictionary with the fraction
    of prompt decays and add the fraction of "long-lived decays".
    The fraction of prompt decays and "long-lived decays" are defined as:
    F_prompt = 1 - exp(-width*l_inner/gb_inner)
    F_long = exp(-width*l_outer/gb_outer)
    where l_inner is the inner radius of the detector, l_outer is the outer radius
    and gb_x is the estimate for the kinematical factor gamma*beta for each case.
    We use gb_outer = 10 and gb_inner= 0.5
    :param widthDic: Dictionary with the widths of the particles
    :param l_inner: Radius of the inner tracker
    :param gb_inner: Effective gamma*beta factor to be used for prompt decays
    :param l_outer: Radius of the outer detector
    :param gb_outer: Effective gamma*beta factor to be used for long-lived decays
    
    :return: Dictionary = {pid : decay}
    """
    
    hc = 197.327*MeV*fm  #hbar * c
        
    #Get the widths:
    res = pyslha.readSLHAFile(slhafile)
    decays = res.decays

    #PID for displaced decays:
    dispPid = 0
        
    for pid in brDic:
        if pid == dispPid:
            continue
        width = abs(decays[abs(pid)].totalwidth)*GeV
        Fprompt = 1. - math.exp(-width*l_inner/(gb_inner*hc))
        Flong = math.exp(-width*l_outer/(gb_outer*hc))
        for decay in brDic[pid]:
            decay.br *= Fprompt  #Reweight by prompt fraction
            
        #Add long-lived fraction:
        if Flong > 1e-50:
            stableFraction = pyslha.Decay(br=Flong,ids=[],nda=0)
            brDic[pid].append(stableFraction) 
        if (Flong+Fprompt) > 1.:
            logger.error("Sum of decay fractions > 1 for "+str(pid))
            return False
        Fdisp = 1 - Flong - Fprompt
        #Add displaced decay:
        if Fdisp > 0.001:
            displacedFraction = pyslha.Decay(br=Fdisp, ids = [dispPid], nda=1)
            brDic[pid].append(displacedFraction)
        
    return brDic
