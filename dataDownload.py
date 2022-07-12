#%%codecell
#import module
import json
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

#%%code cell
#set config
with open ("./config.json",'r',encoding='utf-8-sig') as f:
	params= json.load(f)
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
poplist=pop.list()
numMessage = len(poplist[1])
popuid=pop.uidl()


# %%
