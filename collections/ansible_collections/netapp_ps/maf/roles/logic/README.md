# dictu / logic

This role contains the logic for the dictu project. 
It mainly accepts 1 dictionary call vars_external and returns a dictionary that is then used as vars_internal.
It is used to complete the vars_internal dictionary with the values that are not provided by the user.
Naming conventions, data validation, data lookup, ...

## tasks

- facts_share : complete logic for share creation (required credentials : aiqum, mysql)
- facts_svm_nas : complete logic for svm creation (required credentials : aiqum)
- facts_svm_delete : complete logic for svm deletion (required credentials : none)
