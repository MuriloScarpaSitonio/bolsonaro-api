import os
import subprocess
import sys
from typing import Iterable

from utils import yield_env_vars_from_file


def main(eb_env_name: str, env_files_path: Iterable[str]) -> None:
    """Create an AWS Elastic Beanstalk environment with env vars.

    Args:
        eb_env_name (str): Environment's name;
        env_files_path (Iterable[str]): Paths to env files.
    """
    eb_create_command = [
        "eb",
        "create",
        eb_env_name,
        "--scale=1",
        "--cname=bolsonaro-api",
        "--elb-type=application",
        "--verbose",
        "--envvars",
    ]
    aws_rds_command = ["--database.engine=postgres", "--database.instance=db.t2.micro"]
    aws_eb_env_vars = []

    for file_path in env_files_path:
        failures = []

        if not os.path.exists(file_path):
            print(f"ERROR!! {file_path} file is missing!")
            return

        for k, v in yield_env_vars_from_file(file_path=file_path):
            if k == "DATABASE_USER":
                aws_rds_command.append(f"--database.username={v}")
                continue
            if k == "DATABASE_PASSWORD":
                aws_rds_command.append(f"--database.password={v}")
                continue

            if v:
                aws_eb_env_vars.append(f"{k}={v}")
            else:
                failures.append(k)

        if failures:
            for failure in failures:
                print(f"{failure} requires a value")

    if len(aws_rds_command) == 4:
        eb_create_command.insert(4, " ".join(aws_rds_command))
    else:
        print("ERROR!! DATABASE_USER or DATABASE_PASSWORD RDS env vars are missing!")
        return

    eb_create_command.append(",".join(aws_eb_env_vars))
    print("Executing the following command:\n\n")
    print(" ".join(eb_create_command))
    print("\n\n")
    subprocess.check_call(eb_create_command)


if __name__ == "__main__":
    pwd = os.environ.get("PWD")
    if not pwd:
        sys.exit("PWD env var is not available, please make sure to set it.")
    main(
        eb_env_name="bolsonaro-api-env",
        env_files_path=[
            f"{pwd}/django/.env",
            f"{pwd}/react/.env",
            f"{pwd}/postgres/.env",
        ],
    )
