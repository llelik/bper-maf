# filter_plugins/iso8601_duration_filter.py

import re

def is_duration(value):
    ''' Check if the value is a valid ISO8601 duration or is one of the special values '''
    if value.lower() in ['none', 'unspecified', 'infinite']:
        return True
    
    value = value.upper()  # Convert duration input to uppercase
    pattern = r'^P((\d+Y)?(\d+M)?(\d+W)?(\d+D)?)?(T(\d+H)?(\d+M)?)?$'
    return bool(re.match(pattern, value))

class FilterModule(object):
    ''' Custom Jinja2 filters for working with ISO8601 durations '''
    def filters(self):
        return {
            'is_duration': is_duration
        }