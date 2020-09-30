import pandas as pd
from funcs import get_filelist, read_sims

filelist = get_filelist('/home/disk/eos8/ach315/upscale/sims/opt/')
files = filelist[:]
df_sims, df_issues = read_sims(files)
df_sims.to_csv('/home/disk/eos8/ach315/upscale/data/sims_6105.csv', index=False)