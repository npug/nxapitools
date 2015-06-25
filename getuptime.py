#!/usr/bin/env python2

__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

import argparse
import getpass

parser = argparse.ArgumentParser()
parser.add_argument('-ip', '--ipaddress', help='IP address of switch', required=True)
parser.add_argument('-user', '--user', help='Username', required=True)
parser.add_argument('-pass', '--password', help='Password', required=False)

args = parser.parse_args()

if args.password == None:
    args.password = getpass.getpass()

import requests
import json

"""
Modify these please
"""
url='http://%s/ins' % args.ipaddress
switchuser=args.user
switchpassword=args.password

myheaders={'content-type':'application/json'}
payload={
  "ins_api": {
    "version": "1.0",
    "type": "cli_show",
    "chunk": "0",
    "sid": "1",
    "input": "show ver",
    "output_format": "json"
  }
}
response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
response_body = response['ins_api']['outputs']['output']['body']

days = response_body['kern_uptm_days']
hrs = response_body['kern_uptm_hrs']
mins = response_body['kern_uptm_mins']
secs = response_body['kern_uptm_secs']
version = response_body['kickstart_ver_str']
hostname = response_body['host_name']

print('%s is running %s and has been up for %s days, %s hours, %s mins, %s secs') % (hostname, version, days, hrs, mins, secs)