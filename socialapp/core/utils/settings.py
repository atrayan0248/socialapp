import os

from .misc import yaml_coerce


def get_settings_from_environment(prefix):
    #Get the length of prefix
    prefix_len = len(prefix)

    #Return a dictionary of key: value where key is the environment variable name stripped off of it's prefix
    #and value is the result of passing the value of the environment variable through the yaml_coerce function
    #in the misc.py file.
    return {key[prefix_len:]: yaml_coerce(value) for key, value in os.environ.items() if key.startswith(prefix)}