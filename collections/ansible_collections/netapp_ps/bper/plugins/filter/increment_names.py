##########################################################################
#
# - increment name
# 
#
# 
# Alexey Mikhaylov
# NetApp Deutschland GmbH
# Professional Services 2024
##########################################################################
def increment_names(names, step=1):
    ''' increments names index in the list by the specified step '''
    sorted_names = sorted(names)
    for name in reversed(sorted_names):
        if name[-2:].isdigit():
            number = int(name[-2:])
            incremented_number = (number + step) % 100  # Ensure the number remains 2-digit
            incremented_name = name[:-2] + str(incremented_number).zfill(2)
            return incremented_name
    return ""

class FilterModule(object):
    def filters(self):
        return {
            'increment_names': increment_names
        }