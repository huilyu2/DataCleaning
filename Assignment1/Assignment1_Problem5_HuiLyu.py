# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:46:17 2017

@author: HuiLyu
"""

from datetime import datetime
from datetime import date
import re

# Three types of non-standard dates:
# (0[1-9]|[1-9]|1[0-2])\/(0[1-9]|[1-9]|[12]\d|3[01])\/[12]\d{3}
# (0[1-9]|[1-9]|[12]\d|3[01])\.(0[1-9]|[1-9]|1[0-2])\.[12]\d{3}
# (January|February|March|April|May|June|July|August|September|October|November|December) (0[1-9]|[1-9]|[12]\d|3[01]), [12]\d{3}

# Assume the year of dates are from 1000 to 2999

def reformat1(string):
    match = re.search(r'(0[1-9]|[1-9]|1[0-2])\/(0[1-9]|[1-9]|[12]\d|3[01])\/([12]\d{3})', string)
    if match != None:
        month = match.group(1)
        day = match.group(2)
        year = match.group(3)
        standard_date = date(int(year), int(month), int(day)).isoformat()
        return standard_date
    else:
        return -1
        
def reformat2(string):
    match = re.search(r'(0[1-9]|[1-9]|[12]\d|3[01])\.(0[1-9]|[1-9]|1[0-2])\.([12]\d{3})', string)
    if match != None:
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)
        standard_date = date(int(year), int(month), int(day)).isoformat()
        return standard_date
    else:
        return -1
        
def reformat3(string):
    try:
        standard_date = datetime.strptime(string, '%B %d, %Y')
        return standard_date.date()
    except ValueError:
        return -1
        
def standardization():
    string = input("Please input the date:")
    result1 = reformat1(string)
    if result1 != -1:
        print("The standardized date is {}".format(result1))
    else:
        result2 = reformat2(string)
        if result2 != -1:
            print("The standardized date is {}".format(result2))
        else:
            result3 = reformat3(string)
            if result3 != -1:
                print("The standardized date is {}".format(result3))
            else:
                print("Failed to reformat. Please try again.")
            
standardization()
