from typing import Iterator, Tuple


def yield_env_vars_from_file(file_path: str) -> Iterator[Tuple[str, str]]:
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

            yield k, v