## Get all rejected requests which is because of system busy and resend
#%%codecell
#import module
from errno import EMLINK
import json
from tkinter import E
import pyodbc
import os
from os.path import join,isfile,isdir
import email
from email.header import decode_header
import datetime
import re
import email.utils
import html
import jieba
import jieba.analyse
import poplib
import re
import time
#%%code cell
#set config
with open ("./config.json",'r',encoding='utf-8-sig') as f:
    params= json.load(f)

#%%code cell
def decode_str(s):
    '''
    DECODE sring s for email
    '''
    if not s:
        return None
    value1=''
    for ele in decode_header(s):
        value,charset = ele
        if charset:
            try:
                value1+=value.decode(charset,'ignore')
            except:
                value1+=value.decode('gbk','ignore')
        else:
            value1+=str(value)
    return value1

# %%code cell

poplib._MAXLINE=20480
server='outlook.office365.com'
port=995
user='syslucinda@outlook.com'
pswd='200312Az'
pop=poplib.POP3_SSL(server,port)
pop.user(user)
pop.pass_(pswd)
# %%code cell
#message list
poplist=pop.list()
#with poplist as ['mesg_num_index octets']

pattern="\.+(NAME)+[\w\W]+(\?{3})"
#net mail

for i,id in enumerate(poplist[1]):
    
    uidl=bytes.decode(id)
    uid=uidl.split(' ',1)[1]
    #whole message retrieve
    raw_email  = b"\n".join(pop.retr(i+1)[1])
    msg = email.message_from_bytes(raw_email)
    Eml_from =str(decode_str(msg.get('from')))
    if (Eml_from!="breq-fast-tiares-admin@ohpdmc.eri.u-tokyo.ac.jp"):
        continue

    #    subject title of email
    subject = decode_str(msg.get("Subject"))

    if (subject!="Breq-Fast has rejected data request"):
        continue
    body = msg.get_payload(decode=True)
    seedFile= re.search(pattern,body.decode("utf-8") )
    
    if (seedFile):
        if ("System busy" in body.decode("utf-8")):
            with open('rejectedRequest.txt','w') as f:
                f.write(seedFile.group()+'\n')
                f.close()
            os.system(f'cat rejectedRequest.txt | mail -s "TIARES" "breq-fast-tiares@ohpdmc.eri.u-tokyo.ac.jp"')
            time.sleep(120)
