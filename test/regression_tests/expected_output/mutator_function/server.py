def generate(data):
    data['params']['names_for_user'] = []
    data["params"]["names_from_user"] = [
  {
    "name": "remove_suffixes",
    "description": "A function to convert \"+/-\" grades into \"straight\" grades",
    "type": "function"
  },
  {
    "name": "truncate",
    "description": "A function to adjust list values to remain in a given range",
    "type": "function"
  },
  {
    "name": "truncate_and_count",
    "description": "Another function to adjust list values to remain in a given range",
    "type": "function"
  }
]