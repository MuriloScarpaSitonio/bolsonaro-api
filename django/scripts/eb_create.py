import os
import subprocess

from decouple import config as secret

from scripts.utils import yield_env_vars_from_file

DATABASE_USER = secret("DATABASE_USER", default="postgres")
DATABASE_PASSWORD = secret("DATABASE_PASSWORD", default="password")


def main(file_path: str) -> None:
    command = [
        "eb",
        "create",
        "--scale=1",
        f"--database.username={DATABASE_USER}",
        f"--database.password={DATABASE_PASSWORD}",
        "--database.engine=postgres",
        "--database.instance=db.t2.micro",
        "--envvars",
    ]
    aws_eb_env_vars = []
    failures = []

    if not os.path.exists(".env"):
        print("ERROR!! .env file is missing!")
        return

    for k, v in yield_env_vars_from_file(file_path=file_path):
        if k in ("DATABASE_USER", "DATABASE_PASSWORD"):
            continue

        if v:
            aws_eb_env_vars.append(f"{k}={v}")
        else:
            failures.append(k)

    if failures:
        for failure in failures:
            print(f"{failure} requires a value")
    else:
        command.append(",".join(aws_eb_env_vars))
        print("Executing the following command:\n\n")
        print(" ".join(command))
        print("\n\n")
        subprocess.check_call(command)


if __name__ == "__main__":
    FILE_PATH = ".env"
    main(file_path=FILE_PATH)
