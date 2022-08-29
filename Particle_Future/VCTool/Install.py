import sys
import subprocess
class Install:

    # Install all packages needed to webscrape
    def installPackages(self):
        packages = ["flask"]
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])  # import data libraries
