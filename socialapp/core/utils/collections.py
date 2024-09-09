#Update base settings with new settings
def deep_update(base_dict: dict, update_with: dict) -> dict:

    #Iterate over each item in the new dict
    for key, value in update_with.items():

        #If the value is a dict
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)

            #If the original value is also a dict then run it through the same function
            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)

            #If the original value is not a dict then just set the new value
            else:
                base_dict[key] = value

        #If the new value is not a dict
        else:
            base_dict[key] = value

    return base_dict