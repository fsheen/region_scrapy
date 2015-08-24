# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:16:33 2015

@author: Sheen
"""

import urllib
import re
import csv
#import codecs


#读取地市网页代码
main_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/'
year ='2013'
province='33'
city =  '3309'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

#读取网页内容
def url_content (url,head):
    url_request = urllib.request.Request(url,headers=head)
    url_response = urllib.request.urlopen(url_request)
    url_content = url_response.read().decode('gbk')
    return url_content
#创建行政区划字典（url对应区划名称）
def region_dic (pname,purl,content):
    region_name=re.findall(pname,content)
    region=re.findall(purl,content)
    region_url=sorted(set(region),key=region.index)
    region_dic=dict(zip(region_url, region_name))
    return region_dic
    
#省份页面下内容
prov_url = main_url +year+'/'+ province +'.html'
prov_content = url_content(prov_url,headers)
#各级名称规则
name_pattern = re.compile('[\u4e00-\u9fa5]+(?=</a>)',re.S)
village_pattern = re.compile('(?<=<td>\d{12}</td><td>\d{3}</td><td>)[\u4e00-\u9fa5]+(?=</td>.*?</tr>)',re.S)
city_url_pattern = re.compile('\d{2}/\d{4}.html',re.S)
county_url_pattern = re.compile('\d{2}/\d{6}.html',re.S)
town_url_pattern =  re.compile('\d{2}/\d{9}.html',re.S)

#地市名及url
city_dic=region_dic(name_pattern,city_url_pattern,prov_content)

dict_slice = lambda adict, start, end: { k:adict[k] for k in list(adict.keys())[start:end] }
city_dic2 = dict_slice(city_dic,1,8)
print(city_dic2)

reg_add_list=[]
for (url,city) in city_dic2.items():
    city_url = main_url +year+'/' + url
    city_num=url[5:7]
    city_content = url_content(city_url,headers)
    #区县名及url
    county_dic=region_dic(name_pattern,county_url_pattern,city_content)

    for (url,county) in county_dic.items():
        county_url=main_url +year+'/'+ province +'/' + url   
        county_content = url_content(county_url,headers)
        town_dic=region_dic(name_pattern,town_url_pattern,county_content)

        for (url,town) in town_dic.items():          
            town_url= main_url +year+'/'+ province +'/'+city_num+'/' +url
            town_content = url_content(town_url,headers)
            village_name=re.findall(village_pattern,town_content)
            
            for village in village_name:
                reg_address = [city,county,town,village]
                reg_add_list=reg_add_list+[reg_address]
    

                
first_line = ['city_name','county_name','town_name','village_name']   
     
with open('/Users/Sheen/Desktop/REGION_TREE.csv','w',newline='',encoding='utf-8') as csvfile:
 
     writer = csv.writer(csvfile,dialect='excel')
 #   writer.write('\xEF\xBB\xBF')
     writer.writerow(first_line)
     for s in reg_add_list:
         writer.writerow(s)