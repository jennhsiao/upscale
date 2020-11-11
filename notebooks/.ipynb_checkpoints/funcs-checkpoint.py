import os
import pandas as pd 
import numpy as np
import pytz
from scipy import stats, linalg
from timezonefinder import TimezoneFinder


def tup_convert(tup):
    str = ''.join(tup)
    return str


def fold(val, min, max):
    """
    transform values normalized between 0-1 back to their regular range
    """
    
    fold_list = []
    for i in val: 
        fold_i = (i-min)/(max - min)
        fold_list.append(fold_i)        
    return fold_list


def unfold(val, min, max):
    """
    transform values normalized between 0-1 back to their regular range
    """
    
    unfold_list = []
    for i in val: 
        unfold_i = i*(max - min) + min
        unfold_list.append(unfold_i)        
    return unfold_list


def get_filelist(path):
    """
    For the given path, retrieve list of all files in the directory tree
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


def read_sims(files):
    """
    For the given file path of maizsim model output .txt files, 
    - 1. slightly resets column names for model output
    - 2. fetches year/site/cvar info from file name
    - 3. reads in last line of model output
    - 4. documents files with abnormal line output length and does not read them
    - 5. compiles year/site/cvar info & last line of model output into pd.DataFrame
    - 6. issues compiled into pd.DataFrame as well
    - 7. returns: df_sims & df_issues
    """
    
    cols = ['year', 'cvar', 'site', 'date', 'jday', 'time', 
            'leaves', 'mature_lvs', 'drop_lvs', 'LA', 'LA_dead', 'LAI', 
            'RH', 'leaf_WP', 'PFD', 'Solrad', 'temp_soil', 'temp_air', 'temp_can', 'ET_dmd', 'ET_suply',
            'Pn', 'Pg', 'resp', 'av_gs', 'LAI_sunlit', 'LAI_shaded', 'PFD_sunlit', 'PFD_shaded',
            'An_sunlit', 'An_shaded', 'Ag_sunlit', 'Ag_shaded', 'gs_sunlit', 'gs_shaded', 'VPD',
            'N', 'N_dmd', 'N_upt', 'N_leaf', 'PCRL', 'dm_total', 'dm_shoot', 'dm_ear', 'dm_totleaf',
            'dm_dropleaf', 'df_stem', 'df_root', 'roil_rt', 'mx_rootdept', 
            'available_water', 'soluble_c', 'note']

    years = []
    cvars = []
    sites = []
    data_all = []
    issues = []
    
    for file in files:
        # extrating basic file info
        year = int(file.split('/')[-3])
        site = file.split('/')[-1].split('_')[1]
        cvar = int(file.split('/')[-1].split('_')[-1].split('.')[0])

        # reading in file and setting up structure
        with open(file, 'r') as f:
            f.seek(0, os.SEEK_END) # moving the pointer to the very end of the file
                                   # * f.seek(offset, whence)
                                   # * The position is computed from adding offset to a reference point,
                                   # * the reference point is selected by the whence argument.
                                   # * os.SEEK_SET (=0)
                                   # * os.SEEK_CUR (=1)
                                   # * os.SEEK_END (=2)
            try: 
                f.seek(f.tell() - 3000, os.SEEK_SET) # finding the current position -
                                                     # (should be at the very end of the file)
                                                     # and counting back a few positions 
                                                     # and reading forward from there
                                    # * f.tell() returns an integer giving the file object’s 
                                    # * current position in the file represented as number of bytes 
                                    # * from the beginning of the file when in binary mode 
                                    # * and an opaque number when in text mode.
                for line in f:
                    f_content = f.readlines()

                if len(f_content[-1]) == 523: # character length of a normal output
                    sim_output = list(f_content[-1].split(','))
                    data = [i.strip() for i in sim_output]
                    data.insert(0, year)
                    data.insert(1, cvar)
                    data.insert(2, site)
                    data_all.append(data)

                else: 
                    issues.append(file)

            except:
                print(file)
                
    df_sims = pd.DataFrame(data_all, columns=cols)
    df_sims.dm_total = df_sims.dm_total.astype(float)
    df_sims.dm_ear = df_sims.dm_ear.astype(float)
    df_issues = pd.Series(issues, dtype='str')
    
    return df_sims, df_issues
    

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


def partial_corr(C):
    """
    Code source: https://gist.github.com/fabianp/9396204419c7b638d38f
    
    Adpoted from Matlab's partialcorr
    Uses the linear regression approach to compute the partial correlation,
    algorithms detailed here: http://en.wikipedia.org/wiki/Partial_correlation#Using_linear_regression
    
    --- Summary:
    Taking two variables of interest: X & Y, and the Z matrix with all the variables minus {X, Y}, 
    the algorithm:
    
    1) performs a normal linear least-squares regression with X as the target and Z as the predictor
    2) calculates the residuals in step #1
    3) performs a normal linear least-squars regression with Y as the target and Z as the predictor
    4) calcualtes the residuals in step #3
    5) calculates the correlation coefficient between the residuals from step #2 & step #4
    6) results give you the partial correlation between X & Y while controlling for the effect of Z
    
    --- Parameters:
    C: array-like, shape (n, p)
       Array with the different variables - can be a pandas dataframe
       Each column of C is taken as a variable.
    
    --- Returns:
    P: array-like, shape (p, p)
       p[i, j] contains the partial correlation of C[:, i] and C[:, j]
       while controlling for the remaining variables in C
    """
    
    C = np.asarray(C)
    p = C.shape[1]
    p_corr = np.zeros((p, p), dtype=np.float)
    for i in range(p):
        p_corr[i, i] = 1
        for j in range(i+1, p):
            idx = np.ones(p, dtype=np.bool)
            idx[i] = False
            idx[j] = False
            beta_i = linalg.lstsq(C[:, idx], C[:, j])[0]
            beta_j = linalg.lstsq(C[:, idx], C[:, i])[0]
            
            res_j = C[:, j] - C[:, idx].dot(beta_i)
            res_i = C[:, i] - C[:, idx].dot(beta_j)
            
            corr = stats.pearsonr(res_i, res_j)[0] # might want to switch this to Spearman
            p_corr[i, j] = corr
            p_corr[j, i] = corr # this line is just to mirrow the results to fill out whole matrix
    
    
    return p_corr


def find_zone(site, siteinfo):
    """
    find time zone for specific sites
    """
    lat = float(siteinfo[siteinfo.site == site].lat)
    lon = float(siteinfo[siteinfo.site == site].lon)
    tf = TimezoneFinder()    
    zone = tf.timezone_at(lng=lon, lat=lat)
    return zone


def utc_to_local(times, zone):
    """
    convert list of utc timestamps into local time
    """
    times = times.to_pydatetime() # convert from pd.DatetimeIndex into python datetime format
    utc = pytz.timezone('UTC') # setting up the UTC timezone, requires package 'pytz'
    local_datetime = list()
    
    for time in times:
        utctime = utc.localize(time) # adding UTC timezone to datetime
        localtime = utctime.astimezone(pytz.timezone(zone)) 
        datetime = pd.to_datetime(localtime)
        local_datetime.append(datetime)
        
    return local_datetime