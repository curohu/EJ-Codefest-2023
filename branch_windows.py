#!/usr/bin/env python
##############################################################################################################################################
# Name:      branch_windows.py
# Created by:  TaCoya Harris, Rick Wallen 
# Created:       2023-01-26
# Last Modified: 2023-01-27
# Description:
#
#
# Schedule:
# LOG:
#    2023-01-26   #######   rww     Initial Creation of script
#    2023-01-26.  #######   rww     Commented out standard deviation and altered threshold to use k=2 to better detect anomalies
#    
#    
#    
#    
##############################################################################################################################################
import sys,os;
import platform, os, time, subprocess, json, math
import pandas as pd
import numpy as np

#PATHS
db_loc ="./"
data_path="./"
#CSV LOCATIONS
# br_csv = "{0}branch_metrics.csv".format(db_loc)
br_csv = "{0}branch_metrics2.csv".format(db_loc)
br_threshold_csv = "{0}branch_thresholds.csv".format(db_loc)
# br_threshold_xk_csv = "{0}branch_thresholds_multiply.csv".format(db_loc)
# br_std_csv = "{0}branch_std".format(db_loc)
#VARIABLES
k = 2
weight = 1
########################################################################
# DATA READ SECTION
########################################################################
#BRANCH DATA READ CSV FILE
br_ls = pd.read_csv(br_csv, index_col=0, low_memory=False)

#CALCULATE MEAN
br_mean = br_ls.ewm(weight).mean()
# #CALCULATE STANDARD DEVIATION
# br_std = br_ls.ewm(weight).std()
# br_std.to_csv(br_std_csv,index=True)
# print br_std.head(10)
# print br_std.mul(k).head(10)

#CALCULATE THRESHOLD (ADDING CONSTANT)
br_threshold_k = br_mean.add(k)
print (br_threshold_k)
br_threshold_k.to_csv(br_threshold_csv,index=True)

#CALCULATE THRESHOLD (MULTIPLYING CONSTANT TO STANDARD DEVIATION)
# br_threshold_xk = br_mean.add(br_std.mul(k), fill_value=0)
# print br_threshold_xk
# br_threshold_xk.to_csv(br_threshold_xk_csv,index=True)

# newdf = br_threshold_xk
# newdf['Branch'] = '4873'
# print newdf['Branch']
# newdf = [newdf['4873'], newdf['Branch']]
# print newdf
