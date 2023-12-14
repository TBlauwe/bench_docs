from typing import List, Any


def retrieve_value_from_dict(data: dict, keys: List[str]) -> Any:
    assert (len(keys) > 0)
    key = keys.pop(0)
    if len(keys) > 0:  # It means we still have to navigate through dict hierarchies
        return retrieve_value_from_dict(data[key], keys)
    else:  # Otherwise we finished navigating and can return the value
        return data[key]


def retrieve_integer(s: str):
    if s.startswith("@"):
        num = s.split("@")[1]
        try:
            num = int(num)
            return num
        except ValueError:
            return None
    else:
        return None
