# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:16:33 2015

@author: Sheen
"""

import urllib
import re
import csv
import codecs


#读取地市网页代码
year ='2013'
province='33'
city =  '3309'
city_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/'+year+'/'+ province +'/' + city +'.html'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

city_request = urllib.request.Request(city_url,headers=headers)
city_response = urllib.request.urlopen(city_request)
city_content = city_response.read().decode('gbk')
name_pattern = re.compile('[\u4e00-\u9fa5]+(?=</a>)',re.S)
village_pattern = re.compile('(?<=<td>\d{12}</td><td>\d{3}</td><td>)[\u4e00-\u9fa5]+(?=</td>.*?</tr>)',re.S)
county_url_pattern = re.compile('\d{2}/\d{6}.html',re.S)
town_url_pattern =  re.compile('\d{2}/\d{9}.html',re.S)

county_name=re.findall(name_pattern,city_content)
county1=re.findall(county_url_pattern,city_content)
county_url_l=sorted(set(county1),key=county1.index)

#保存URL及区县名称为字典
county_dic=dict(zip(county_url_l, county_name))

reg_add_list=[]

for (url,county) in county_dic.items():
    county_url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+ province +'/' + url
    county_request = urllib.request.Request(county_url,headers=headers)
    county_response = urllib.request.urlopen(county_request)
    county_content = county_response.read().decode('gbk')
    town_name=re.findall(name_pattern,county_content)
    town1=re.findall(town_url_pattern,county_content)
    town_url_l=sorted(set(town1),key=town1.index)

    town_dic=dict(zip(town_url_l, town_name))


    for (url,town) in town_dic.items():
        town_url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+ province +'/09/' +url
        town_request = urllib.request.Request(town_url,headers=headers)
        town_response = urllib.request.urlopen(town_request)
        town_content = town_response.read().decode('gbk')
        village_name=re.findall(village_pattern,town_content)
        for village in village_name:
            reg_address = [county,town,village]
            reg_add_list=reg_add_list+[reg_address]
#print (reg_add_list)

headers = ['县市','乡镇','村']   
     
with open('/Users/Sheen/Desktop/qh.csv','w',newline='',encoding='utf-8') as csvfile:
 
     writer = csv.writer(csvfile,dialect='excel')
 #    writer.write('\xEF\xBB\xBF')
     writer.writerow(headers)
     for s in reg_add_list:
         writer.writerow(s)