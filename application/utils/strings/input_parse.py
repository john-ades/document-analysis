import json
from typing import Union

from application.errors import APIError


def str_input_parse(s: Union[str, list[str], set[str]]) -> list[str]:
    if isinstance(s,str):
        # check for commas
        if "[" in s or "{" in s:
            # replace brackets with parenthesis
            s = s\
                .replace("{","[")\
                .replace("}","]")
            # check if this is a json array
            try:
                data = json.loads(s)
            except json.decoder.JSONDecodeError:
                raise APIError(f"Could not interpret the string input '{s}'.")
            return data
        elif "," in s:
            # comma seperated list
            return [string.strip() for string in s.split(",") if len(string.strip()) != 0]
        # assume this is a simple string
        return [s]
    elif isinstance(s, list) or isinstance(s, set):
        data = list(s)
        # make sure each element in array is a string
        if not all(isinstance(item, str) for item in data):
            raise APIError("Array input must only contain string types as their items")
        return data
    else:
        raise APIError(f"Could not interpret the string input type '{type(s)}'. "
                       f"Can only accept types [str, list[str], set[str]].")
