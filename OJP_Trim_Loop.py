#!/usr/bin/env python
# coding: utf-8

# In[19]:


### No instrument response removal is done in this script due to the (super) long run time.
### Perform instrument response removal in the trim_event code instead.
### This script does not do downsampling.
### Components are currently not in the loop. Run for each component.
# import libraries
from obspy import read
from obspy.io.xseed import Parser
from obspy.signal import PPSD

import obspy
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from obspy.core import AttribDict
from obspy.io.sac import SACTrace
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

from obspy import read
from obspy import read_inventory
from obspy.core.inventory import Inventory, Network, Station, Channel, Site
from obspy.clients.nrl import NRL
from obspy.imaging.cm import pqlx

import glob
import configparser
import multiprocessing
import time
import sys
import pickle
import io


# In[21]:


tslst = ["20150101","20150301","20150501","20150701","20150901","20151101","20160101","20160301","20160501","20160701"]
telst = ["20150301","20150501","20150701","20150901","20151101","20160101","20160301","20160501","20160701","20160901"]

### define trace length
reclen = 512
numchunks = 20000
chunksize = numchunks * reclen # Around 50 MB
#stalst = ["OJ02","OJ03","OJ04","OJ05","OJ06","OJ08","OJ09","OJ11","OJ12","OJ13","OJ14","OJ15","OJ16","OJ18","OJ19","OJ20","OJ22"]
stalst = ["OJ02","OJ06","OJ08","OJ11","OJ14"] # for pressure record

### loop through stations
for sta in stalst:
    stadir = '/scratch/tolugboj_lab/Prj4c_OJP/2_Data/OJP_Data/'+sta #+'/Original' #for 100 Hz
    station = sta
    print('working on station '+station)
    invFull = read_inventory('/scratch/tolugboj_lab/Prj4c_OJP/2_Data/OJP_Data/xml/PS_'+sta+'.xml')
    
    ### loop through seed files
    for i in range(len(tslst)):
        filepath = '/scratch/tolugboj_lab/Prj4c_OJP/2_Data/OJP_Data/'+sta+'/'+sta+tslst[i]+telst[i]+'.seed'
        tstart = tslst[i][:4]+'-'+tslst[i][4:6]+'-'+tslst[i][6:8]+'T00:00:00'
        tend = telst[i][:4]+'-'+telst[i][4:6]+'-'+telst[i][6:8]+'T00:00:00'
        count  = 0;
        with io.open(filepath, 'rb') as fh:
            while True:
                with io.BytesIO() as buf:
                    c = fh.read(chunksize)
                    if not c:
                        break
                    buf.write(c)
                    buf.seek(0, 0)
                    st = obspy.read(buf)
                    tr = st.select(id='PS.'+sta+'..HHZ') ####### change component #######
                
                    if len(tr) == 0:
                        continue
                
                    if count == 0:
                        st_all = tr
                    if count > 1:
                        st_all += tr
                
                    count += 1
                
            st_all.sort(['starttime'])
            print('Sort Done')
        
            # start time in plot equals 0
            dt = st_all[0].stats.starttime.timestamp
        
            # Go through the stream object, determine time range in julian seconds
            # and plot the data with a shared x axis

            # Merge the data together and show plot in a similar way
            st_test = st_all
            st_test.merge(method=1, fill_value=0)

            print('Merge Done')
            
            # cut and save in days
            trlen = 24*60*60

            dayvec = pd.date_range(start=tstart, end=tend, freq=str(trlen)+'S')
            sr_new = 1
            is_downsamp = 1

            # loop through days
            for iday, DAY in enumerate(dayvec) :
                    daystr = DAY.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    print('Working on ' + station + ' : ' + daystr)
    
                    tdbeg = UTCDateTime(DAY.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
                    tdend = UTCDateTime((DAY+pd.Timedelta(seconds=trlen)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        
                    st_all = st_test.copy()
                    st = st_all.trim(starttime=tdbeg, endtime=tdend, pad=True, nearest_sample=False, fill_value=0) # make sure correct length
                    print('Trim Complete')
                    sr = st[0].stats.sampling_rate
                    st.detrend(type='demean')
                    st.detrend(type='linear')
                    st.taper(type="cosine",max_percentage=0.05)
                    if is_downsamp and sr!=sr_new:
                        st.filter('lowpass', freq=0.4*sr_new, zerophase=True) # anti-alias filter
                        st.decimate(factor=int(sr/sr_new), no_filter=True) # downsample
                    st.detrend(type='demean')
                    st.detrend(type='linear')
                    st.taper(type="cosine",max_percentage=0.05)
            
                    # convert to SAC and fill out station/event header info
                    st.plot()
                    for tr in st:
                        sac = SACTrace.from_obspy_trace(tr)
                        sac.stel = invFull[0].stations[0].elevation
                        sac.stla = invFull[0].stations[0].latitude
                        sac.stlo = invFull[0].stations[0].longitude
                        kcmpnm = sac.kcmpnm
                        yr = str(st[0].stats.starttime.year)
                        jday = '%03i'%(st[0].stats.starttime.julday)
                        hr = '%02i'%(st[0].stats.starttime.hour)
                        mn = '%02i'%(st[0].stats.starttime.minute)
                        sec = '%02i'%(st[0].stats.starttime.second)
                        sac_out = stadir + '/' + station+'.'+yr+'.'+jday+'.'+hr+'.'+mn+'.'+sec+'.'+kcmpnm+'.sac'
                        #sac.write(sac_out)

