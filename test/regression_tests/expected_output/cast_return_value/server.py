def generate(data):
    data['params']['names_for_user'] = []
    data["params"]["names_from_user"] = [
  {
    "name": "is_standard_phone_number",
    "description": "Is a string a phone number.",
    "type": "function"
  },
  {
    "name": "is_paren_phone_number",
    "description": "Is a string a phone number (with or without parens)",
    "type": "function"
  },
  {
    "name": "is_dotted_phone_number",
    "description": "is_dotted_phone_number",
    "type": "function"
  },
  {
    "name": "is_integer",
    "description": "Is a string an integer",
    "type": "function"
  },
  {
    "name": "is_ip_address",
    "description": "is_ip_address",
    "type": "function"
  }
]