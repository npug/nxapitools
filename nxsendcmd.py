#!/usr/bin/env python

__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

import argparse
import yaml
import requests
import json



##gather command to push
parser = argparse.ArgumentParser(description="Input Command")
parser.add_argument('-c', '--config', help='Configuration', required=False)
parser.add_argument('-s', '--show', help='Show Command', required=False)
parser.add_argument('-l', '--lab', help='Lab File', required=True)
args = parser.parse_args()
cmdlist = ""
if args.config != None:
    cmd = args.config
    type = "cli_conf"

else:
    cmd = args.show
    type = "cli_show_ascii"

if len(cmd.split(";")) == 1:
    cmdcount = "single"
else:
    cmdcount = "multi"


#Open and read config file
file = open(args.lab, 'r')
devicelist = yaml.load(file)
file.close()

myheaders={'content-type':'application/json'}


for x in devicelist['lab']:
    #print(devicelist['lab'][x]['hostname'])
    hostname = devicelist['lab'][x]['hostname']
    ip = devicelist['lab'][x]['ip']
    username = devicelist['lab'][x]['user']
    password = devicelist['lab'][x]['pass']
    url='http://%s/ins' % ip
    payload={
      "ins_api": {
        "version": "1.0",
        "type": type,
        "chunk": "0",
        "sid": "1",
        "input": cmd,
        "output_format": "json"
      }
    }
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(username,password)).json()


###Display Information####
    if (cmdcount == "single"):
        msg = response['ins_api']['outputs']['output']['msg']
        body = response['ins_api']['outputs']['output']['body']
        if type == "cli_show":
            print(body)
        if cmd == "cli_conf":
            print('{0:12} {1:1} {2:7}'.format(hostname, ":", msg))
        else:
            print("|===Printing Output from %s===|" % hostname)
            print(body)
    else:
        count = 0
        #print(response['ins_api']['outputs']['output'])
        for x in response['ins_api']['outputs']['output']:
            print('{0:12} {1:1} {2:15} {3:1} {4:7}'.format(hostname,":",cmd.split(";")[count], ":", x['msg']))
            count = count + 1