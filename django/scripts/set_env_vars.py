import os

from scripts.utils import yield_env_vars_from_file


def set_env_vars(file_path: str) -> None:
    for k, v in yield_env_vars_from_file(file_path=file_path):
        os.environ[k] = v
