# define a dictionary of conversion factors
factors = {
    "ns": 1e-9,  # nanoseconds
    "us": 1e-6,  # microseconds
    "ms": 1e-3,  # milliseconds
    "s": 1,  # seconds
    "m": 60,  # minutes
    "h": 3600,  # hours
    "d": 86400  # days
}

reversed_factors = {
    1e-9: "ns",
    1e-6: "us",
    1e-3: "ms",
    1: "s",
    60: "m",
    3600: "h",
    86400: "d"
}


# define a function to convert time units
def convert_time(value, from_unit: str, to_unit: str):
    from_factor = factors.get(from_unit)
    to_factor = factors.get(to_unit)
    if from_factor and to_factor:
        # convert the value from the from_unit to seconds
        value_in_seconds = value * from_factor
        # convert the value from seconds to the to_unit
        value_in_to_unit = value_in_seconds / to_factor
        return value_in_to_unit
    else:
        return None
