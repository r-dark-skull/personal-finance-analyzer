from dotenv import load_dotenv
import tomllib

load_dotenv()

with open("credentials.toml", "rb") as toml_file:
    credentials = tomllib.load(toml_file)
context = {}
