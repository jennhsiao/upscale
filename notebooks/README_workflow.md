### Data Process & Analysis Workflow

#### 0. raw data download
1. Download ISH_NSRD dataset
    - wget script: /home/disk/eos8/ach315/upscale/raw_data_process
    - figure out site/years that have solar radiation data
    - store raw data: /home/disk/eos8/ach315/data/ISH_NSRD
    - data stored in individual folders for each year
2. Download ISH dataset
    - wget
    - only download site/years in which we know solar radiation data exits
    - Use WBAN weather station ID to reference stations in ISH_NSRD vs. ISH dataset
    - store raw data: /home/disk/eos8/ach315/data/ISH/
    - data stored in individual folders for each year
3. Create solar radiation file list based on the weather files left after cleaning up
    - solfile_list_1961to1990 is created based on weafile_list_1961to1990


#### 1. prep: meteorology data
- weafile_read
- weafile_process
- weafile_visualization

#### 2. prep: model inputs
- init_siteyear
- init_param

#### 3. prep: simulation setup
- wflow_con
- wflow_opt

#### 4. analysis: model output
- sim_con
- sim_opt5
- sim_opt100

