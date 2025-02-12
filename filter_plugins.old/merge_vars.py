class FilterModule(object):
  '''
  custom jinja merge vars Filter
  '''

  ########################################################
  # custom merge filters
  ########################################################
  # we can merge dictionaries and lists
  # dictionaries are merged in the following order: defaults, templates, external, local, overrides
  # for dictionary merge, templates can be applied globally or locally, local wins

  # lists are not merged like dictionaries, we "add" them together, extending the list
  # for list merge, templates can be applied globally.  
  # Locally is technically not possible, because we can't add a loose property to a list, it must be a dictionary
  # however, if you use "has_template", it will assume the external object is a dictionary with a template name
  #   the external object will be ignored and not added to the list

  def filters(self):
    return {
      'merge_vars':self.merge_vars,
      'merge_lists':self.merge_lists
    }

  # merges variables
  # object_name = name of the object (volume, svm, ...)
  # d = defaults object (typically vars_defaults)
  # t = templates object (typically vars_templates)
  # v = external variables (typically vars_external or vars_local)
  # l = local object (a very specific object, typically used with a loop item and looping lists)
  # o = overrides object (typically vars_overrides)
  # s = suffix object name (typically to specify a specific object, like volume_root, volume_data,...)
  # c = child (incase the external variables are wrapped in an additional child, typically used for multi server actions)

  def merge_vars(self,object_name,d={},t={},v={},l={},o={},s='',c=None):

    # we need to merge 2 dictionaries together, source and destination, the source must be merged into the destination.  Source wins in case of conflict
    def merge(source, destination):
      '''
      merge
      '''
      for key, value in source.items():
          if isinstance(value, dict):
              merge(value, destination.setdefault(key, {}))
          else:
              destination[key] = value
      return destination

    try:

      defaults = d or {}
      templates = t or {}
      external = v or {}
      local = l or {}
      overrides = o or {}
      child = c or None
      if child:
        external = external.get(child,{})
        defaults = defaults.get(child,{})
        
      s = str(s)
      # grab the default object
      default_object         = defaults.get(object_name,{})                                                          # default values
       # grab the global template name
      template_name_global   = external.get("template","")                                                           # global template name
      # grab the local template name
      template_name_local    = local.get("template",None) or external.get(object_name+s,{}).get("template","")       # object template name (local or external, local wins)
      # grab the global template object
      template_object_global = templates.get(template_name_global,{}).get(object_name+s,{})                          # global template values
      # grab the local template object
      template_object_local  = templates.get(template_name_local,{}).get(object_name+s,{})                           # object template values
      # grab the external object
      external_object        = local or external.get(object_name+s,{})                                               # external values (local or external, local wins)
      # grab the override object
      overrides_object       = overrides.get(object_name,{})                                                         # override values

      # print ("-"*80)
      # print (f"object_name: {object_name}")
      # print (f"template_name_global: {template_name_global}")
      # print (f"template_name_local: {template_name_local}")
      # print (f"default_object: {default_object}")
      # print (f"template_object_global: {template_object_global}")
      # print (f"template_object: {template_object_local}")
      # print (f"external_object: {external_object}")
      # print (f"overrides_object: {overrides_object}")

      # now we merge 1 by 1, each time merging properties, overwrite on conflict
      step1 = merge(template_object_global,default_object) # merge global template values into default values
      step2 = merge(template_object_local,step1)           # merge object template values
      step3 = merge(external_object,step2)                 # merge external values
      step4 = merge(overrides_object,step3)                # merge override values

      # print (f"step1: {step1}")
      # print (f"step2: {step2}")
      # print (f"step3: {step3}")
      # print (f"step4: {step4}")

      return step4
    
    except Exception as e:
      print (f"Error: {e}")
      # stacktrace
      import traceback
      print (traceback.format_exc())
      return {}
  
  ###############################
  # merges lists
  ###############################
  # object_name   = name of the object (volume, svm, ...)
  # d             = defaults object (typically vars_defaults)
  # t             = templates object (typically vars_templates)
  # v             = external variables (typically vars_local => after vars_external was passed through logic)
  # l             = local object (a very specific object, already present, typically used with a loop item and looping lists)  
  # s             = suffix object name (typically to specify a specific object, like volume_root, volume_data,...)
  # c             = child (incase the external variables are wrapped in an additional child, typically used for multi host actions)
  # has_template  = this is special case where you pass a dictionary with a template name, but the default-object and template-object are lists
  # required_keys = if the object is a list, we can specify required keys that must be present in the object, otherwise the object is excluded from the list
  #                 for example you pass a list with items, but some don't have a name, then we say that the name is required, so we exclude the items without a name
  def merge_lists(self,object_name,d={},t={},v={},l=[],s='',c=None,has_template=False,required_keys=[]):
      '''
      merge_lists
      '''
      defaults = d or {}
      templates = t or {}
      external = v or {}
      local = l or []
      child = c or None
      default_object   = defaults.get(object_name+s,[])
      template_name_global  = external.get("template","")
      s=str(s)
      if child:
        external = external.get(child,{})
      
      #if the object has a template, we take the template but don't use the vars object, because it's not a list (we can't merge a list with a dict)
      if has_template:
        # we grab the template name
        template_name_local  = external.get(object_name+s,{}).get("template","")    
        # be then ignore the external object and grab directly the template object (as a list)
        external_object    = templates.get(template_name_local,{}).get(object_name+s,[])
      else:
        # we grab the external object, assuming it's a list
        external_object  = external.get(object_name+s,[])

      # we grab the global template object
      template_object_global    = templates.get(template_name_global,{}).get(object_name+s,[])

      local_object     = local
      merged_list = [*default_object,*template_object_global,*external_object,*local_object]
      # if the required keys are not in the merged list, we exclude the object from the list
      if required_keys:
        return [x for x in merged_list if all(k in x for k in required_keys)]
      else:
        return merged_list
      