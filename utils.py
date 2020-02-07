import re

def cast_input(input_str: str) -> bool:
  """Check that input value is allowed, otherwise complain with raised exception."""
  input_str = str.strip(input_str)
  if re.match('^[1-9]{1}$', input_str) is None:
    raise Exception('Input values must be between 1-9')
  else:
    return int(input_str)

if __name__ == "__main__":
    cast_input()