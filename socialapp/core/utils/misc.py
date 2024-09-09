from __future__ import annotations

import yaml


def yaml_coerce(value: str):
    # Convert string into proper python dict

    if isinstance(value, str):
        return yaml.load(f'dummy: {value}', Loader=yaml.SafeLoader)['dummy']

    return value
