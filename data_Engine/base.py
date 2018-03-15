# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:43:09 2018

@author: xinger
"""
from jaqs.data.dataapi import DataApi
from jaqs.data import DataView
from datetime import datetime, timedelta
from time import time
from WindPy import w
import pandas as pd
import numpy as np
import pymongo
import openpyxl
import os
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from abc import ABCMeta, abstractmethod
now = datetime.now()
str_now = datetime.strftime(now,'%Y%m%d')



