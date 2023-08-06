#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: __init__.py
# Author: cluckbird
# Mail: admin@muzmn.cn
# Created Time:  2020-11-4 7:44
#############################################

name = "winoc"

import wmi
import psutil

cpuinfo = wmi.WMI()

# Cpu Occupy info
'''
Calling this function will directly return the Int value as a percentage of CPU usage, without the percentage sign.
'''
def cpuoccupy():
    cpu_json_occupy_list = {}
    for cpu in cpuinfo.Win32_Processor():
            return int(cpu.LoadPercentage)

#Men Occupy info
'''
Return percentage of memory usage (Int type)
'''
def menoccupy():
    return int(psutil.virtual_memory().percent)

#Memory used
'''
Please bring the parameter: the decimal place (Int) you want to keep.
Returns the amount of memory used, in MB.
'''
def memoryused(keep_decimals):
    return "{:.{}f}".format((int(float(psutil.virtual_memory().used)/1024)/1024),keep_decimals)

#Occupy info json
'''
Returns a JSON with: % CPU occupied, % memory occupied, remaining memory (mb)
'''
def occupy_json():
    for cpu in cpuinfo.Win32_Processor():     
        zd = {}
        mensy = "{:.2f}".format((int(float(psutil.virtual_memory().used)/1024)/1024))
        zd["cpu"] = str(cpu.LoadPercentage)
        zd["men"] = str(psutil.virtual_memory().percent)
        zd["men_u"] = str(mensy)
        return repr(zd).replace("'",'"')

def main():
  pass

if __name__ == '__main__':
    main()