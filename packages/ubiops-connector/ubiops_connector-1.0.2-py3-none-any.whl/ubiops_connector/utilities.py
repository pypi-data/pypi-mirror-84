import json
import os

from .exceptions import ConnectorError


def get_variable(variable_name, default_value=None):
    """
    Get the environment variable with the given name. If the variable is not set and a default value is passed, use
    this value.

    :param str variable_name: the name of the variable
    :param str default_value: the default value of the variable in case it is not set
    :return: the value for the given environment variable
    """

    if variable_name in os.environ:
        return os.environ[variable_name]
    elif default_value:
        return default_value

    raise ConnectorError(f"Environment variable {variable_name} is not set")


def map_data(data):
    """
    Map data, in case the fields in the connector are different from its input fields. The environment variable
    `MAPPING` is used to specify the input fields to actual columns in the database.

    Mapping only works for structured connectors.

    :param dict data: input data
    :return dict: mapped data
    """

    # Map data
    mapping = os.environ.get('MAPPING', None)

    if mapping:
        mapping = json.loads(mapping)

        for old_field in data.keys():
            if old_field in mapping:
                data[mapping[old_field]] = data.pop(old_field)

    return data
