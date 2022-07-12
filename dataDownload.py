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
with open ("./config.json",'r',encoding='utf-8-sig') as f:
	d= json.load(f)
# %%
