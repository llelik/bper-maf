import datetime

class FilterModule(object):

  
  '''
  custom jinja merge vars Filter
  '''

  def filters(self):
    return {
      'reformat_datetime':self.reformat_datetime,
      'diff_datetime':self.diff_datetime,
      'add_time_to_datetime': self.add_time_to_datetime
    }

  
  def reformat_datetime(self, input, input_format='%Y-%m-%d %H:%M:%S', output_format='%Y-%m-%d %H:%M:%S'):

      dt=None
      if not input:
        dt=datetime.datetime.now()
      else:
        dt = datetime.datetime.strptime(input, input_format)
      return dt.strftime(output_format)

  def diff_datetime(self, input, date_format='%Y-%m-%d %H:%M:%S', date2=None, date2_format='%Y-%m-%d %H:%M:%S', invert=False):
    dt1 = datetime.datetime.strptime(input, date_format)
    dt2 = None
    if not date2:
      dt2=datetime.datetime.now()
    else:
      dt2 = datetime.datetime.strptime(date2, date2_format)
    # lets return an object of as much info we can compare
    # diff in seconds,minutes,hours,days,weeks,months,years
    
    if invert:
      dt1, dt2 = dt2, dt1
      
    diff = dt2 - dt1
    diff_seconds = diff.total_seconds()
    diff_minutes = diff_seconds / 60
    diff_hours = diff_minutes / 60
    diff_days = diff_hours / 24
    diff_weeks = diff_days / 7
    diff_months = diff_days / 30
    diff_years = diff_days / 365

    return {
        "seconds": diff_seconds,
        "minutes": diff_minutes,
        "hours": diff_hours,
        "days": diff_days,
        "weeks": diff_weeks,
        "months": diff_months,
        "years": diff_years,
    }

  def add_time_to_datetime(self, input, date_format='%Y-%m-%d %H:%M:%S', add_time=0, add_type='seconds'):
    dt = None
    add_time = int(add_time)
    if not input:
      dt = datetime.datetime.now()
    else:
      dt = datetime.datetime.strptime(input, date_format)
    if add_type == 'seconds':
        dt = dt + datetime.timedelta(seconds=add_time)
    elif add_type == 'minutes':
        dt = dt + datetime.timedelta(minutes=add_time)
    elif add_type == 'hours':
        dt = dt + datetime.timedelta(hours=add_time)
    elif add_type == 'days':
        dt = dt + datetime.timedelta(days=add_time)
    elif add_type == 'weeks':
        dt = dt + datetime.timedelta(weeks=add_time)
    elif add_type == 'months':
        dt = dt + datetime.timedelta(days=add_time*30)
    elif add_type == 'years':
        dt = dt + datetime.timedelta(days=add_time*365)
    return dt.strftime(date_format)