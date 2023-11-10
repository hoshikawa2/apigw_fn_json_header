import io
import json
import logging
import requests
import oci

from fdk import response
from datetime import timedelta

def count_items(dictData):
    counting = 0
    for item in dictData:
        if type(dictData[item]) == list:
            counting += len(dictData[item])
        else:
            if not type(dictData[item]) == str:
                counting += count_items(dictData[item])
    return counting

def handler(ctx, data: io.BytesIO = None):
    jsonData = "API Error"
    c = 0
    try:
        config = oci.config.from_file("./config","DEFAULT")
        logging = oci.loggingingestion.LoggingClient(config)
        rdata = json.dumps({
            "active": True,
            "context": {
                "requestheader": data.getvalue().decode('utf-8'),
            },
        })

        jsonData = data.getvalue().decode('utf-8')
        # Get the body content from the API request
        body = dict(json.loads(data.getvalue().decode('utf-8')).get("data"))["body"]
        body = dict(json.loads(body))
        # Count the number of items on arrays inside the JSON body
        c = count_items(body)

        # If JSON body content has more than 1 item in arrays, block the authorization for the API backend
        if (c > 1):
            # Send a log to observability with out of limit of items in array
            put_logs_response = logging.put_logs(
                log_id="ocid1.log.oc1.iad.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                put_logs_details=oci.loggingingestion.models.PutLogsDetails(
                    specversion="EXAMPLE-specversion-Value",
                    log_entry_batches=[
                        oci.loggingingestion.models.LogEntryBatch(
                            entries=[
                                oci.loggingingestion.models.LogEntry(
                                    data="out of limit of items in array " + str(c),
                                    id="ocid1.test.oc1..00000001.EXAMPLE-id-Value")],
                            source="EXAMPLE-source-Value",
                            type="EXAMPLE-type-Value")]))

            return response.Response(
                ctx,
                status_code=401,
                response_data=json.dumps({"active": False, "wwwAuthenticate": "API Gateway JSON"})
            )

        # Send a log to observability with HEADERs and BODY content
        put_logs_response = logging.put_logs(
            log_id="ocid1.log.oc1.iad.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            put_logs_details=oci.loggingingestion.models.PutLogsDetails(
                specversion="EXAMPLE-specversion-Value",
                log_entry_batches=[
                    oci.loggingingestion.models.LogEntryBatch(
                        entries=[
                            oci.loggingingestion.models.LogEntry(
                                data=jsonData,
                                id="ocid1.test.oc1..00000001.EXAMPLE-id-Value")],
                        source="EXAMPLE-source-Value",
                        type="EXAMPLE-type-Value")]))

        return response.Response(
            ctx, response_data=rdata,
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    except(Exception) as ex:
        jsonData = 'error parsing json payload: ' + str(ex) + ", " + json.dumps(jsonData)
        pass

    return response.Response(
        ctx,
        status_code=401,
        response_data=json.dumps({"active": False, "wwwAuthenticate": jsonData})
    )