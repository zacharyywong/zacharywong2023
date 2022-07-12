# Install all packages needed for webscrape

import sys
import subprocess


# Install all packages needed to webscrape
def installPackages():
    packages = ["pandas", "IPython", "numpy", "xlwt", "wheel", "html5lib", "bs4", "openpyxl", "selenium",
                "webdriver-manager"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])  # import data libraries


if __name__ == '__main__':
    installPackages()