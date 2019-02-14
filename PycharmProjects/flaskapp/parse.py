# -*- coding:utf8 -*-
import urllib.request
import urllib.parse
import time
import json
import base64
import hashlib

#定义虚词的pos
func_words = ['c',  #连词
              'e',  #惊叹词
              'g',  #语素
              'h',  #前缀
              'k',  #后缀
              'm',  #数词
              'o',  #拟声词
              'p',  #介词
              'q',  #数量词
              'u',  #助词
              'wp', #标点
              'ws', #外来词
              'x'   #非词汇
              ]

#dependency parsing from LTP Cloud server
def get_dependency(text):
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')

    url = 'http://ltpapi.xfyun.cn/v1/dp'
    api_key = 'API KEY'
    param = {"type": "dependent"}

    x_appid = '5c3bbb85'
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    data = json.loads(result.decode('utf-8'))
    #print(data)
    dp_result = data['data']['dp']
    words = get_segment(text)
    pos = get_pos(text)

    #add id, word, pos tag
    for i in range(len(words)):
        dp_result[i]['pos'] = pos[i]
        dp_result[i]['cont'] = words[i]
        dp_result[i]['id'] = i

   # print(dp_result)

    return dp_result

def get_pos(text):
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')

    url = 'http://ltpapi.xfyun.cn/v1/pos'
    api_key = '30faed8d05958ecf8ec12faf5b680f73'
    param = {"type": "dependent"}

    x_appid = '5c3bbb85'
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()

    data = json.loads(result.decode('utf-8'))
    pos = data['data']['pos']

    return pos

def get_segment(text):
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')

    url = 'http://ltpapi.xfyun.cn/v1/cws'
    api_key = '30faed8d05958ecf8ec12faf5b680f73'
    param = {"type": "dependent"}

    x_appid = '5c3bbb85'
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()

    data = json.loads(result.decode('utf-8'))
    words = data['data']['word']

    return words

#change format from json to conll
def changetoconll(data):
    list = [0] * 10
    sentence = []

    for i in range(0, len(data)):
        temp = data[i]

        list[0] = int(temp['id'] + 1)
        list[1] = temp['cont']
        list[2] = '_'
        list[3] = temp['pos']
        list[4] = temp['pos']
        list[5] = '_'
        list[6] = int(temp['parent'] + 1)
        list[7] = temp['relate']
        list[8] = '_'
        list[9] = '_'
        sentence.append(list.copy())

    return sentence

#Fix-point dependency parsing
#delete functional words
#text type is list of dict [{}]
def fdc(data):
    func_index = []
    fdc_data = []

    for i in range(len(data)):

        element = data[i]['pos']
        if element in func_words:  # 根据pos删除虚词
            for j in range(len(data)):
                if data[j]['parent'] == data[i]['id']:
                    data[j]['parent'] = data[i]['parent']
        else:
            fdc_data.append(data[i])

    # 更新编号
    for i in range(len(fdc_data)):
        if fdc_data[i]['id'] != i:
            for j in range(len(fdc_data)):
                if fdc_data[j]['parent'] == fdc_data[i]['id']:
                    fdc_data[j]['parent'] = i
            fdc_data[i]['id'] = i

    return fdc_data

# change json data that can be used in d3
def visualize_data(text):

    data = text
    extract_data = []
    node = {}


    for i in range(len(data)):
        node["target"] = str(data[i]["id"])+", "+data[i]["cont"]+", "+data[i]["pos"]
        parent = data[i]["parent"]
        if parent == '-1':
            parent = data[i]["id"]
        for j in range(len(data)):
            if data[j]["id"] == parent:
                node["source"] = str(data[j]["id"])+", "+data[j]["cont"]+", "+data[j]["pos"]
        node["type"] = "suit"
        extract_data.append(node.copy())


    return extract_data

