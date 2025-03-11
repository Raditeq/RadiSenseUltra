__author__ = "Raditeq"
__copyright__ = "Copyright (C) 2025 Raditeq"
__license__ = "MIT"

import subprocess
import sys

def install_requirements(requirements_file="requirements.txt"):
    """
    Install packages from the given requirements file.

    :param requirements_file: Path to the requirements.txt file.
    """
    try:
        # Run the pip install command
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing packages: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Install requirements from requirements.txt
    install_requirements()
