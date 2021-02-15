from datetime import date, timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
import json
import math as m
def D(x):
    return np.deg2rad(x)
    
API_URL = 'http://api.timezonedb.com/v2.1/get-time-zone'

latitude = 3.0685
longitude = 101.7704


# latitude = 30.211543
# longitude = 101.804091

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

# D = np.pi / 180

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
# sun_path.set_yticks([str(i) for i in range (90,0,30)])


for tempFrame in lines:
    # r = [np.pi - q for q in tempFrame['elevation']]
    r = tempFrame['elevation']
    theta = np.real(tempFrame['azimuth'])
    sun_path.plot(theta,r,linestyle='-.', marker='.',label='a',color='r')
    
plt.title(f'{parsed["countryName"]} {base_year}| {old_lat},{longitude}')
plt.show()