import os

def get_env_variable(variable_name, default_value=''):
    return os.environ.get(variable_name, default_value)

def parse_comma_str_to_list(comma_sep_str):
    if not comma_sep_str or not isinstance(comma_sep_str, str):
        return []
    cleaned = comma_sep_str.strip().strip("'\"")
    return [s.strip().strip('\'"') for s in cleaned.split(',') if s.strip()]