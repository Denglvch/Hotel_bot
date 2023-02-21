import os
from dotenv import dotenv_values


try:
    if os.path.exists('.venv.templates'):
        config = dotenv_values('.venv.templates')
    elif os.path.exists('../.venv.templates'):
        config = dotenv_values('../.venv.templates')
    else:
        raise FileExistsError('Файл ".venv.templates" отсутвует, либо находится вне корневого каталога.')
except FileExistsError:
    raise
