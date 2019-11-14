
from bs4 import BeautifulSoup
import urllib.request
import re
from ipaddress import ip_address
import os


ip_list={}
def is_ping(ips='127.0.0.1', location=''):
    #首先判断存活性
    i=0
    for a_ip in ips:
        while os.system('ping -n 2 -w 1 '+a_ip) == 0:
            print(a_ip+'is the'+location+'ip_addres')
            ip_list[loction]=a_ip
            break
        if i == 20:
            break
        i=i+1
#寻找IP地址        
def findIPs(start, end, area):
    start = ip_address(start)
    end = ip_address(end)
    result = []
    while start <= end:
            result.append(str(start))
            start += 1
    is_ping(result, area)

def ip_get(location="BJ"):
    #如果是网址，可以用这个办法来读取网页
    print(location)
    html_doc = 'http://ips.chacuo.net/view/s_'+location
    req = urllib.request.Request(html_doc)
    webpage = urllib.request.urlopen(req)
    html = webpage.read()
    soup = BeautifulSoup(html, 'html.parser')
    ips=[]
    for l in soup.find_all('dd'):
        ips.append(re.findall('[\d\.]+',str(l)))
        for ip in ips:
            findIPs(ip[0],ip[1], location)
    print(ips)
   
area=['BJ','GD','SD','ZJ','JS','SH','LN','SC','HA','HB','FJ','HN','HE','CQ','SX','JX','SN','AH','HL','GX','JL','YN','TJ','NM',
      'XJ','GS','GZ','HN','NX','XZ']
for loction in area:
    ip_get(loction)
