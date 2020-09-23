import numpy as np
import pandas as pd
from funcs import CC_VPD


### reading in weather data
df_temp = pd.read_csv('/home/disk/eos8/ach315/upscale/weadata/temp_all.csv', index_col= 0)
df_rh = pd.read_csv('/home/disk/eos8/ach315/upscale/weadata/rh_all.csv', index_col= 0)
df_precip = pd.read_csv('/home/disk/eos8/ach315/upscale/weadata/precip_all.csv', index_col= 0)
df_solrad = pd.read_csv('/home/disk/eos8/ach315/upscale/weadata/solrad_all.csv', index_col= 0)

# interpolating weather data 
df_temp = df_temp.interpolate()
df_rh = df_rh.interpolate()
df_precip = df_precip.interpolate()
df_solrad = df_solrad.interpolate()


### Selecting site-years
# read in sites info
df_sites_all = pd.read_csv('/home/disk/eos8/ach315/upscale/weadata/site_summary.csv', 
                           index_col=0, dtype={'site': str})

# filter based on planting area & irrigation
df_sites = df_sites_all[(df_sites_all.area > 1000) & (df_sites_all.perct_irri < 50)]
df_sites.head()
# fetch list of site-years
siteyear_ctr2 = pd.read_csv('/home/disk/eos8/ach315/upscale/weadata/siteyears_crithr2.csv', 
                            usecols=[1,2], dtype='str') 
siteyears = siteyear_ctr2[siteyear_ctr2.site.isin(df_sites.site)] 


### converting the dataframe-style weather data into a single long-form list
# only selecting weather data for filtered siteyears
temp_all = [np.nan]*siteyears.shape[0]
rh_all = [np.nan]*siteyears.shape[0]
precip_all = [np.nan]*siteyears.shape[0]
solrad_all = [np.nan]*siteyears.shape[0]

# plotting data for growing season between 4/1 - 10/31
season_start = '-04-01'
season_end = '-10-31'

for i in np.arange(siteyears.shape[0]):
    # growing season temp mean for each site-year
    temp = df_temp.loc[siteyears.iloc[i,1] + season_start: 
                       siteyears.iloc[i,1] + season_end, 
                       siteyears.iloc[i,0]].mean()
    # growing season RH mean for each site-year
    rh = df_rh.loc[siteyears.iloc[i,1] + season_start: 
                   siteyears.iloc[i,1] + season_end, 
                   siteyears.iloc[i,0]].mean()
    # growing season precip sum for each site-year
    precip = df_precip.loc[siteyears.iloc[i,1] + season_start: 
                           siteyears.iloc[i,1] + season_end, 
                           siteyears.iloc[i,0]].sum()

    # solar radiation
    solrad = df_solrad.loc[siteyears.iloc[i,1] + season_start: 
                           siteyears.iloc[i,1] + season_end, 
                           siteyears.iloc[i,0]].mean()
    
    temp_all[i] = temp
    rh_all[i] = rh
    precip_all[i] = precip
    solrad_all[i] = solrad
    
# calculating VPD based on temperature & RH
vpd_all = []
for i in np.arange(len(temp_all)):
    vpd_all.append(CC_VPD(temp_all[i], rh_all[i]/100))
    
# storing output in dataframe
df_siteyears_weamean = siteyears.copy()
df_siteyears_weamean['temp'] = list(temp_all)
df_siteyears_weamean['rh'] = list(rh_all)
df_siteyears_weamean['precip'] = list(precip_all)
df_siteyears_weamean['solrad'] = list(solrad_all)
df_siteyears_weamean['vpd'] = list(vpd_all)

# save processed weather data as .csv
#df_siteyears_weamean.to_csv('/home/disk/eos8/ach315/upscale/weadata/wea_summary.csv')
