import pandas as pd
from funcs import get_filelist, read_sims

# get_filelist: for the given path, retrieve list of all files within the directory tree, including those in subdirectories
filelist = get_filelist('/home/disk/eos8/ach315/upscale/sims/opt/')
files = filelist[:]

# read_sims: read in last line of maizsim simulation output, organize and form into pd.DataFrame
# outputs: df_sims
df_sims, df_issues = read_sims(files)

# store output since processing raw maizsim outputs take quite some time
#df_sims.to_csv('/home/disk/eos8/ach315/upscale/data/sims_6105.csv', index=False)