---
duration: PT1H00M0S
description: Learn how to use Oracle Cloud API Gateway, Functions and Observability for monitoring API Headers and Body
level: Advanced
roles: Devops;Developer
products: en/cloud/oracle-cloud-infrastructure/oci
keywords: APIs REST/SOAP
inject-note: true
---

# Learn how to use Oracle Cloud API Gateway, Functions and Observability for monitoring API Headers and Body

## Introduction

When we develop distributed applications, especially in architectures based on microservices, we want components that scale and perform well in their execution.
They are very complex architectures, components that execute other components that execute other components in an infinite number of endless calls. 

Planning how to develop each of them is a huge task.
You can expose your microservices built on a Kubernetes cluster through the OCI API Gateway. There are a series of facilities, such as performing call authentication and authorization, data validation and call optimization, to name just a few.
There is also the possibility of executing calls with OCI Functions with the aim of creating personalized authentication and authorization mechanisms, when existing methods are not sufficient to solve the need.

This material will show how to use the custom mechanism to validate some use cases such as:

- Validate the size of JSON parameter data
- Validate the maximum number of JSON items

Despite being a mechanism for authentication and authorization in the OCI API Gateway, it could help with some other needs, such as:

- Capture data from HEADER, query parameters or the body of the REST call
- Send this data to OCI Observability with the aim of facilitating the debugging of problems, which are often impossible to detect without this information

>**Note:** Consider in your code, as a best practice, use of redaction for HEADER or BODY content, like passwords or sensitive data. Another approach could be to turn on/off your function for debugging purposes.

### Objectives

- Configure an API Deployment
- Develop an OCI Function to capture the HEADER and BODY from the API request
- Validade a body JSON data
- Send the HEADER and BODY information to OCI Observability 

### Prerequisites

- An operational Oracle Cloud tenant: You can create a free Oracle Cloud account with US$ 300.00 for a month to try this tutorial. See [Create a Free Oracle Cloud Account](https://www.oracle.com/cloud/free/).
- An OCI API Gateway instance created and exposed to the Internet. See [Creating Your First API Gateway In The Oracle Cloud](https://blogs.oracle.com/developers/post/creating-your-first-api-gateway-in-the-oracle-cloud).

## Task 1: Configure OCI Observability

![logging-1](./images/logging-1.png)
![logging-2](./images/logging-2.png)
![logging-3](./images/logging-3.png)
![logging-4](./images/logging-4.png)

## Task 2: Create an OCI Function to capture the HEADERs and BODY from API request

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
                log_id="ocid1.log.oc1.iad.cbcbdcsbcdcsdhcgshjdcgsdjhcgsdjhcgsjhghjdscsdcsdh",
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

### Understand the Code
### Configure the SDK Authentication to OCI
### Build and deploy the function

## Task 3: Configure the OCI Function in API Gateway

![config-apigw-1](./images/config-apigw-1.png)
![config-apigw-2](./images/config-apigw-2.png)
![config-apigw-3](./images/config-apigw-3.png)


### Configure the Response to show the values of HEADER and BODY

## Task 4: Test your Request

![test-1](./images/test-1.png)

## Related Links

- [OCI SDK API Reference - LoggingClient](https://docs.oracle.com/en-us/iaas/tools/python/2.115.1/api/loggingingestion/client/oci.loggingingestion.LoggingClient.html)
- [Python OCI SDK Example](https://docs.oracle.com/en-us/iaas/tools/python-sdk-examples/2.115.1/loggingingestion/put_logs.py.html)

## Acknowledgments

* **Author** - Cristiano Hoshikawa (Oracle LAD A-Team Solution Engineer)
