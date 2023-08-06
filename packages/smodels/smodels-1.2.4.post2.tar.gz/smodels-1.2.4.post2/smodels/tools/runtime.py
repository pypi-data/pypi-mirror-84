#!/usr/bin/env python3

"""
.. module:: runtime
    :synopsis: Tools to gather info about runtime enviroment,
               ( nCPUs() ), or obtain file type ( filetype() ). Pointer
               to model file is also kept here.

.. moduleauthor:: Wolfgang Waltenberger <wolfgang.waltenberger@gmail.com>

"""

## place to keep the pointer to the model file
modelFile="share.models.mssm"

def filetype ( filename ):
    """ obtain information about the filetype of an input file,
        currently only used to discriminate between slha and lhe
        files.

        :returns: filetype as string("slha" or "lhe"),
                  None if file does not exist, or filetype is unknown.
    """
    import os
    if not os.path.exists ( filename ):
        return None
    if filename.endswith(".slha"):
        return "slha"
    if filename.endswith(".SLHA"):
        return "slha"
    if filename.endswith(".lhe" ):
        return "lhe"
    if filename.endswith(".LHE" ):
        return "lhe"
    try:
        with open ( filename, "rt" ) as f:
            for line in f:
                if "<LesHouchesEvents" in line:
                    return "lhe"
                if "<event>" in line:
                    return "lhe"
                if "block " in line.lower():
                    return "slha"
    except UnicodeDecodeError:
        ## a binary file??
        return None
    return None

def nCPUs():
    """ obtain the number of CPU cores on the machine, for several
        platforms and python versions. """
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except ImportError as e:
        pass
    try:
        import psutil
        return psutil.NUM_CPUS
    except ImportError as e:
        pass
    try:
        import os
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))
        if res>0: return res
    except ImportError as e:
        pass
    return None

if __name__ == "__main__":
    print ( "This machine has %d CPUs" % nCPUs() )
