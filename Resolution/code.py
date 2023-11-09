import io
import json

from fdk import response


def handler(ctx, data: io.BytesIO = None):
    rdata = json.dumps({
        "active": True,
        "context": {
            "requestbody": data.getvalue().decode('utf-8'),
        },
    })
    return response.Response(
        ctx, response_data=rdata,
        status_code=200,
        headers={"Content-Type": "application/json"}
    )