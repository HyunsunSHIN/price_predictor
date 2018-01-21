import numpy as np
import urllib.request

def query_sender(localcode, timecode):
    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?'
    code_info = 'LAWD_CD='+ localcode + '&DEAL_YMD=' + timecode
    key = '&serviceKey=서비스키'
    request = urllib.request.Request(url+code_info+key)
    request.get_method = lambda: 'GET'
    response_body = urllib.request.urlopen(request).read()
    u = str(response_body, "utf-8")
    return u

xml_string = query_sender('11110','201612')
print(xml_string)
import xml.etree.ElementTree as ET
#from xml.etree.ElementTree import parse, Element

def xml_to_item_list(xml_string,local_name, time_code):
    result = []
    root = ET.fromstring(xml_string)
    elements = root.findall('body/items/item')
    item_list = []
    for item in elements:
        try:
            item_list = []
            item_list.append(time_code)
            item_list.append(item.find('거래금액').text)
            item_list.append(item.find('건축년도').text)
            item_list.append(local_name+" "+item.find('법정동').text+" "+item.find('지번').text)
            item_list.append(item.find('아파트').text)
            item_list.append(item.find('전용면적').text)
            result.append(item_list)
        except Exception as e:
            print(e)
            print("This row will be ignored. ",item_list)
    return result

item_list = xml_to_item_list(xml_string,'11110','201612')

from pprint import pprint
pprint(item_list)
item_numpy_list = np.array(item_list)

import pandas as pd

def numpy_to_csv(item_numpy_list):
    df = pd.DataFrame(item_numpy_list)
    df.to_csv("tmp.csv",encoding='utf-8', header = False, index = False)

def item_writer(localcode, timecode, local_name):
    xml_string = query_sender(localcode, timecode)
    item_list = xml_to_item_list(xml_string, local_name, time_code)
    item_numpy_list = np.array(item_list)
    #print(item_numpy_list)
    numpy_to_csv(item_numpy_list)

def timecode_generator(start_code, end_code):
    result = []

    start_YY = int(start_code[:4])
    start_MM = int(start_code[4:])

    end_YY = int(end_code[:4])
    end_MM = int(end_code[4:])

    tmp_MM = start_MM
    tmp_YY = start_YY

    print(end_YY * 100 + end_MM)
    print(tmp_YY * 100 + tmp_MM)

    while (tmp_YY * 100 + tmp_MM < end_YY * 100 + end_MM):
        tmp_timecode = tmp_MM + tmp_YY * 100
        # print(tmp_timecode)
        result.append(tmp_timecode)
        tmp_MM = tmp_MM + 1

        if tmp_MM >= 13:
            tmp_MM = 1
            tmp_YY = tmp_YY + 1

    return result

time_code_list = timecode_generator('200601', '200602')
local_code = '11110'
local_name = "서울특별시 종로구"

for time_code in time_code_list:
    print(time_code)
    time_code_str = str(time_code)
    path = './test'
    item_writer(local_code, time_code_str, local_name)
#이후 현재 디렉토리에 tmp.csv 파일에 데이터가 저장됨.