import azure.functions as func
import datetime
import json
import logging
import requests
from requests_toolbelt.adapters import host_header_ssl
from urllib.parse import urlparse

target = "https://TARGETHOST:TARGETPORT"
hostname = "host_in_cert"
key = "s3cr3tk3y"

## END of user config data

app = func.FunctionApp()

def merge_two_dicts(x, y):
    logging.info(x)
    return x | y

def set_header():
    headers = {'X-Key': key, 'host': hostname}
    return headers

@app.function_name(name="ProxyTrigger1")
@app.route(route="{*restOfPath}", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    url = target + urlparse(req.url).path
    
    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())

    if req.method == "GET":
        resp = s.get(url, params=req.params, headers=merge_two_dicts(dict(req.headers), set_header()), allow_redirects=False, verify="ssl.crt")
        return func.HttpResponse(body=resp.content, status_code=resp.status_code, mimetype=resp.headers['content-type'])
    elif req.method == "POST":
        resp = s.post(url, params=req.params, data=req.get_body(), headers=merge_two_dicts(dict(req.headers), set_header()), allow_redirects=False, verify="ssl.crt")
        if 'content-type' in resp.headers:
            return func.HttpResponse(body=resp.content, status_code=resp.status_code, mimetype=resp.headers['content-type'])
        else:
            return func.HttpResponse(body=resp.content, status_code=resp.status_code, headers=resp.headers)
    else:
        return func.HttpResponse("Method not supported.", status_code=200)
