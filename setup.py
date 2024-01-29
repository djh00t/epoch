#!/usr/bin/env python

import urllib.request
import os
import subprocess
import sys

ENV_NAME = os.path.basename(os.getcwd())
PYTHON_VERSION = '3.10'

def install_miniconda():
    """
    Install Miniconda if Conda is not already installed.
    """
    print("Checking for Conda installation...")
    conda_installed = subprocess.run(['which', 'conda'], stdout=subprocess.PIPE).stdout
    if not conda_installed:
        print("Conda not found. Installing Miniconda...")
        miniconda_installer = "Miniconda3-latest-Linux-x86_64.sh" if sys.platform.startswith('linux') else "Miniconda3-latest-MacOSX-x86_64.sh"
        miniconda_url = f"https://repo.anaconda.com/miniconda/{miniconda_installer}"
        installer_path = os.path.join(os.getcwd(), miniconda_installer)
        urllib.request.urlretrieve(miniconda_url, installer_path)
        os.chmod(installer_path, 0o755)
        subprocess.run([installer_path, "-b", "-p", os.path.expanduser("~/miniconda")])
        conda_path = os.path.expanduser("~/miniconda/bin")
        os.environ["PATH"] += os.pathsep + conda_path
        subprocess.run(["conda", "init"])
        print("Miniconda installed successfully.")
    else:
        print("Conda is already installed.")

def main():
    install_miniconda()

    # Check if the conda environment exists
    env_list = subprocess.run(['conda', 'env', 'list'], stdout=subprocess.PIPE)
    envs = env_list.stdout.decode().splitlines()
    env_exists = any(ENV_NAME in env for env in envs)

    if env_exists:
        # Activate the environment
        print(f"Activating Conda environment '{ENV_NAME}'...")
        os.system(f"conda activate {ENV_NAME}")
    else:
        # Create the environment
        print(f"Creating Conda environment '{ENV_NAME}' with Python {PYTHON_VERSION}...")
        os.system(f"conda create --name {ENV_NAME} python={PYTHON_VERSION} --yes")
        os.system(f"conda activate {ENV_NAME}")

    # Install the required libraries from condareq.txt
    print("Installing libraries from condareq.txt...")
    os.system(f"conda env update --name {ENV_NAME} --file condareq.txt --prune")

    print("Setup complete.")

if __name__ == '__main__':
    main()
