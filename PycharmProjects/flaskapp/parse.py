# -*- coding:utf8 -*-
import urllib.request
import urllib.parse
from urllib.parse import quote
import json

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
def get_dependency(text, textformat):
    url_get_base = "http://api.ltp-cloud.com/analysis/"

    args = {
        'api_key': '61Y2D2r7g93Z8PxmzNpL5HQTPysLJCSNSC9hcznI',
        'text': quote(text),
        'pattern': 'dp',
        'format': textformat
    }

    args = urllib.parse.urlencode(args).encode('utf-8')
    req = urllib.request.Request(url_get_base)
    result = urllib.request.urlopen(req, data=args)  # POST method
    content = result.read()

    return content.decode()

#change format from conll to json
def changetojson(conlltext):
    data = conlltext
    list = {}
    text = []
    result = [[[]]]

    for i in range(0, len(data)):
        temp = data[i]

        list["id"] = temp[0]
        list["cont"] = temp[1]
        list["pos"] = temp[4]
        list["parent"] = temp[6]
        list["relate"] = temp[7]
        text.append(list.copy())

    result[0][0]=text
    result = json.dumps(result,ensure_ascii=False)

    return result

#Fix-point dependency parsing
#delete functional words
def fdc(text, textformat):
    fdc_data = [[[]]]
    func_index = []

    if textformat == "conll":
        words = list(text)

        for i in range(len(words)):
            if words[i][4] in func_words:  # pos位置
                func_index.append(i)  # 记录虚词在原句中的位置
                parent = words[i][6]  # parent node编号
                for j in range(len(words)):
                    if words[j][6] == words[i][0]:  # 是否有子节点
                        words[j][6] = parent
        # 删除虚词
        func_index.reverse()
        for i in range(len(func_index)):
            words.pop(func_index[i])

        fdc_data[0][0] = words

    else:
        data = json.loads(text)
        data = data[0][0]

        for i in range(len(data)):
            element = data[i]["pos"]
            if element in func_words:  #根据pos删除虚词
                for j in range(len(data)):
                    if data[j]["parent"] == data[i]["id"]:
                        data[j]["parent"] = data[i]["parent"]
            else:
                func_index.append(i)

        for i in range(len(data)):
            if i in func_index:
                fdc_data[0][0].append(data[i])

    return fdc_data

# change json data that can be used in d3
def visualize_data(text):
    # data = json.loads(text)
    data = text[0][0]
    extract_data = []
    node = {}

    for i in range(len(data)):
        node["target"] = data[i]["cont"]
        parent = data[i]["parent"]
        if parent == '-1':
            parent = data[i]["id"]
        for j in range(len(data)):
            if data[j]["id"] == parent:
                node["source"] = data[j]["cont"]
        node["type"] = "suit"
        extract_data.append(node.copy())

    return extract_data

#
# content = '''[[['0', '他', '_', '_', 'r', '_', '3', 'SBV', '_', '_', '_'], ['1', '把', '_', '_', 'p', '_', '3', 'ADV', '_', '_', '_'], ['2', '苹果', '_', '_', 'n', '_', '1', 'POB', '_', '_', '_'], ['3', '吃', '_', '_', 'v', '_', '-1', 'HED', '_', '_', '_'], ['4', '了', '_', '_', 'u', '_', '3', 'RAD', '_', '_', '_'], ['5', '。', '_', '_', 'wp', '_', '3', 'WP', '_', '_', '_']]]'''
# print(fdc(content,"conll"))
# text = changetojson(content)
# # # text = '''[ [ [ { "id": 0, "cont": "他", "pos": "r", "parent": 3, "relate": "SBV" }, { "id": 1, "cont": "把", "pos": "p", "parent": 3, "relate": "ADV" }, { "id": 2, "cont": "苹果", "pos": "n", "parent": 1, "relate": "POB" }, { "id": 3, "cont": "吃", "pos": "v", "parent": -1, "relate": "HED" }, { "id": 4, "cont": "了", "pos": "u", "parent": 3, "relate": "RAD" }, { "id": 5, "cont": "。", "pos": "wp", "parent": 3, "relate": "WP" } ] ] ]'''
# print(text)
# print(visualize_data(text))
