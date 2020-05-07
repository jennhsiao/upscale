## Creating MAIZSIM Weather File Input
### 1. The NASA Integrated Surfact Hourly Dataset (ISH)
[ISD dataset](https://www.ncdc.noaa.gov/isd/data-access) - choose FTP access

#### Site Info
- pos 1-4: The number of characters in the variable data section.
- pos 5-10: USAF identifier (1991-2010)
- pos 11-15: WBAN identifier (1961-1990)
- pos 16-23: Observation date
- pos 24-27: Observation time
- pos 28-28: Flag
- pos 29-34: Latitude
- pos 35-41: Longitude
- pos 47-51: Elevation

#### Mandatory Data Section
- pos 66-69: Wind speed (m/s)
- pos 70-70: Wind speed quality code
- pos 88-92: Air temperature (˚C)
- pos 93-93: Air temperature quality code
- pos 94-98: Dew point temperature (˚C)
- pos 99-99: Dew point temperature quality

#### Additional Data Section 
- AA1: precipitation (liquid precipitation occurrence identifier)
- first search for AA1 within data, the values following it indicate data as following:
- FLD LEN 2: liquid preciptiation period quantity in hours (hours)
- FLD LEN 4: liquid precipitation depth dimension (mm)
- FLD LEN 1: liquid precipitation condition code
- FLD LEN 1: liquid precipitation quality code


### 2. The NSRD Hourly Solar Radiation Dataset
[NSRD dataset](https://rredc.nrel.gov/solar/old_data/nsrdb/)

#### Year 1961-1990 Dataset (WBAN ID#): 

##### Headers
- 002-006: WBAN number
- 008-029: City
- 031-032: State
- 034-036: Time Zone
- 039-044: Latitude
    - 039: N = North of equator
    - 040-042: Degree
    - 043-044: Minutes
- 047-053: Longitude
    - 047: W = West, E = East
    - 048-050: Degree
    - 052-053: Minutes
- 056-059: Elevation

##### Data Elements
- 002-012: Local standard time
- 024-030: Global horizontal radiation (GHR, Wh/m2)

#### Year 1991-2010 Dataset (USAF ID#):

##### Data Elements
- col01: YYYY-MM-DD
- col02: HH:MM
- col16: METSTAT Glo (Wh/m2)

