def generate(data):
    data['params']['names_for_user'] = []
    data["params"]["names_from_user"] = [
  {
    "name": "largest_population",
    "description": "A function that returns the jurisdiction with the largest population.",
    "type": "function"
  },
  {
    "name": "first_match",
    "description": "A function that returns the first line containing the given string",
    "type": "function"
  },
  {
    "name": "last_match",
    "description": "A function that returns the last line containing the given string",
    "type": "function"
  }
]