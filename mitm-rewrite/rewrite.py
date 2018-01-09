import os
import sys
import json
import yaml
from mitmproxy import http

HOME_DIR = './'
DATA_DIR = HOME_DIR + 'response/'
ROUTER_FILE = HOME_DIR + 'router.yaml'

def readFile(file):
    """Read file and return json data or dict

    Read file and return all its content as json format or dict

    Arg:
        file: File name, including its path
    """

    if not os.path.isfile(file):
        print("File: " + file + ' not found!')
        sys.exit(1)

    fname, fext = os.path.splitext(file)

    with open(file) as data:
        if fext == ".yaml":
            return yaml.load(data)
        else:
            return json.load(data)

def request(flow: http.HTTPFlow) -> None:
    """Mock response

    If URL corresponds to router.yaml, use matched json file as response
    Link url and json file in router.yaml

    Arg:
        flow: http flow, fom mitm
    """

    router = readFile(ROUTER_FILE)
    url = flow.request.url

    if url in router:
        jsonfile = DATA_DIR + str(router[url]) + '.json'
        print(url + ' found. Send data from "' + jsonfile + '"')

        data = readFile(jsonfile)

        status = int(data['status'])
        try:
            content = json.dumps(data['content'])
        except:
            content = ''
        header = data['header']

        flow.response = http.HTTPResponse.make(status, content, header)