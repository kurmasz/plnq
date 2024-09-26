def generate(data):
    data['params']['names_for_user'] = []
    data["params"]["names_from_user"] = [
  {
    "name": "letters_in_string",
    "description": "A function that returns the number of letters in a string",
    "type": "function"
  },
  {
    "name": "num_long_words",
    "description": "A function that returns the number of words longer than the threshold",
    "type": "function"
  },
  {
    "name": "first_alphabetically",
    "description": "A function that returns the word in a phrase that comes first alphabetically",
    "type": "function"
  },
  {
    "name": "create_abbreviation",
    "description": "A function that returns an abbreviated version of a phrase",
    "type": "function"
  }
]