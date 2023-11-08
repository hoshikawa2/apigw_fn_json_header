import io
import json
import logging
import datetime

from datetime import timedelta
from fdk import response

def conta_items(dictData):
    contagem = 0
    for item in dictData:
        if type(dictData[item]) == list:
            contagem += len(dictData[item])
        else:
            if not type(dictData[item]) == str:
                contagem += conta_items(dictData[item])
    return contagem

def handler(ctx, data: io.BytesIO = None):
    jsonData = "API Error"
    try:
        c = 0
        errLine = 0
        rdata = json.dumps({
            "active": True,
            "context": {
                "requestbody": data.getvalue().decode('utf-8'),
            },
        })

        errLine = 1

        jsonData = dict(json.loads(data.getvalue().decode('utf-8')).get("data"))["body"]
        jsonData = dict(json.loads(jsonData))
        errLine = 2

        c = conta_items(jsonData)

        errLine = 3

        if (c > 1):
            return response.Response(
                ctx,
                status_code=401,
                response_data=json.dumps({"active": False, "wwwAuthenticate": "API Gateway JSON"})
            )

        return response.Response(
            ctx, response_data=rdata,
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    except(Exception) as ex:
        jsonData = 'error parsing json payload: ' + str(ex) + ", " + json.dumps(jsonData) + ", " + str(errLine)
        pass

    return response.Response(
        ctx,
        status_code=401,
        response_data=json.dumps({"active": False, "wwwAuthenticate": jsonData})
    )
