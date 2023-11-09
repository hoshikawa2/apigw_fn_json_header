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

When we develop distributed applications, especially in microservices architectures, we want to build APIs to scale and perform. But this architecture is very complex, many times, view the messages going from a API to another is very hard to monitor.

Effective monitoring of these API calls is essential to view the health of the application as well as debug problems and correct them.
When we talk about REST APIs, passing parameters often becomes quite complex, as they can be passed as query parameters, as headers or even in the body of the REST call.
When debugging, understanding what is happening with the execution of the API often depends on knowing more about these parameters.

This material will show how to use OCI API Gateway, OCI Functions and OCI Observability to monitor the header and body parameters of the API call message through the authorization and authentication feature.
When executing an API call, the OCI API Gateway will receive the message header and body data and, through a function, intercept this data and send it to a log within OCI Observability, thus allowing monitoring of this data in the search tool of logs.

### Objectives

- Configure an API Deployment
- Develop an OCI Function to capture the HEADER and BODY from the API request
- Send the HEADER and BODY information to OCI Observability 

### Prerequisites


## Task 1: Configure an application in Oracle Identity Cloud Service


## Related Links

## Acknowledgments

* **Author** - Cristiano Hoshikawa (Oracle LAD A-Team Solution Engineer)
