from argparse import ArgumentParser
from hashlib import md5
from os import system
from tempfile import TemporaryDirectory


def cleanup_files(folder):
    system(f'find {folder} -path "*/__pycache__*" -delete 1>/dev/null')


def install_requirements(requirements: str, folder) -> None:
    if not requirements:
        return
    system(f"pip install -q -r {requirements} --target {folder} 1>/dev/null")


def copy_inputs(inputs: str, folder) -> None:
    for inp in inputs:
        system(f"cp --parents -r -p {inp} {folder} 1>/dev/null")


def build_zip(output_filename: str, requirements: str, inputs: str) -> None:
    with TemporaryDirectory() as destination:
        install_requirements(requirements=requirements, folder=destination)
        copy_inputs(inputs=inputs, folder=destination)
        cleanup_files(folder=destination)
        system(f"mkdir -p $(dirname {output_filename})")
        system(f"cd {destination}; zip -X -q {output_filename} -r . >/dev/null")


if __name__ == "__main__":
    parser = ArgumentParser(description="Create lambda function package")
    parser.add_argument(
        "-r",
        "--requirements",
        dest="requirements",
        default=None,
        help="The path to the pip requirements file.",
    )
    parser.add_argument("output_filename", help="The filename of the output zip file.")
    parser.add_argument(
        "inputs", type=str, nargs="+", help="The source files to be included."
    )
    args = vars(parser.parse_args())

    build_zip(
        output_filename=args["output_filename"],
        requirements=args["requirements"],
        inputs=args["inputs"],
    )
    md5sum = md5(open(args["output_filename"], "rb").read()).hexdigest()
    print('{"md5sum": "' + md5sum + '"}')
