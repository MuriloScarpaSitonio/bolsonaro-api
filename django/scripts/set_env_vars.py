import os

from scripts.utils import yield_env_vars_from_file

FILE_PATH = "/opt/elasticbeanstalk/deployment/env"


def set_env_vars():
    for k, v in yield_env_vars_from_file(file_path=FILE_PATH):
        os.environ[k] = v
