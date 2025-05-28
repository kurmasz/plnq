def generate(data):
    data['params']['names_for_user'] = []
    data["params"]["names_from_user"] = [
  {
    "name": "extract_phone",
    "description": "A function that extract the digits from a formatted phone number",
    "type": "function"
  },
  {
    "name": "parse_format",
    "description": "A function to parse matplotlib's format string",
    "type": "function"
  },
  {
    "name": "get_first_quote",
    "description": "A function returning the first quote in a string",
    "type": "function"
  }
]