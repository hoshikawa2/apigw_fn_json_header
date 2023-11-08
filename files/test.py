import io
import json

def conta_items(dictData):
    contagem = 0
    for item in dictData:
        if type(dictData[item]) == list:
            contagem += len(dictData[item])
        else:
            if not type(dictData[item]) == str:
                contagem += conta_items(dictData[item])
    return contagem

jsonData = dict(json.loads('{"data": {"clientID": "e3e5160e2f584e52a0ffb9fa4785fc2f", "teste": [1, 2, 3, 4], "secretID": "8ed5582d-fa5e-49cf-806c-f793927b0687", "jList":[{"added_by":"Ani","description":"example description.","start_date":"2014-10-10","mark":255,"id":975}, {"added_by":"Ani","description":"example description.","start_date":"2014-10-10","mark":255,"id":975}, {"added_by":"Ani","description":"example description.","start_date":"2014-10-10","mark":255,"id":975}]}}'))
c = conta_items(jsonData)

print(c)