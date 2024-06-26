from dotenv import load_dotenv
load_dotenv()

from router import create_app
import logging


logging.basicConfig(level=logging.INFO)
app = create_app()
