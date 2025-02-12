class FilterModule(object):
  '''
  custom jinja merge vars Filter
  '''

  def filters(self):
    return {
      'reset_var':self.reset_var
    }

  def reset_var(self, input):
     if input is None:
        return None
     else:
        return input