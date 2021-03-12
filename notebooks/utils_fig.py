import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import seaborn as sns
import numpy as np
from palettable.colorbrewer.sequential import YlGn_9


def maps(sites, data, title='title', cbar_lab='cbar_lab'):
    """
    plots out a basic map for maizsi simulation outputs
    """
    
    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot(1,1,1, projection=ccrs.AlbersEqualArea(
                              central_latitude=39.5, central_longitude=-98.35))
    ax.set_extent([-123, -72, 19, 53])
    mp = ax.scatter(sites.lon, sites.lat, transform=ccrs.PlateCarree(), 
                    s=60, c=data.dm_ear, cmap=YlGn_9.mpl_colormap, 
                    vmin=20, vmax=70, alpha=0.8)
    ax.add_feature(cfeature.BORDERS, edgecolor='grey')
    ax.add_feature(cfeature.COASTLINE, edgecolor='grey')
    ax.add_feature(cfeature.STATES, edgecolor='grey', linewidth=0.5)
    ax.set_title(title)
    cbar = fig.colorbar(mp, ax=ax, shrink=0.7)
    cbar.set_label(cbar_lab, size=12, weight='light')

    
def bars(data, fig_w=10, fig_h=4, bar_width=0.8, 
         title='title', xlab='xlabel', ylab='ylabel'):
    """
    sdf
    """
    
    x = np.arange(len(data))
    width=bar_width
    
    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = fig.add_subplot(1,1,1)
    ax.bar(x-width/2, data, width, alpha=0.5)
    ax.set_xlabel(xlab, size=12, weight='light')
    ax.set_ylabel(ylab, size=12, weight='light')
    ax.set_title(title, size=12)
