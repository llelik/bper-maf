##########################################################################
#
# - convert input FUSn to Fn
# 
# NOTE: the logic of input data that supposed to be passed into this filter has changed.
#       This means that the input will always be bypased by this filter.
#
# 
# Alexey Mikhaylov
# NetApp Deutschland GmbH
# Professional Services 2024
##########################################################################
def shorten_fus(value):
    ''' Shorten the FUS name to the format Fn. '''
    value_upper = value.upper()

    # Check if the value starts with "FUS"
    if value_upper.startswith("FUS"):
        # Check if the value ends with a dash followed by a digit
        if value_upper[-2:].startswith("-") and value_upper[-1].isdigit():
                      
            # Return the first character 'F' and the last digit
            return "F" + value_upper[-1]
        else:
            raise ValueError("Input does not comply with the format 'FUS-n'.")
    else:
        # Return the original value if it doesn't start with "FUS"
        return value_upper


class FilterModule(object):
    ''' Ansible filters. '''
    def filters(self):
        return {
            'shorten_fus': shorten_fus
        }