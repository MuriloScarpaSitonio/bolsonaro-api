import os
import subprocess

from decouple import config as secret

DATABASE_USER = secret("DATABASE_USER", default="postgres")
DATABASE_PASSWORD = secret("DATABASE_PASSWORD", default="password")


def main() -> None:
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
    failures = []

    if not os.path.exists(".env"):
        print("ERROR!! .env file is missing!")
        return

    with open(".env", encoding="UTF-8") as file_:
        for line in file_:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            k, v = line.split("=", 1)
            if k.startswith("POSTGRES"):
                print("Skipping POSTGRES values - Amazon RDS provides these")
                continue

            v = v.strip()
            k = k.strip()
            if len(v) >= 2 and (
                (v.startswith("'") and v.endswith("'"))
                or (v.startswith('"') and v.endswith('"'))
            ):
                v = v.strip("'\"")

            if k in ("DATABASE_USER", "DATABASE_PASSWORD"):
                continue

            if v:
                command.append(f"{k}={v}")
            else:
                failures.append(k)
    if failures:
        for failure in failures:
            print(f"{failure} requires a value")
    else:
        print("Executing the following command...")
        print(" ".join(command))
        subprocess.check_call(command)


if __name__ == "__main__":
    main()
