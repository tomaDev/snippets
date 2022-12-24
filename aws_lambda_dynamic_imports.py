import importlib
import os
import subprocess
import sys
import tempfile

EXAMPLE_MODULE = "requests"


def install_packages(packages: str):
    """
    Dynamically pip install packages to import modules
    Suitable when you only have write permissions to temp
    (No control over deployment, no S3 write permissions etc)
    AND you're ok with:
    - RAM as storage for both modules and dependancies
    - Increased runtime
    - Implied cost etc

    @packages: str, required - either literal package names,
        or a filename in the function directory (eg requirements.txt)

    Returns: directory path of the newly installed
    """
    if not packages:
        return
    if os.path.isfile(packages):
        packages = f"-r {packages}"

    packages_dir = tempfile.mkdtemp(prefix="packages-")
    result = subprocess.run(
        f"pip install {packages} --target {packages_dir}",
        shell=True
    )
    sys.path.append(packages_dir)
    return packages_dir


def lambda_handler(event, context):
    # download, install and ref packages
    packages_dir = install_packages(EXAMPLE_MODULE)

    # import EXAMPLE_MODULE
    imported_module = importlib.import_module(EXAMPLE_MODULE)

    return {
        "Wheels and packages": str(os.listdir(packages_dir)),
        "Imports": str(imported_module)
    }
