<img src=docs/netapp-footer-logo.png>
# DOCUMENTATION
## MAF implementation for BPER Services ScpA

## *Contents:*
1. ### MAF
2. ### Automation task
3. ### Requirements
4. ### Execution environment
5. ### Ansible playbook operations
   1. #### Roles
   2. #### Inventory
   3. #### Credentials
   4. #### Input values
   5. #### Data structure
   6. #### Default values
   7. #### Name generation
   8. #### Logging
   9. #### Dryrun
6. ### Play workflow
   1. #### Collect data
   2. #### Create export policy
   3. #### Create source volume
   4. #### Create qtree
   5. #### Create destination volume
   6. #### Create Snapmirror
   7. #### Rollback
7. ### Authors and contacts
 


1. # MAF
## MAF is a collection of Ansible roles, modules, filters.

Roles can be defined by function they serve:
- Manipulate with ONTAP resources
- Implement logic that allows decision making on ONTAP resources
- Manupulating with data
- Other applications comminucation
- Any other functionality that Ansible provides
Data structure it uses is mimicing ONTAP REST API structure.

ONTAP related roles implement the following operations with objects:
- Create
- Modify parameters
- Delete
- Manupilate (Ex: vol move, vol efficiency start etc.)

Logic operations may include: 
- Implement corner cases
- Prepare values based on other values

Custom Ansible modules allow to implement functionality unique to the environment it operates in.
Custom modules allow to fine tune the behavior to the task requiremnts.
Ex.: custom module for identifying best aggregate candidate for the new volume basing on multiple values and exceptions.

Custom filters allow data manipulation and are useful with naming convention, logging and data manupulation.

2. # Automation task
Playbook name: bper_vol_qtree_create.yml

Task:
1. Create a single volume with 1 qtree on primary Metrocluster (MCC) ONTAP system 
2. Volume name must be unique across MCC environment
3. Qtree must be exported via NFS to the given network
4. Once primary volume is created - secondary volume must be created as SnapMirror destination for vaulting purposes
5. SnapMirror relationship must be established

  