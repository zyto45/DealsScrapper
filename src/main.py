import json
import requests
from jsonpath_ng import jsonpath, parse
from typing import List

f = open("config.cfg", "r")
config_json = json.loads(f.read())
config = []
pass_map = {}


class Details:
    def __init__(self, name, selector, label):
        self.name = name
        self.selector = selector
        self.label = label


class Config:
    def __init__(self, mode, url, params: List[Details], outputs: List[Details]):
        # self.label = label
        self.mode = mode
        self.url = url
        self.params = params
        self.outputs = outputs


for el in config_json.items():
    for p in el[1]:
        config.append(Config(**p))

    for c in config:
        url = c.url
        for p in c.params:
            url.replace(p['name'], pass_map[p['name']])

        data = requests.get(c.url)
        data_json = data.json()

        for o in c.outputs:
            jsonpath_expression = parse(o['selector'])
            pass_map[o['name']] = jsonpath_expression.find(data_json)

URL = config[1]["url"]
res = {}
for market in []:
    print(market.value)
    data = requests.get(URL.format(market.value, config[1]["params"][1]["value"]))
    data_json = data.json()
    jsonpath_expression = parse('$.products.*.price')
    xxx = jsonpath_expression.find(data_json)
    for r in xxx:
        if r.context.path.fields[0] in res:
            if res[r.context.path.fields[0]][1] > float(r.value):
                res[r.context.path.fields[0]] = (market.value, float(r.value))
        else:
            res[r.context.path.fields[0]] = (market.value, float(r.value))

print(res)
