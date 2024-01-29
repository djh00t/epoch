#!/usr/bin/env python

import os
import subprocess
import sys

ENV_NAME = os.path.basename(os.getcwd())
PYTHON_VERSION = '3.10'

def main():
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
