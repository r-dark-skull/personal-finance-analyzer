import tomllib


with open("credentials.toml", "rb") as toml_file:
    credentials = tomllib.load(toml_file)
context = {}
