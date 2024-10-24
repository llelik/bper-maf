#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

import re
import requests
import urllib3
import mysql.connector

# Disable SSL certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

summary=[]
result = {}

def validate_input(inputs):
    for i in inputs:
        for key in i:
            if not i[key]:
                raise Exception(f"Missing required parameter {key}")
            
# logging 
def log(t):
    global summary
    summary.append(t)

def get_clusters(aiqum_host, aiqum_username, aiqum_password):
    url = f"https://{aiqum_host}/api/datacenter/cluster/clusters"
    response = requests.get(url, auth=(aiqum_username, aiqum_password), verify=False)
    response_json = response.json()
    clusters = response_json.get("records", [])
    # only keep properties name & management_ip
    clusters = [{"name": cluster["name"], "management_ip": cluster["management_ip"]} for cluster in clusters]
    return clusters


# main code
def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        aiqum_host                = dict(type='str', required=True), # AIQUM IP
        aiqum_username            = dict(type='str', required=True), # AIQUM username
        aiqum_password            = dict(type='str', required=True, no_log=True), # AIQUM password
        vars_external               = dict(type='dict', required=True), # vars external dict
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # store input to vars, some are global
    global summary
    
    err = None
    # debug          = module.params['debug']
    aiqum_host               = module.params['aiqum_host']
    aiqum_username           = module.params['aiqum_username']
    aiqum_password           = module.params['aiqum_password']
    ve                       = module.params['vars_external']

    # apply logic and complete the variables
    try:

        # get share type full name
        clusters = get_clusters(aiqum_host, aiqum_username, aiqum_password)
        ve["clusters"] = clusters



    except Exception as e:
        log(repr(e))
        err = str(e)

    result["vars"] = ve
    result["summary"] = summary

    # return
    if err:
        module.fail_json(err,**result)
    else:
        module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
