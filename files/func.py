import io
import json
import logging
import datetime
import requests
import base64
import oci

from datetime import timedelta
from fdk import response

def handler(ctx, data: io.BytesIO = None):
    jsonData = "API Error"
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

        #envia os logs via oci sdk
        put_logs_response = logging.put_logs(
            log_id="ocid1.log.oc1.iad.amaaaaaaihuwreyaminpecs5omqm5ug2rcekhuce4pndhaaqxdrw3rxtwria",
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