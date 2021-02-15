from datetime import date, timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
import json



# =============================================================================
# def fig2data ( fig ):
#     """
#     @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
#     @param fig a matplotlib figure
#     @return a numpy 3D array of RGBA values
#     """
#     fig.canvas.draw()
#     # Get the RGBA buffer from the figure
#     w,h = fig.canvas.get_width_height()
#     buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
#     buf.shape = ( w, h,4 )
#  
#     # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
#     buf = np.roll ( buf, 3, axis = 2 )
#     return buf
# 
# def fig2img ( fig ):
#     """
#     @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
#     @param fig a matplotlib figure
#     @return a Python Imaging Library ( PIL ) image
#     """
#     # put the figure pixmap into a numpy array
#     buf = fig2data ( fig )
#     w, h, d = buf.shape
#     return Image.frombytes( "RGBA", ( w ,h ), buf.tobytes() )
# =============================================================================

def D(x):
    return np.deg2rad(x)

def make_graph(latitude, longitude):
    
    API_URL = 'http://api.timezonedb.com/v2.1/get-time-zone'

    current = datetime.now()
    # timestamp = datetime.timestamp(current)
    base_year = current.year
    base_date = date(base_year,1,1)

    with open("cred.json") as f:
        data = json.load(f)
        
    key = data["key"]

    parameters = {"key":key,
                "by":"position",
                "lat":latitude,
                "lng":longitude,
                "format":"json"}

    timezdb = requests.get(API_URL,params=parameters)
    parsed = json.loads(timezdb.content)

    deltaGMT_a = (parsed['gmtOffset']/3600)

    data = pd.DataFrame(data=None)
    # times = np.linspace(4,21,100,endpoint=True)
    times = np.arange(4,21)
    dates = [date(base_year,i,21) for i in range(1,13)]

    latitude,old_lat = D(latitude), latitude

        
    for j in dates:
        
        # LSTM = 15*D * (deltaGMT_a)
        
        days_since = j-base_date
        B = ((360/365) + (days_since.days +285))
        # delta = D(23.45) * np.sin(D(B))
        delta = D(23.45) * np.sin(D(B))

        # EoT = 9.878*np.sin(2*B) - 7.53*np.cos(B) - 1.5*np.sin(B)
        
        # TC = (4/D)*(longitude*D - LSTM) + EoT

        
        
        for i in np.arange(-np.pi,np.pi+D(15),step=D(15)):
        
    # =============================================================================
    #         LST = i+TC/60
    #         
    #         HRA = D*15*(LST-12)
    # =============================================================================
            HRA = i
            
            
            elevation = np.arcsin(np.sin(delta)*np.sin(latitude)+np.cos(delta)*np.cos(latitude)*np.cos(HRA))
            
            intermediate = (np.sin(delta)*np.cos(latitude)-np.cos(delta)*np.sin(latitude)*np.cos(HRA))/np.cos(elevation)
            azimuth = np.arccos(np.clip(intermediate,-1,1))
        
            
            if  HRA>0:
                azimuth = 2*np.pi - azimuth
                
            
            to_store = {"day":j,
                        "elevation": elevation,
                        "azimuth":azimuth,
                        "intermediate":intermediate
                        }
        
            data = data.append(to_store,ignore_index=True)
        
    
    lines = [data[data.day==i] for i in dates]
    sun_path = plt.subplot(1,1,1,projection='polar')
    sun_path.set_theta_zero_location('N')
    sun_path.set_theta_direction(-1)
    sun_path.set_rlim(np.pi/2, 0,D(15))
    sun_path.set_thetalim(0,2*np.pi)
    sun_path.set_xticks([D(i) for i in range(0,360, 30)])


    for tempFrame in lines:
        r = tempFrame['elevation']
        theta = np.real(tempFrame['azimuth'])
        sun_path.plot(theta,r,linestyle='-.', marker='.',label='a',color='r')
    
    fig = plt.gca()
    x_axis = fig.axes.get_xaxis()
    x_axis.set_ticklabels([])
    
    y_axis = fig.axes.get_yaxis()
    y_axis.set_visible(False)
    plt.savefig(r'C:\Users\Iz\Desktop\Solar_Path_App\test_pics\graphed.png',transparent=True,dpi=200)


