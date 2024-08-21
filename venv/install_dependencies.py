import subprocess
import sys

def install_dependencies():
    try:
        # Read the requirements.txt file
        with open('requirements.txt', 'r') as file:
            requirements = file.read().splitlines()

        # Install each requirement using pip
        for requirement in requirements:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', requirement])
        print("All dependencies installed successfully.")

    except Exception as e:
        print(f"An error occurred while installing dependencies: {e}")

# Call the function to install dependencies
install_dependencies()
