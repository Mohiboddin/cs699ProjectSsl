#!/usr/bin/python3
#

import re
import os
import shutil
import sys
import codecs
from datetime import datetime
import secrets
import string
from util import *

import pandas as pd 
import numpy as np
from os.path import exists


# ----------------------------------------------------------
# Paths and urls
# ----------------------------------------------------------

def url_prefix( dept ):


def cert_files_and_path(year, dept):


# ----------------------------------------------------------
# Utilities
# ----------------------------------------------------------


def get_expire_time(cert):
    if not os.path.exists(cert):
        return None
    cmd = [ 'openssl -noout -dates -in', cert ]
    cmd = ' '.join(cmd)
    time = os.popen(cmd).read().split('\n')[1][9:]
    tformat = '%b %d %H:%M:%S %Y %Z'
    time = datetime.strptime(time,tformat)
    return time

def get_start_time(cert):
    if not os.path.exists(cert):
        return None
    cmd = [ 'openssl  -noout -dates -in', cert ]
    cmd = ' '.join(cmd)
    time = os.popen(cmd).read().split('\n')[0][10:]
    tformat = '%b %d %H:%M:%S %Y %Z'
    time = datetime.strptime(time,tformat)
    return time

def get_expire_time_dept( year, dept ):
    _,cert_folder,_,_,cert = cert_files_and_path( year, dept)
    return get_expire_time( cert_folder + cert )

def get_start_time_dept( year, dept ):
    _,cert_folder,_,_,cert = cert_files_and_path( year, dept)
    return get_start_time( cert_folder + cert )

def print_expire_time_dept( year, dept ):
    t = get_expire_time_dept( year, dept )
    if t != None:
        print(days_left(t), dept)
    return t 

def print_start_time_dept( year, dept ):
    t = get_start_time_dept( year, dept )
    if t != None:
        print(t.date(), dept)
    return t 

# ----------------------------------------------------------
#
# Comptues private CSR KEYS
#
# ----------------------------------------------------------

def create_csr_key(folder, csr, key, cert):
    if os.path.exists( folder+'/'+csr):
        # print('csr and key files already exist!')
        return
    c_cmd = ['cd', folder, '&&'] 
    cmd = ["openssl req -new -newkey rsa: -nodes ",
           "-out", csr,
           '-keyout', key,
           '-subj',
           "\"________-------_________\""
           ]
    cmd = c_cmd + cmd
    cmd = ' '.join(cmd)
    print(cmd)
    os.system(cmd)

def create_certificate( dept ):
    prefix  = url_prefix( dept )
    year  = datetime.now().year

    key_folder,cert_folder,csr,key,cert = cert_files_and_path( year, dept)
    _,last_cert_folder,_,_,_ = cert_files_and_path( year-1, dept)

    #----------------------------------------
    # Creating private key, if does not exist
    #----------------------------------------

    t = get_expire_time( last_cert_folder+cert )
    if t != None:
        if days_left(t) > 14:
            print( '> 14 days left in certificate. Expiration date:',t.date() )
            return

    os.makedirs( key_folder,  exist_ok=True )
    os.makedirs( cert_folder, exist_ok=True )
    create_csr_key( key_folder, csr, key, cert )

    #---------------------------------------
    # Copy received certificate to the folder
    # in control repo, if does not exist
    #---------------------------------------

    t = get_expire_time( cert_folder + cert )

    if t != None:
        return

    if os.path.exists( download_dir+cert ):
        # if certificate is already saved in download_dir
        # copy it to control repo and commit
        t = get_expire_time(  cert )
        if t == 'None' or days_left(t) < 100:
            print('Bad certifcate ', cert )
            exit()
        shutil.copyfile(    )
        shutil.copyfile( )

   
# ----------------------------------------------------------
# Install certificate :
#   - TODO: Check if the certificate is already installed
# ----------------------------------------------------------

def copy_certificate( depts ):


# ----------------------------------------------------------
# Display state of website certificates
# ----------------------------------------------------------

year = datetime.now().year

print( "----------------------------------------" )
print( "Days left of managed sites:"             )
print( "----------------------------------------" )

updated = set()
for dept in depts :
    t = print_expire_time_dept( year, dept )
    if t != None :
        updated.add( dept )
print( "----------------------------------------" )
for dept in depts:
    if not dept in updated:
        t = print_expire_time_dept( year-1, dept )
        if( t == None ):
            print( "missing", dept )

 
print( "----------------------------------------" )
print( " Create pending certificates "            )
print( "----------------------------------------" )

for dept in depts:
    create_certificate( dept )




