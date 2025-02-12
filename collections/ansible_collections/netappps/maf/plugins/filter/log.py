class FilterModule(object):
  '''
  log to file Filter
  '''



  def filters(self):
    return {
      'do_log':self.logToFile
    }

  def logToFile(self, msg, title, name, logdir, logname):

      import yaml
      import datetime

      # if filepath not ends with .log then
      # append .log to it
      # and prepend logs/ + timestamp to it
      if logname:
          if not logname.endswith('.log'):
            fp = logdir + '/' +datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "_" + logname + '.log'
          else:
            fp = logdir + '/' + logname
            print(f"fp: {fp}")
          with open(fp, 'a', encoding='utf-8') as f:
              # write title with dashed line underlined
              if title:
                f.write('\n\n' + title + '\n')
                f.write('-' * len(title) + '\n')
              if name:
                f.write(f"{name}:\n")
              f.write(msg + '\n')
          return fp
      else:
         return ""