def shorten_fus(value):
    # Check if the value starts with "FUS"
    if value.startswith("FUS"):
        # Check if the value ends with a dash followed by a digit
        if value[-2:].startswith("-") and value[-1].isdigit():
            # Return the first character 'F' and the last digit
            return "F" + value[-1]
        else:
            raise ValueError("Input does not comply with the format 'FUS-n'.")
    else:
        # Return the original value if it doesn't start with "FUS"
        return value


class FilterModule(object):
    def filters(self):
        return {
            'shorten_fus': shorten_fus
        }