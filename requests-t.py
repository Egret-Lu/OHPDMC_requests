# %%code cell
#import module
import pandas as pd
import numpy as np
import os
import datetime

import time


# %% code cell
#sta list
#structure: network, station, startdate,enddate
sta_df=pd.read_csv('stalist/tlist.csv')
sta_df['Start']= pd.to_datetime(sta_df['Start'],format='%Y-%m-%d')
sta_df['End']= pd.to_datetime(sta_df['End'],format='%Y-%m-%d')

# %%code cell
#personal information
req_info = ['.NAME Xinxuan Lu','.INST University of Rochester',
'.MAIL Hutchison Hall 329','.EMAIL syslucinda@outlook.com',
'.PHONE 5854656353']
req_info='\n'.join(req_info)
# %% code cell
# request on rows
for index, row in sta_df.iterrows():
    
    startDate=row['Start']
    endDate=row['End']
    net = row['Network']
    sta = row['Station']
    fileName = f'{net}_req.txt'
    dateCur=startDate
    while dateCur <= endDate:
        #iterate for each week in range
        #for each station sabtch a request on each day
        dayStart= dateCur
        dayEnd = dateCur+datetime.timedelta(20)
        #SET LABEL FOR EACH REQUEST
        label = '.LABEL '
        label += '_'.join([net,sta,dateCur.strftime("%Y%m%d")])
        

        #format example: T01 PS 2007 02 01 00 00 00.0 2007 02 02 00 00 00.0 1 ???
        requestStr = ' '.join([sta,'PS',dayStart.strftime("%Y %m %d"),'00 00 00.0'
        ,dayEnd.strftime("%Y %m %d"),'00 00 00.0 1 ???'])
        #write requests
        """
        format sample
        .NAME Xinxuan Lu
        .INST University of Rochester
        .MAIL Hutchison Hall 329
        .EMAIL syslucinda@outlook.com
        .PHONE 5854656353
        .LABEL OJP_1
        .END

        T01 PS 2007 02 01 00 00 00.0 2007 02 02 00 00 00.0 1 ???
        """
       
        with open(fileName,'w') as f:
            f.write(req_info)
            f.write('\n')
            f.write(label)
            f.write('\n')
            f.write('.END')
            f.write('\n\n')
            f.write(requestStr)
            f.close()
        #remember to set stmp on the system
        os.system(f'cat {fileName} | mail -s "{label}" breq-fast-{net.lower()}@ohpdmc.eri.u-tokyo.ac.jp')
        print(f'submit {[net,sta,dateCur.strftime("%Y%m%d")]}')
        dateCur+=datetime.timedelta(20)
        time.sleep(60)

# %%
