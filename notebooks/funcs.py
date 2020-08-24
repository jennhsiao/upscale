# functions for file 'opt_param'

def tup_convert(tup):
    str = ''.join(tup)
    return str

def unfold(val, min, max):
    """
    transform values normalized between 0-1 back to their regular range
    """
    unfold_list = []
    for i in val: 
        unfold_i = i*(max - min) + min
        unfold_list.append(unfold_i)        
    return unfold_list

def fold(val, min, max):
    """
    transform values normalized between 0-1 back to their regular range
    """
    fold_list = []
    for i in val: 
        fold_i = (i-min)/(max - min)
        fold_list.append(fold_i)        
    return fold_list

def get_filelist(path):
    """
    For the given path, get the List of all files in the directory tree
    including those in subdirectories
    """
    # create a list of file and sub directories names in the given directory 
    filelist = os.scandir(path)
    allfiles = list()
    # iterate over all the entries
    for entry in filelist:
        # create full path
        fullpath = os.path.join(path, entry)
        # if entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullpath):
            allfiles = allfiles + get_filelist(fullpath)
        else:
            allfiles.append(fullpath)
    return allfiles

def CC_VPD(temp, rh):
    """
    function that calculates VPD with temperature and RH
    RH values range between 0 & 1 (fraction, not %)
    """
    # constant parameters
    Tref = 273.15  # reference temperature
#    Es_Tref = 6.11 # saturation vapor pressure at reference temperature (mb)
    Es_Tref = 0.611 # saturation vapor pressure at reference temperature (kPa)
    Lv = 2.5e+06   # latent heat of vaporation (J/kg)
    Rv = 461       # gas constant for moist air (J/kg)
    
    # transformed temperature inputs
    Tair = temp + Tref
    
    # Clausius-Clapeyron relation
    es = Es_Tref*np.exp((Lv/Rv)*(1/Tref - 1/Tair))
    e = es*rh
    vpd = es-e
    
    return(vpd)