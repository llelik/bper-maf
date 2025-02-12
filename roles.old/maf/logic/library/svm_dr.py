#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

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

# main code
def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        # debug                     = dict(type='bool', required=False, default=False),
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
    ve             = module.params['vars_external']
    source         = ve.get("source", None)
    destination    = ve.get("destination", None)

     # apply logic
    try:

        # validate input
        validate_input([source, destination])

        # template
        source["template"] = "nas_nfs"
        destination["template"] = "svm_dr"

        # create cluster peer object
        cluster_peer = []
        source_cluster = source["cluster"]
        source_cluster["intercluster_ips"] = source["cluster"]["management_ip"].replace(".16.", ".19.")
        cluster_peer.append(source_cluster)
        destination_cluster = destination["cluster"]
        destination_cluster["intercluster_ips"] = destination["cluster"]["management_ip"].replace(".16.", ".19.")
        cluster_peer.append(destination_cluster)

        # complete svm lifs
        source_svm = source["svm"]     
        if source_svm.get("lifs", None):   
            source_svm["lifs"][0]["node"] = f"{source_cluster['name']}-01" # set node name

        # complete volumes
        source_volumes = source.get("volumes", [])
        # loop over volumes
        for volume in source_volumes:
            volume["junction_path"] = f"/{volume['name']}"

        # set destination svm
        destination_svm = {
            "name" : f"{source_svm['name']}_dr"
        }
        destination["svm"] = destination_svm    

        # vserver peer
        vserver_peer = []
        peer_source_svm = {
            "cluster": {
                "name": source_cluster["name"],
                "management_ip": source_cluster["management_ip"]
            },
            "svm": {
                "name": source_svm["name"]
            }
        }
        peer_destination_svm = {
            "cluster": {
                "name": destination_cluster["name"],
                "management_ip": destination_cluster["management_ip"]
            },
            "svm": {
                "name": destination_svm["name"]
            }
        }
        vserver_peer.append(peer_source_svm)
        vserver_peer.append(peer_destination_svm)

        # set snapmirror
        snapmirror = {
            "source": {
                "svm": {
                    "name": source_svm["name"]
                },
                "cluster": {
                    "name": source_cluster["name"],
                    "management_ip": source_cluster["management_ip"]
                },
            },
            "destination": {
                "svm": {
                    "name": destination_svm["name"]
                },
                "cluster": {
                    "name": destination_cluster["name"],
                    "management_ip": destination_cluster["management_ip"]
                },
            },
            "identity_preserve": "full"
        }

        # set clusters (for delete)
        clusters = []
        clusters.append(source_cluster)
        clusters.append(destination_cluster)

        source["clusters"] = clusters
        destination["clusters"] = clusters
        ve["snapmirror"] = snapmirror
        ve["vserver_peer"] = vserver_peer
        ve["cluster_peer"] = cluster_peer     

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
