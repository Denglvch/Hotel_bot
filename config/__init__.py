import os
from dotenv import dotenv_values


try:
    if os.path.exists('.venv'):
        config = dotenv_values('.venv')
    elif os.path.exists('../.venv'):
        config = dotenv_values('../.venv')
    else:
        raise FileExistsError('Файл ".venv.templates" отсутвует, либо находится вне корневого каталога.')
except FileExistsError:
    raise
