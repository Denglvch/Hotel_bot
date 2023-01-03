import os
from dotenv import dotenv_values


if os.path.exists('.venv.templates'):
    config = dotenv_values('.venv.templates')
else:
    config = dotenv_values('../.venv.templates')
